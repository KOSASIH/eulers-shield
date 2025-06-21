// SPDX-License-Identifier: Apache-2.0
pragma solidity ^0.8.20;

/// @title AutonomousGrantDAO
/// @notice An unstoppable, AI-powered, feature-rich autonomous grant review and distribution contract.
contract AutonomousGrantDAO {
    struct GrantApp {
        address applicant;
        string project;
        string aiReview;     // AI's review text (impact, feasibility, rationale)
        uint256 requested;   // Amount requested (in wei)
        uint256 awarded;     // Amount awarded (in wei)
        bool aiReviewed;     // Has AI reviewed this application?
        bool funded;         // Has this application been funded?
    }

    uint256 public totalApps;
    address public aiAgent;
    address public owner;
    uint256 public grantPool;
    mapping(uint256 => GrantApp) public applications;

    event GrantApplied(
        uint256 indexed appId,
        address indexed applicant,
        string project,
        uint256 requested
    );
    event GrantReviewed(
        uint256 indexed appId,
        string aiReview,
        uint256 awarded
    );
    event GrantFunded(
        uint256 indexed appId,
        address indexed applicant,
        uint256 awarded
    );

    modifier onlyAIAgent() {
        require(msg.sender == aiAgent, "Not authorized");
        _;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner");
        _;
    }

    /// @notice Constructor - sets the AI agent and initializes the grant pool
    /// @param _aiAgent The address of the trusted AI agent
    constructor(address _aiAgent) payable {
        aiAgent = _aiAgent;
        owner = msg.sender;
        grantPool = msg.value;
    }

    /// @notice Fund the grant pool (anyone can add funds)
    function fundGrantPool() external payable {
        require(msg.value > 0, "Zero value");
        grantPool += msg.value;
    }

    /// @notice Update the AI agent address
    function setAIAgent(address _aiAgent) external onlyOwner {
        require(_aiAgent != address(0), "Zero address");
        aiAgent = _aiAgent;
    }

    /// @notice Apply for a grant
    /// @param project Project details/description
    /// @param requested Amount requested in wei
    function applyForGrant(string calldata project, uint256 requested) external returns (uint256) {
        require(requested > 0, "Requested zero");
        totalApps++;
        applications[totalApps] = GrantApp({
            applicant: msg.sender,
            project: project,
            aiReview: "",
            requested: requested,
            awarded: 0,
            aiReviewed: false,
            funded: false
        });
        emit GrantApplied(totalApps, msg.sender, project, requested);
        return totalApps;
    }

    /// @notice AI agent reviews a grant application and sets the award amount (must not exceed requested or pool)
    /// @param appId Application ID
    /// @param review AI's review string/rationale
    /// @param awarded Amount to award (in wei)
    function aiReviewGrant(uint256 appId, string calldata review, uint256 awarded) external onlyAIAgent {
        GrantApp storage app = applications[appId];
        require(!app.aiReviewed, "Already reviewed");
        require(awarded <= app.requested && awarded <= grantPool, "Invalid award");
        app.aiReview = review;
        app.awarded = awarded;
        app.aiReviewed = true;
        emit GrantReviewed(appId, review, awarded);
    }

    /// @notice Fund the awarded grant. Anyone can trigger. Funds go to applicant.
    /// @param appId Application ID
    function fundGrant(uint256 appId) external {
        GrantApp storage app = applications[appId];
        require(app.aiReviewed, "Not reviewed");
        require(!app.funded, "Already funded");
        require(app.awarded > 0 && app.awarded <= grantPool, "Insufficient funds");
        app.funded = true;
        grantPool -= app.awarded;
        (bool sent, ) = payable(app.applicant).call{value: app.awarded}("");
        require(sent, "Transfer failed");
        emit GrantFunded(appId, app.applicant, app.awarded);
    }

    /// @notice Get application details (useful for off-chain agents)
    function getApplication(uint256 appId) external view returns (
        address applicant, string memory project, string memory aiReview, uint256 requested, uint256 awarded, bool aiReviewed, bool funded
    ) {
        GrantApp storage app = applications[appId];
        return (app.applicant, app.project, app.aiReview, app.requested, app.awarded, app.aiReviewed, app.funded);
    }

    /// @notice Get the contract's remaining grant pool (ETH)
    function getGrantPool() external view returns (uint256) {
        return grantPool;
    }

    /// @notice Emergency withdrawal by owner for unused funds
    function emergencyWithdraw(address to, uint256 amount) external onlyOwner {
        require(amount <= grantPool, "Exceeds pool");
        grantPool -= amount;
        (bool sent, ) = payable(to).call{value: amount}("");
        require(sent, "Withdraw failed");
    }

    receive() external payable {
        grantPool += msg.value;
    }
}
