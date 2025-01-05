from web3 import Web3
import json
import os

class SmartContractManager:
    def __init__(self, provider_url, contract_storage_file='contracts.json'):
        self.web3 = Web3(Web3.HTTPProvider(provider_url))
        self.contract_storage_file = contract_storage_file
        self.contracts = {}
        self.load_contracts()

    def load_contracts(self):
        """Load deployed contracts from a JSON file."""
        if os.path.exists(self.contract_storage_file):
            with open(self.contract_storage_file, 'r') as file:
                self.contracts = json.load(file)

    def save_contracts(self):
        """Save deployed contracts to a JSON file."""
        with open(self.contract_storage_file, 'w') as file:
            json.dump(self.contracts, file)

    def deploy_contract(self, contract_source, constructor_args=None):
        """Deploy a new smart contract."""
        # Compile the contract
        compiled_contract = self.compile_contract(contract_source)
        contract = self.web3.eth.contract(abi=compiled_contract['abi'], bytecode=compiled_contract['bin'])

        # Get the account to deploy the contract
        account = self.web3.eth.accounts[0]
        transaction = contract.constructor(*constructor_args).buildTransaction({
            'from': account,
            'nonce': self.web3.eth.getTransactionCount(account),
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei')
        })

        # Sign and send the transaction
        signed_txn = self.web3.eth.account.signTransaction(transaction, private_key=os.getenv('PRIVATE_KEY'))
        tx_hash = self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)

        # Wait for the transaction to be mined
        tx_receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)

        # Store the contract address
        contract_address = tx_receipt.contractAddress
        self.contracts[contract_address] = {
            'abi': compiled_contract['abi'],
            'source': contract_source
        }
        self.save_contracts()
        return f"Contract deployed at address: {contract_address}"

    def compile_contract(self, contract_source):
        """Compile the smart contract source code."""
        from solcx import compile_source

        compiled = compile_source(contract_source)
        contract_id, contract_interface = compiled.popitem()
        return contract_interface

    def interact_with_contract(self, contract_address, method_name, *args):
        """Interact with a deployed smart contract."""
        if contract_address not in self.contracts:
            return "Contract not found."

        contract_abi = self.contracts[contract_address]['abi']
        contract = self.web3.eth.contract(address=contract_address, abi=contract_abi)

        # Call the specified method
        method = getattr(contract.functions, method_name)
        return method(*args).call()

# Example usage
if __name__ == "__main__":
    provider_url = "https://your.ethereum.node"  # Replace with your Ethereum node URL
    manager = SmartContractManager(provider_url)

    # Example contract source code (simple storage contract)
    contract_source = '''
    pragma solidity ^0.8.0;

    contract SimpleStorage {
        uint256 storedData;

        function set(uint256 x) public {
            storedData = x;
        }

        function get() public view returns (uint256) {
            return storedData;
        }
    }
    '''

    # Deploy the contract
    print(manager.deploy_contract(contract_source, []))

    # Interact with the deployed contract
    contract_address = list(manager.contracts.keys())[0]  # Get the first deployed contract address
    print(manager.interact_with_contract(contract_address, 'get'))  # Call the 'get' method
