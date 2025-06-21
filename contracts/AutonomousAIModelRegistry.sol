// SPDX-License-Identifier: Apache-2.0
pragma solidity ^0.8.20;

/// @title AutonomousAIModelRegistry
/// @notice Decentralized, unstoppable registry for AI models, upgrades, and activation.
contract AutonomousAIModelRegistry {
    struct Model {
        string name;
        string version;
        string ipfsHash; // Location of the model weights, manifest, or code
        address submitter;
        bool verified;
        bool active;
        uint256 timestamp;
    }

    uint256 public totalModels;
    mapping(uint256 => Model) public models;
    address public owner;
    address public verifier; // Can be an AI agent or DAO agent

    event ModelSubmitted(uint256 indexed modelId, string name, string version, string ipfsHash, address submitter);
    event ModelVerified(uint256 indexed modelId, bool verified, address verifier);
    event ModelActivated(uint256 indexed modelId, bool active);

    modifier onlyVerifier() {
        require(msg.sender == verifier, "Not authorized");
        _;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner");
        _;
    }

    constructor(address _verifier) {
        owner = msg.sender;
        verifier = _verifier;
    }

    function submitModel(string memory name, string memory version, string memory ipfsHash) public returns (uint256) {
        totalModels++;
        models[totalModels] = Model({
            name: name,
            version: version,
            ipfsHash: ipfsHash,
            submitter: msg.sender,
            verified: false,
            active: false,
            timestamp: block.timestamp
        });
        emit ModelSubmitted(totalModels, name, version, ipfsHash, msg.sender);
        return totalModels;
    }

    function verifyModel(uint256 modelId, bool status) public onlyVerifier {
        models[modelId].verified = status;
        emit ModelVerified(modelId, status, msg.sender);
    }

    function activateModel(uint256 modelId, bool status) public onlyOwner {
        require(models[modelId].verified, "Model must be verified");
        models[modelId].active = status;
        emit ModelActivated(modelId, status);
    }

    function setVerifier(address _verifier) public onlyOwner {
        verifier = _verifier;
    }

    function getModel(uint256 modelId) external view returns (
        string memory, string memory, string memory, address, bool, bool, uint256
    ) {
        Model storage m = models[modelId];
        return (m.name, m.version, m.ipfsHash, m.submitter, m.verified, m.active, m.timestamp);
    }
}
