// PiCoin.sol

pragma solidity ^0.8.0;

import "https://github.com/OpenZeppelin/openzeppelin-solidity/contracts/ownership/Ownable.sol";
import "https://github.com/OpenZeppelin/openzeppelin-solidity/contracts/lifecycle/Pausable.sol";

contract PiCoin is Ownable, Pausable {
    string public name = "Pi Coin";
    string public symbol = "π";
    uint8 public decimals = 18;

    uint256 public totalSupply;

    mapping (address => uint256) public balances;
    mapping (address => mapping (address => uint256)) public allowed;

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);

    constructor() public {
        totalSupply = 100000000 * (10 ** decimals);
        balances[msg.sender] = totalSupply;
    }

    function transfer(address _to, uint256 _value) public whenNotPaused returns (bool) {
        require(_to != address(0), "Invalid recipient address");
        require(_value > 0, "Invalid transfer value");
        require(balances[msg.sender] >= _value, "Insufficient balance");

        balances[msg.sender] -= _value;
        balances[_to] += _value;

        emit Transfer(msg.sender, _to, _value);
        return true;
    }

    function approve(address _spender, uint256 _value) public whenNotPaused returns (bool) {
        require(_spender != address(0), "Invalid spender address");
        require(_value > 0, "Invalid approval value");

        allowed[msg.sender][_spender] = _value;

        emit Approval(msg.sender, _spender, _value);
        return true;
    }

    function transferFrom(address _from, address _to, uint256 _value) public whenNotPaused returns (bool) {
        require(_from != address(0), "Invalid sender address");
        require(_to != address(0), "Invalid recipient address");
        require(_value > 0, "Invalid transfer value");
        require(balances[_from] >= _value, "Insufficient balance");
        require(allowed[_from][msg.sender] >= _value, "Insufficient allowance");

        balances[_from] -= _value;
        balances[_to] += _value;
        allowed[_from][msg.sender] -= _value;

        emit Transfer(_from, _to, _value);
        return true;
    }

    function increaseAllowance(address _spender, uint256 _addedValue) public whenNotPaused returns (bool) {
        require(_spender != address(0), "Invalid spender address");
        require(_addedValue > 0, "Invalid increase value");

        allowed[msg.sender][_spender] += _addedValue;

        emit Approval(msg.sender, _spender, allowed[msg.sender][_spender]);
        return true;
    }

    function decreaseAllowance(address _spender, uint256 _subtractedValue) public whenNotPaused returns (bool) {
        require(_spender != address(0), "Invalid spender address");
        require(_subtractedValue > 0, "Invalid decrease value");
        require(allowed[msg.sender][_spender] >= _subtractedValue, "Insufficient allowance");

        allowed[msg.sender][_spender] -= _subtractedValue;

        emit Approval(msg.sender, _spender, allowed[msg.sender][_spender]);
        return true;
    }

    function pause() public onlyOwner {
        super.pause();
    }

    function unpause() public onlyOwner {
        super.unpause();
    }

    function renounceOwnership() public onlyOwner {
        super.renounceOwnership();
    }

    function transferOwnership(address newOwner) public onlyOwner {
        super.transferOwnership(newOwner);
    }
}
