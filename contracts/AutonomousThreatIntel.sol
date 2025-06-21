// SPDX-License-Identifier: Apache-2.0
pragma solidity ^0.8.20;

/// @title AutonomousThreatIntel
/// @notice Decentralized, unstoppable AI-driven threat report and intelligence hub.
contract AutonomousThreatIntel {
    struct ThreatReport {
        address reporter;
        string target;      // Target system or address
        string description; // Threat description
        string aiAssessment;
        uint256 severity;   // 1 (Critical) - 5 (Low)
        uint256 timestamp;
        bool aiValidated;
    }

    uint256 public totalThreats;
    address public aiAgent;
    mapping(uint256 => ThreatReport) public threats;

    event ThreatSubmitted(uint256 indexed reportId, address indexed reporter, string target, string description);
    event ThreatAssessed(uint256 indexed reportId, string aiAssessment, uint256 severity);

    modifier onlyAIAgent() {
        require(msg.sender == aiAgent, "Not authorized");
        _;
    }

    constructor(address _aiAgent) {
        aiAgent = _aiAgent;
    }

    function submitThreat(string memory target, string memory description) public returns (uint256) {
        totalThreats++;
        threats[totalThreats] = ThreatReport({
            reporter: msg.sender,
            target: target,
            description: description,
            aiAssessment: "",
            severity: 0,
            timestamp: block.timestamp,
            aiValidated: false
        });
        emit ThreatSubmitted(totalThreats, msg.sender, target, description);
        return totalThreats;
    }

    function aiAssessThreat(uint256 reportId, string memory aiAssessment, uint256 severity) public onlyAIAgent {
        ThreatReport storage report = threats[reportId];
        require(!report.aiValidated, "Already validated");
        require(severity > 0 && severity <= 5, "Severity must be 1-5");
        report.aiAssessment = aiAssessment;
        report.severity = severity;
        report.aiValidated = true;
        emit ThreatAssessed(reportId, aiAssessment, severity);
    }

    function getThreat(uint256 reportId) external view returns (
        address reporter, string memory target, string memory description,
        string memory aiAssessment, uint256 severity, uint256 timestamp, bool aiValidated
    ) {
        ThreatReport storage r = threats[reportId];
        return (r.reporter, r.target, r.description, r.aiAssessment, r.severity, r.timestamp, r.aiValidated);
    }
}
