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

    def get_total_supply(self):
        return self.contract.functions.totalSupply().call()

    def get_owner(self):
        return self.contract.functions.owner().call()

    def renounce_ownership(self):
        tx_hash = self.contract.functions.renounceOwnership().transact({'from': self.get_owner()})
        return tx_hash

    def transfer_ownership(self, new_owner):
        tx_hash = self.contract.functions.transferOwnership(new_owner).transact({'from': self.get_owner()})
        return tx_hash

    def pause(self):
        tx_hash = self.contract.functions.pause().transact({'from': self.get_owner()})
        return tx_hash

    def unpause(self):
        tx_hash = self.contract.functions.unpause().transact({'from': self.get_owner()})
        return tx_hash

    def is_paused(self):
        return self.contract.functions.paused().call()

    def get_name(self):
        return self.contract.functions.name().call()

    def get_symbol(self):
        return self.contract.functions.symbol().call()

    def get_decimals(self):
        return self.contract.functions.decimals().call()
