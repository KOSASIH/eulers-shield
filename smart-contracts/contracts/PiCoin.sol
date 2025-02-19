// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract PiCoin {
    string public name = "Pi Coin";
    string public symbol = "PI";
    uint8 public decimals = 18;
    uint256 public totalSupply;
    mapping(address => uint256) public balanceOf;

    address public owner;
    uint256 public constant TARGET_VALUE = 314159 * 10 ** 18; // Target value of $314,159 in wei

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Mint(address indexed to, uint256 value);
    event Burn(address indexed from, uint256 value);
    event SupplyAdjusted(uint256 newSupply);

    modifier onlyOwner() {
        require(msg.sender == owner, "Not the contract owner");
        _;
    }

    constructor() {
        owner = msg.sender;
        totalSupply = 100000000000 * 10 ** uint256(decimals); // 100 billion Pi Coins with 18 decimals
        balanceOf[owner] = totalSupply; // Assign the total supply to the contract deployer
        emit Transfer(address(0), owner, totalSupply); // Emit transfer event for initial supply
    }

    function transfer(address _to, uint256 _value) public returns (bool success) {
        require(balanceOf[msg.sender] >= _value, "Insufficient balance");
        balanceOf[msg.sender] -= _value;
        balanceOf[_to] += _value;
        emit Transfer(msg.sender, _to, _value);
        return true;
    }

    // Mint new Pi Coins
    function mint(address _to, uint256 _value) public onlyOwner returns (bool success) {
        totalSupply += _value;
        balanceOf[_to] += _value;
        emit Mint(_to, _value);
        emit Transfer(address(0), _to, _value); // Emit transfer event for minting
        return true;
    }

    // Burn Pi Coins
    function burn(uint256 _value) public returns (bool success) {
        require(balanceOf[msg.sender] >= _value, "Insufficient balance to burn");
        balanceOf[msg.sender] -= _value;
        totalSupply -= _value;
        emit Burn(msg.sender, _value);
        emit Transfer(msg.sender, address(0), _value); // Emit transfer event for burning
        return true;
    }

    // Function to adjust supply based on external price feed
    function adjustSupply(uint256 currentPrice) public onlyOwner {
        // Logic to adjust supply based on the current price of Pi Coin
        // If the price is below the target, mint more coins
        // If the price is above the target, burn some coins
        if (currentPrice < TARGET_VALUE) {
            uint256 amountToMint = (TARGET_VALUE - currentPrice) / 10 ** 18; // Example calculation
            mint(owner, amountToMint); // Mint new coins to the owner
            emit SupplyAdjusted(totalSupply);
        } else if (currentPrice > TARGET_VALUE) {
            uint256 amountToBurn = (currentPrice - TARGET_VALUE) / 10 ** 18; // Example calculation
            burn(amountToBurn); // Burn coins from the owner
            emit SupplyAdjusted(totalSupply);
        }
    }

    // Function to get the current price of Pi Coin (placeholder)
    function getCurrentPrice() public view returns (uint256) {
        // This function should return the current market price of Pi Coin
        // In a real implementation, this could be fetched from an oracle
        return 0; // Placeholder value
    }
}
