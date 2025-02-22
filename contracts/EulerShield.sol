// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/utils/math/SafeMath.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract EulerShield is Ownable, ReentrancyGuard {
    using SafeMath for uint256;

    // Events
    event SupplyAdjusted(uint256 newSupply);
    event GovernanceProposalCreated(uint256 proposalId, string description);
    event VoteCast(uint256 proposalId, address voter, bool support);
    event StakingRewardDistributed(address indexed user, uint256 amount);

    // Governance structure
    struct Proposal {
        string description;
        uint256 voteCountFor;
        uint256 voteCountAgainst;
        uint256 endTime;
        bool executed;
    }

    // Staking structure
    struct Staker {
        uint256 amount;
        uint256 rewardDebt;
    }

    // State variables
    IERC20 public piCoin; // Reference to Pi Coin contract
    uint256 public totalSupply;
    uint256 public targetValue; // Target value for Pi Coin
    uint256 public constant MAX_SUPPLY = 100_000_000_000 * 10 ** 18; // Max supply of Pi Coin
    uint256 public rewardRate; // Reward rate for staking
    mapping(address => Staker) public stakers;
    Proposal[] public proposals;

    // Constructor
    constructor(IERC20 _piCoin, uint256 _targetValue, uint256 _rewardRate) {
        piCoin = _piCoin;
        targetValue = _targetValue;
        rewardRate = _rewardRate;
    }

    // Function to adjust supply based on market conditions
    function adjustSupply(uint256 currentPrice) external onlyOwner {
        if (currentPrice < targetValue) {
            uint256 amountToMint = (targetValue - currentPrice).mul(10 ** 18); // Example calculation
            require(totalSupply.add(amountToMint) <= MAX_SUPPLY, "Exceeds max supply");
            totalSupply = totalSupply.add(amountToMint);
            emit SupplyAdjusted(totalSupply);
        } else if (currentPrice > targetValue) {
            uint256 amountToBurn = (currentPrice - targetValue).mul(10 ** 18); // Example calculation
            require(totalSupply >= amountToBurn, "Insufficient supply to burn");
            totalSupply = totalSupply.sub(amountToBurn);
            emit SupplyAdjusted(totalSupply);
        }
    }

    // Governance proposal creation
    function createProposal(string memory description) external onlyOwner {
        proposals.push(Proposal({
            description: description,
            voteCountFor: 0,
            voteCountAgainst: 0,
            endTime: block.timestamp + 1 weeks,
            executed: false
        }));
        emit GovernanceProposalCreated(proposals.length - 1, description);
    }

    // Voting on proposals
    function vote(uint256 proposalId, bool support) external {
        require(proposalId < proposals.length, "Invalid proposal ID");
        Proposal storage proposal = proposals[proposalId];
        require(block.timestamp < proposal.endTime, "Voting has ended");

        if (support) {
            proposal.voteCountFor = proposal.voteCountFor.add(1);
        } else {
            proposal.voteCountAgainst = proposal.voteCountAgainst.add(1);
        }
        emit VoteCast(proposalId, msg.sender, support);
    }

    // Staking function
    function stake(uint256 amount) external nonReentrant {
        require(amount > 0, "Amount must be greater than 0");
        piCoin.transferFrom(msg.sender, address(this), amount);
        stakers[msg.sender].amount = stakers[msg.sender].amount.add(amount);
    }

    // Distributing staking rewards
    function distributeRewards() external onlyOwner {
        for (uint256 i = 0; i < proposals.length; i++) {
            Proposal storage proposal = proposals[i];
            if (proposal.executed) continue;

            uint256 totalVotes = proposal.voteCountFor.add(proposal.voteCountAgainst);
            if (totalVotes > 0) {
                uint256 reward = rewardRate.mul(totalVotes);
                for (address staker : stakers) {
                    uint256 userShare = stakers[staker].amount.mul(1e18).div(totalSupply);
                    uint256 userReward = reward.mul(userShare).div(1e18);
                    stakers[staker].rewardDebt = stakers[staker].rewardDebt.add(userReward);
                    emit StakingRewardDistributed(staker, userReward);
                }
                proposal.executed = true }
        }
    }

    // Function to claim rewards
    function claimRewards() external nonReentrant {
        uint256 reward = stakers[msg.sender].rewardDebt;
        require(reward > 0, "No rewards to claim");
        stakers[msg.sender].rewardDebt = 0;
        piCoin.transfer(msg.sender, reward);
    }

    // Function to get the current proposal status
    function getProposalStatus(uint256 proposalId) external view returns (string memory description, uint256 voteCountFor, uint256 voteCountAgainst, bool executed) {
        require(proposalId < proposals.length, "Invalid proposal ID");
        Proposal storage proposal = proposals[proposalId];
        return (proposal.description, proposal.voteCountFor, proposal.voteCountAgainst, proposal.executed);
    }

    // Function to get the staking balance of a user
    function getStakingBalance(address user) external view returns (uint256) {
        return stakers[user].amount;
    }

    // Function to get total supply
    function getTotalSupply() external view returns (uint256) {
        return totalSupply;
    }
}
