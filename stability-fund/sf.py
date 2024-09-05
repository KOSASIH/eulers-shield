# sf.py

from web3 import Web3, HTTPProvider
from contract import PiCoinContract

class StabilityFund:
    def __init__(self, web3, contract_address):
        self.web3 = web3
        self.contract_address = contract_address
        self.pi_coin_contract = PiCoinContract(web3, contract_address)

    def get_balance(self, address):
        return self.pi_coin_contract.functions().balanceOf(address).call()

    def get_total_supply(self):
        return self.pi_coin_contract.get_total_supply()

    def get_stability_fund_balance(self):
        return self.get_balance(self.contract_address)

    def deposit(self, amount):
        tx_hash = self.pi_coin_contract.functions().transfer(self.contract_address, amount).transact({'from': self.pi_coin_contract.get_owner()})
        return tx_hash

    def withdraw(self, amount):
        tx_hash = self.pi_coin_contract.functions().transfer(self.pi_coin_contract.get_owner(), amount).transact({'from': self.pi_coin_contract.get_owner()})
        return tx_hash

    def get_stability_fund_ratio(self):
        total_supply = self.get_total_supply()
        stability_fund_balance = self.get_stability_fund_balance()
        return stability_fund_balance / total_supply

    def adjust_stability_fund(self, target_ratio):
        current_ratio = self.get_stability_fund_ratio()
        if current_ratio < target_ratio:
            amount_to_deposit = (target_ratio - current_ratio) * self.get_total_supply()
            self.deposit(amount_to_deposit)
        elif current_ratio > target_ratio:
            amount_to_withdraw = (current_ratio - target_ratio) * self.get_total_supply()
            self.withdraw(amount_to_withdraw)

    def get_stability_fund_address(self):
        return self.contract_address
