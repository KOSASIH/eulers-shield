// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract PiCoin {
    string public name = "Pi Coin";
    string public symbol = "PI";
    uint8 public decimals = 18;
    uint256 public totalSupply;
    mapping(address => uint256) public balanceOf;

    address public owner;
    // Target value of Pi Coin in USD
    uint256 public constant TARGET_VALUE = 314159; // Target value of $314,159
    uint256 public constant MAX_SUPPLY = 100000000000 * 10 ** uint256(decimals); // Maximum supply of 100 billion Pi Coins

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Mint(address indexed to, uint256 value);
    event Burn(address indexed from, uint256 value);
    event SupplyAdjusted(uint256 newSupply);
    event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);

    modifier onlyOwner() {
        require(msg.sender == owner, "Not the contract owner");
        _;
    }

    modifier validAddress(address _address) {
        require(_address != address(0), "Invalid address");
        _;
    }

    constructor() {
        owner = msg.sender;
        totalSupply = MAX_SUPPLY; // Set total supply to maximum
        balanceOf[owner] = totalSupply; // Assign the total supply to the contract deployer
        emit Transfer(address(0), owner, totalSupply); // Emit transfer event for initial supply
    }

    function transfer(address _to, uint256 _value) public validAddress(_to) returns (bool success) {
        require(balanceOf[msg.sender] >= _value, "Insufficient balance");
        balanceOf[msg.sender] -= _value;
        balanceOf[_to] += _value;
        emit Transfer(msg.sender, _to, _value);
        return true;
    }

    // Mint new Pi Coins
    function mint(address _to, uint256 _value) public onlyOwner validAddress(_to) returns (bool success) {
        require(totalSupply + _value <= MAX_SUPPLY, "Minting exceeds max supply");
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
        // Logic to adjust supply based on the current price of Pi Coin in USD
        if (currentPrice < TARGET_VALUE) {
            uint256 amountToMint = (TARGET_VALUE - currentPrice); // Example calculation
            mint(owner, amountToMint); // Mint new coins to the owner
            emit SupplyAdjusted(totalSupply);
        } else if (currentPrice > TARGET_VALUE) {
            uint256 amountToBurn = (currentPrice - TARGET_VALUE); // Example calculation
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

    // Function to transfer ownership
    function transferOwnership(address newOwner) public onlyOwner validAddress(newOwner) {
        emit OwnershipTransferred(owner, newOwner);
        owner = newOwner;
    }
}
