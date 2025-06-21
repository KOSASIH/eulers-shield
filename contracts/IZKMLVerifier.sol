// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface IZKMLVerifier {
    function verifyProof(
        bytes calldata proof,
        uint256[] calldata publicSignals
    ) external view returns (bool);
}

contract ZKMLDecisionRegistry {
    address public verifier;
    event DecisionProved(address indexed agent, bytes32 signalHash, bool result);

    constructor(address _verifier) {
        verifier = _verifier;
    }

    function proveDecision(
        bytes calldata proof,
        uint256[] calldata publicSignals,
        bytes32 signalHash,
        bool result
    ) external {
        require(
            IZKMLVerifier(verifier).verifyProof(proof, publicSignals),
            "Invalid ZKML proof"
        );
        emit DecisionProved(msg.sender, signalHash, result);
    }
}
