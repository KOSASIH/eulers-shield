// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Migrations {
    address public owner;
    uint256 public last_completed_migration;

    modifier restricted() {
        require(msg.sender == owner, "Only the owner can call this function");
        _;
    }

    constructor() {
        owner = msg.sender; // Set the contract deployer as the owner
    }

    function setCompleted(uint256 completed) public restricted {
        last_completed_migration = completed; // Update the last completed migration
    }

    function upgrade(address new_address) public restricted {
        Migrations upgraded = Migrations(new_address); // Upgrade to a new Migrations contract
        upgraded.setCompleted(last_completed_migration); // Set the last completed migration in the new contract
    }
}
