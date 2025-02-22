// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/utils/math/SafeMath.sol";

contract Staking is Ownable, ReentrancyGuard {
    using SafeMath for uint256;

    // Events
    event Staked(address indexed user, uint256 amount);
    event Unstaked(address indexed user, uint256 amount);
    event RewardPaid(address indexed user, uint256 reward);

    // State variables
    IERC20 public piCoin; // Reference to the Pi Coin contract
    uint256 public rewardRate; // Reward rate per block
    uint256 public lastUpdateBlock; // Last block number when rewards were updated
    uint256 public totalStaked; // Total amount of Pi Coins staked
    mapping(address => uint256) public stakedBalances; // User's staked balance
    mapping(address => uint256) public rewards; // User's accumulated rewards

    // Constructor
    constructor(IERC20 _piCoin, uint256 _rewardRate) {
        piCoin = _piCoin;
        rewardRate = _rewardRate;
        lastUpdateBlock = block.number;
    }

    // Modifier to update rewards
    modifier updateReward(address account) {
        rewards[account] = earned(account);
        lastUpdateBlock = block.number;
        _;
    }

    // Function to stake Pi Coins
    function stake(uint256 amount) external nonReentrant updateReward(msg.sender) {
        require(amount > 0, "Cannot stake 0");
        piCoin.transferFrom(msg.sender, address(this), amount);
        stakedBalances[msg.sender] = stakedBalances[msg.sender].add(amount);
        totalStaked = totalStaked.add(amount);
        emit Staked(msg.sender, amount);
    }

    // Function to unstake Pi Coins
    function unstake(uint256 amount) external nonReentrant updateReward(msg.sender) {
        require(amount > 0, "Cannot unstake 0");
        require(stakedBalances[msg.sender] >= amount, "Insufficient staked balance");
        stakedBalances[msg.sender] = stakedBalances[msg.sender].sub(amount);
        totalStaked = totalStaked.sub(amount);
        piCoin.transfer(msg.sender, amount);
        emit Unstaked(msg.sender, amount);
    }

    // Function to claim rewards
    function claimRewards() external nonReentrant updateReward(msg.sender) {
        uint256 reward = rewards[msg.sender];
        require(reward > 0, "No rewards to claim");
        rewards[msg.sender] = 0;
        piCoin.transfer(msg.sender, reward);
        emit RewardPaid(msg.sender, reward);
    }

    // Function to calculate earned rewards
    function earned(address account) public view returns (uint256) {
        return stakedBalances[account].mul(rewardRate).mul(block.number - lastUpdateBlock).div(1e18).add(rewards[account]);
    }

    // Function to get the staked balance of a user
    function getStakedBalance(address account) external view returns (uint256) {
        return stakedBalances[account];
    }

    // Function to get the total staked amount
    function getTotalStaked() external view returns (uint256) {
        return totalStaked;
    }

    // Function to set a new reward rate (only owner)
    function setRewardRate(uint256 newRate) external onlyOwner {
        rewardRate = newRate;
    }
}
