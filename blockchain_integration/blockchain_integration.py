from web3 import Web3

class BlockchainIntegration:
    def __init__(self, provider_url):
        """Initialize the blockchain connection."""
        self.web3 = Web3(Web3.HTTPProvider(provider_url))
        if not self.web3.isConnected():
            raise Exception("Failed to connect to the blockchain.")

    def deploy_contract(self, contract_abi, contract_bytecode):
        """Deploy a smart contract to the blockchain."""
        contract = self.web3.eth.contract(abi=contract_abi, bytecode=contract_bytecode)
        tx_hash = contract.constructor().transact()
        tx_receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)
        return tx_receipt.contractAddress

    def call_contract_function(self, contract_address, function_name, *args):
        """Call a function of a deployed smart contract."""
        contract = self.web3.eth.contract(address=contract_address, abi=contract_abi)
        return getattr(contract.functions, function_name)(*args).call()

    def send_transaction(self, from_address, to_address, value):
        """Send a transaction on the blockchain."""
        tx = {
            'from': from_address,
            'to': to_address,
            'value': self.web3.toWei(value, 'ether'),
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei'),
            'nonce': self.web3.eth.getTransactionCount(from_address),
        }
        signed_tx = self.web3.eth.account.signTransaction(tx, private_key='YOUR_PRIVATE_KEY')
        tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        return self.web3.toHex(tx_hash)

# Example Usage
if __name__ == "__main__":
    blockchain = BlockchainIntegration('https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID')
    print("Connected to blockchain:", blockchain.web3.isConnected())
