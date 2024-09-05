# pcsc.py

from web3 import Web3, HTTPProvider
from contract import PiCoinContract

class PiCoinSmartContract:
    def __init__(self, contract_address, provider_url):
        self.contract_address = contract_address
        self.provider_url = provider_url
        self.web3 = Web3(HTTPProvider(self.provider_url))
        self.contract = PiCoinContract(self.web3, self.contract_address)

    def get_balance(self, address):
        return self.contract.functions.balanceOf(address).call()

    def transfer(self, sender, recipient, amount):
        tx_hash = self.contract.functions.transfer(recipient, amount).transact({'from': sender})
        return tx_hash

    def approve(self, owner, spender, amount):
        tx_hash = self.contract.functions.approve(spender, amount).transact({'from': owner})
        return tx_hash

    def transfer_from(self, sender, recipient, amount):
        tx_hash = self.contract.functions.transferFrom(sender, recipient, amount).transact({'from': recipient})
        return tx_hash

    def get_allowance(self, owner, spender):
        return self.contract.functions.allowance(owner, spender).call()

    def increase_allowance(self, owner, spender, amount):
        tx_hash = self.contract.functions.increaseAllowance(spender, amount).transact({'from': owner})
        return tx_hash

    def decrease_allowance(self, owner, spender, amount):
        tx_hash = self.contract.functions.decreaseAllowance(spender, amount).transact({'from': owner})
        return tx_hash
