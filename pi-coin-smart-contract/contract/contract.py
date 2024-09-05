# contract.py

from solc import compile_source
from web3 import Web3, HTTPProvider

class PiCoinContract:
    def __init__(self, web3, contract_address):
        self.web3 = web3
        self.contract_address = contract_address
        self.contract_interface = self.compile_contract()

    def compile_contract(self):
        with open('PiCoin.sol', 'r') as f:
            contract_source = f.read()
        compiled_contract = compile_source(contract_source, 'PiCoin')
        contract_interface = compiled_contract['<stdin>:PiCoin']
        return contract_interface

    def deploy_contract(self):
        tx_hash = self.web3.eth.contract(abi=self.contract_interface['abi'], bytecode=self.contract_interface['bin']).constructor().transact()
        return tx_hash

    def functions(self):
        return self.contract_interface['functions']

    def get_contract_address(self):
        return self.contract_address

    def get_abi(self):
        return self.contract_interface['abi']

    def get_bytecode(self):
        return self.contract_interface['bin']

    def get_owner(self):
        return self.functions().owner().call()

    def get_total_supply(self):
        return self.functions().totalSupply().call()

    def get_name(self):
        return self.functions().name().call()

    def get_symbol(self):
        return self.functions().symbol().call()

    def get_decimals(self):
        return self.functions().decimals().call()

    def is_paused(self):
        return self.functions().paused().call()

    def pause(self):
        tx_hash = self.functions().pause().transact({'from': self.get_owner()})
        return tx_hash

    def unpause(self):
        tx_hash = self.functions().unpause().transact({'from': self.get_owner()})
        return tx_hash

    def renounce_ownership(self):
        tx_hash = self.functions().renounceOwnership().transact({'from': self.get_owner()})
        return tx_hash

    def transfer_ownership(self, new_owner):
        tx_hash = self.functions().transferOwnership(new_owner).transact({'from': self.get_owner()})
        return tx_hash
