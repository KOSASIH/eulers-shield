uint256 public constant INITIAL_SUPPLY = 100_000_000_000 * 10 ** 18; // Total supply with decimals
uint256 public constant STABLE_VALUE = 314159 * 10 ** 18; // Stable value in wei

// Multi-signature wallet addresses
address[] public multiSigWallets;
uint256 public requiredSignatures;

event SupplyAdjusted(uint256 newSupply);
event MultiSigWalletAdded(address wallet);
event MultiSigWalletRemoved(address wallet);

modifier onlyMultiSig() {
    require(isMultiSig(msg.sender), "Not authorized");
    _;
}

constructor() ERC20("Pi Coin", "Pi") {
    _mint(msg.sender, INITIAL_SUPPLY);
    multiSigWallets.push(msg.sender); // Add deployer as initial multi-sig wallet
    requiredSignatures = 2; // Set required signatures for multi-sig
}

function initialize(address[] memory _multiSigWallets, uint256 _requiredSignatures) public initializer {
    require(_multiSigWallets.length >= _requiredSignatures, "Not enough wallets");
    multiSigWallets = _multiSigWallets;
    requiredSignatures = _requiredSignatures;
}

function transfer(address recipient, uint256 amount) public override whenNotPaused returns (bool) {
    require(amount > 0, "Invalid transfer value");
    return super.transfer(recipient, amount);
}

function approve(address spender, uint256 amount) public override whenNotPaused returns (bool) {
    require(amount > 0, "Invalid approval value");
    return super.approve(spender, amount);
}

function adjustSupply(uint256 newSupply) external onlyMultiSig {
    require(newSupply > 0, "Invalid supply value");
    _mint(address(this), newSupply.sub(totalSupply()));
    emit SupplyAdjusted(newSupply);
}

function isMultiSig(address wallet) internal view returns (bool) {
    for (uint256 i = 0; i < multiSigWallets.length; i++) {
        if (multiSigWallets[i] == wallet) {
            return true;
        }
    }
    return false;
}

function addMultiSigWallet(address wallet) external onlyOwner {
    require(!isMultiSig(wallet), "Wallet already exists");
    multiSigWallets.push(wallet);
    emit MultiSigWalletAdded(wallet);
}

function removeMultiSigWallet(address wallet) external onlyOwner {
    require(isMultiSig(wallet), "Wallet does not exist");
    for (uint256 i = 0; i < multiSigWallets.length; i++) {
        if (multiSigWallets[i] == wallet) {
            multiSigWallets[i] = multiSigWallets[multiSigWallets.length - 1];
            multiSigWallets.pop();
            emit MultiSigWalletRemoved(wallet);
            break;
        }
    }
}

function pause() public onlyOwner {
    _pause();
}

function unpause() public onlyOwner {
    _unpause();
}

function renounceOwnership() public override onlyOwner {
    super.renounceOwnership();
}

function transferOwnership(address newOwner) public override onlyOwner {
    super.transferOwnership(newOwner);
}
