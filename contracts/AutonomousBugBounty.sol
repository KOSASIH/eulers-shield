// SPDX-License-Identifier: Apache-2.0
pragma solidity ^0.8.20;

contract AutonomousBugBounty {
    struct BugReport {
        address reporter;
        string description;
        string aiAssessment; // AI’s validation and severity
        uint256 timestamp;
        uint256 reward;
        bool resolved;
        bool aiEvaluated;
    }

    uint256 public totalReports;
    address public aiAgent;
    address public owner;
    uint256 public bountyPool;
    mapping(uint256 => BugReport) public reports;

    event BugReported(uint256 indexed reportId, address indexed reporter, string description);
    event AIAssessed(uint256 indexed reportId, string aiAssessment, uint256 reward);
    event RewardClaimed(uint256 indexed reportId, address indexed reporter, uint256 reward);

    constructor(address _aiAgent) payable {
        aiAgent = _aiAgent;
        owner = msg.sender;
        bountyPool = msg.value;
    }

    modifier onlyAIAgent() {
        require(msg.sender == aiAgent, "Not authorized");
        _;
    }

    function fundBountyPool() external payable {
        bountyPool += msg.value;
    }

    function reportBug(string calldata description) external returns (uint256) {
        totalReports++;
        reports[totalReports] = BugReport({
            reporter: msg.sender,
            description: description,
            aiAssessment: "",
            timestamp: block.timestamp,
            reward: 0,
            resolved: false,
            aiEvaluated: false
        });
        emit BugReported(totalReports, msg.sender, description);
        return totalReports;
    }

    function aiEvaluateBug(uint256 reportId, string calldata aiAssessment, uint256 reward) external onlyAIAgent {
        BugReport storage report = reports[reportId];
        require(!report.aiEvaluated, "Already evaluated");
        report.aiAssessment = aiAssessment;
        report.reward = reward;
        report.aiEvaluated = true;
        emit AIAssessed(reportId, aiAssessment, reward);
    }

    function claimReward(uint256 reportId) external {
        BugReport storage report = reports[reportId];
        require(report.aiEvaluated, "Not yet evaluated");
        require(!report.resolved, "Already claimed");
        require(report.reporter == msg.sender, "Only reporter can claim");
        require(report.reward > 0 && report.reward <= bountyPool, "Invalid reward");
        report.resolved = true;
        bountyPool -= report.reward;
        payable(msg.sender).transfer(report.reward);
        emit RewardClaimed(reportId, msg.sender, report.reward);
    }
}
