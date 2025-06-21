// SPDX-License-Identifier: Apache-2.0
pragma solidity ^0.8.20;

contract EulersShieldDAO {
    struct Proposal {
        uint256 id;
        address proposer;
        string title;
        string description;
        uint256 createdAt;
        uint256 votingDeadline;
        string aiSummary;
        string aiRecommendation;
        mapping(address => bool) hasVoted;
        uint256 yesVotes;
        uint256 noVotes;
        bool executed;
        bool aiEvaluated;
    }

    uint256 public proposalCount;
    uint256 public votingPeriod = 3 days;
    mapping(uint256 => Proposal) public proposals;

    event ProposalCreated(uint256 indexed id, address indexed proposer, string title, string description);
    event AISummaryPosted(uint256 indexed id, string summary, string recommendation);
    event Voted(uint256 indexed id, address indexed voter, bool support);
    event ProposalExecuted(uint256 indexed id);

    modifier proposalExists(uint256 _id) {
        require(_id > 0 && _id <= proposalCount, "Proposal does not exist");
        _;
    }

    function createProposal(string memory _title, string memory _description) public returns (uint256) {
        proposalCount++;
        Proposal storage prop = proposals[proposalCount];
        prop.id = proposalCount;
        prop.proposer = msg.sender;
        prop.title = _title;
        prop.description = _description;
        prop.createdAt = block.timestamp;
        prop.votingDeadline = block.timestamp + votingPeriod;

        emit ProposalCreated(prop.id, msg.sender, _title, _description);
        return prop.id;
    }

    function postAISummary(
        uint256 _id,
        string memory _summary,
        string memory _recommendation
    ) public proposalExists(_id) {
        Proposal storage prop = proposals[_id];
        require(!prop.aiEvaluated, "AI summary already posted");
        // Optionally: require(msg.sender == authorizedAI, ...);
        prop.aiSummary = _summary;
        prop.aiRecommendation = _recommendation;
        prop.aiEvaluated = true;

        emit AISummaryPosted(_id, _summary, _recommendation);
    }

    function vote(uint256 _id, bool _support) public proposalExists(_id) {
        Proposal storage prop = proposals[_id];
        require(block.timestamp < prop.votingDeadline, "Voting has ended");
        require(!prop.hasVoted[msg.sender], "Already voted");
        require(prop.aiEvaluated, "AI summary not posted yet");

        prop.hasVoted[msg.sender] = true;
        if (_support) {
            prop.yesVotes++;
        } else {
            prop.noVotes++;
        }

        emit Voted(_id, msg.sender, _support);
    }

    function executeProposal(uint256 _id) public proposalExists(_id) {
        Proposal storage prop = proposals[_id];
        require(block.timestamp >= prop.votingDeadline, "Voting not ended");
        require(!prop.executed, "Already executed");
        require(prop.yesVotes > prop.noVotes, "Proposal rejected");

        prop.executed = true;
        // Insert execution logic, e.g. call external contracts, upgrade system, etc.
        emit ProposalExecuted(_id);
    }

    function getProposal(uint256 _id) public view proposalExists(_id) returns (
        uint256 id,
        address proposer,
        string memory title,
        string memory description,
        uint256 createdAt,
        uint256 votingDeadline,
        string memory aiSummary,
        string memory aiRecommendation,
        uint256 yesVotes,
        uint256 noVotes,
        bool executed,
        bool aiEvaluated
    ) {
        Proposal storage prop = proposals[_id];
        return (
            prop.id,
            prop.proposer,
            prop.title,
            prop.description,
            prop.createdAt,
            prop.votingDeadline,
            prop.aiSummary,
            prop.aiRecommendation,
            prop.yesVotes,
            prop.noVotes,
            prop.executed,
            prop.aiEvaluated
        );
    }
}

