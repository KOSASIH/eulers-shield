// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/math/SafeMath.sol";

contract Governance is Ownable {
    using SafeMath for uint256;

    // Events
    event ProposalCreated(uint256 proposalId, string description, address proposer);
    event Voted(uint256 proposalId, address voter, bool support);
    event ProposalExecuted(uint256 proposalId);

    // Proposal structure
    struct Proposal {
        string description;
        address proposer;
        uint256 voteCountFor;
        uint256 voteCountAgainst;
        uint256 endTime;
        bool executed;
    }

    // State variables
    Proposal[] public proposals;
    mapping(address => mapping(uint256 => bool)) public hasVoted; // Track if an address has voted on a proposal

    // Constructor
    constructor() {}

    // Function to create a new proposal
    function createProposal(string memory description) external {
        proposals.push(Proposal({
            description: description,
            proposer: msg.sender,
            voteCountFor: 0,
            voteCountAgainst: 0,
            endTime: block.timestamp + 1 weeks, // Voting period of 1 week
            executed: false
        }));
        emit ProposalCreated(proposals.length - 1, description, msg.sender);
    }

    // Function to vote on a proposal
    function vote(uint256 proposalId, bool support) external {
        require(proposalId < proposals.length, "Invalid proposal ID");
        Proposal storage proposal = proposals[proposalId];
        require(block.timestamp < proposal.endTime, "Voting has ended");
        require(!hasVoted[msg.sender][proposalId], "You have already voted on this proposal");

        if (support) {
            proposal.voteCountFor = proposal.voteCountFor.add(1);
        } else {
            proposal.voteCountAgainst = proposal.voteCountAgainst.add(1);
        }
        hasVoted[msg.sender][proposalId] = true; // Mark as voted
        emit Voted(proposalId, msg.sender, support);
    }

    // Function to execute a proposal if voting has ended
    function executeProposal(uint256 proposalId) external {
        require(proposalId < proposals.length, "Invalid proposal ID");
        Proposal storage proposal = proposals[proposalId];
        require(block.timestamp >= proposal.endTime, "Voting is still ongoing");
        require(!proposal.executed, "Proposal has already been executed");

        // Execute the proposal based on the voting outcome
        if (proposal.voteCountFor > proposal.voteCountAgainst) {
            // Logic for executing the proposal (e.g., changing a parameter)
            // This is where you would implement the changes proposed
        }

        proposal.executed = true; // Mark proposal as executed
        emit ProposalExecuted(proposalId);
    }

    // Function to get the details of a proposal
    function getProposal(uint256 proposalId) external view returns (
        string memory description,
        address proposer,
        uint256 voteCountFor,
        uint256 voteCountAgainst,
        uint256 endTime,
        bool executed
    ) {
        require(proposalId < proposals.length, "Invalid proposal ID");
        Proposal storage proposal = proposals[proposalId];
        return (
            proposal.description,
            proposal.proposer,
            proposal.voteCountFor,
            proposal.voteCountAgainst,
            proposal.endTime,
            proposal.executed
        );
    }

    // Function to get the total number of proposals
    function getProposalCount() external view returns (uint256) {
        return proposals.length;
    }
}
