# # fund.py

from web3 import Web3, HTTPProvider
from contract import PiCoinContract
from sf import StabilityFund

class FundManagement:
    def __init__(self, web3, pi_coin_contract_address, stability_fund_address):
        self.web3 = web3
        self.pi_coin_contract_address = pi_coin_contract_address
        self.stability_fund_address = stability_fund_address
        self.pi_coin_contract = PiCoinContract(web3, pi_coin_contract_address)
        self.stability_fund = StabilityFund(web3, stability_fund_address)

    def get_fund_balance(self):
        return self.stability_fund.get_stability_fund_balance()

    def get_fund_ratio(self):
        return self.stability_fund.get_stability_fund_ratio()

    def adjust_fund(self, target_ratio):
        self.stability_fund.adjust_stability_fund(target_ratio)

    def allocate_fund(self, recipient_address, amount):
        tx_hash = self.pi_coin_contract.functions().transfer(recipient_address, amount).transact({'from': self.stability_fund_address})
        return tx_hash

    def deallocate_fund(self, amount):
        tx_hash = self.pi_coin_contract.functions().transfer(self.stability_fund_address, amount).transact({'from': self.stability_fund_address})
        return tx_hash

    def get_fund_allocations(self):
        allocations = {}
        for address in self.pi_coin_contract.get_token_holders():
            balance = self.pi_coin_contract.functions().balanceOf(address).call()
            if balance > 0:
                allocations[address] = balance
        return allocations

    def rebalance_fund(self):
        allocations = self.get_fund_allocations()
        total_supply = self.pi_coin_contract.get_total_supply()
        for address, balance in allocations.items():
            ratio = balance / total_supply
            if ratio > 0.1:  # adjust this threshold as needed
                amount_to_deallocate = balance - (ratio * total_supply)
                self.deallocate_fund(amount_to_deallocate)
            elif ratio < 0.1:  # adjust this threshold as needed
                amount_to_allocate = (ratio * total_supply) - balance
                self.allocate_fund(address, amount_to_allocate)

from web3 import Web3, HTTPProvider
from contract import PiCoinContract
from sf import StabilityFund

class FundManagement:
    def __init__(self, web3, pi_coin_contract_address, stability_fund_address):
        self.web3 = web3
        self.pi_coin_contract_address = pi_coin_contract_address
        self.stability_fund_address = stability_fund_address
        self.pi_coin_contract = PiCoinContract(web3, pi_coin_contract_address)
        self.stability_fund = StabilityFund(web3, stability_fund_address)

    def get_fund_balance(self):
        return self.stability_fund.get_stability_fund_balance()

    def get_fund_ratio(self):
        return self.stability_fund.get_stability_fund_ratio()

    def adjust_fund(self, target_ratio):
        self.stability_fund.adjust_stability_fund(target_ratio)

    def allocate_fund(self, recipient_address, amount):
        tx_hash = self.pi_coin_contract.functions().transfer(recipient_address, amount).transact({'from': self.stability_fund_address})
        return tx_hash

    def deallocate_fund(self, amount):
        tx_hash = self.pi_coin_contract.functions().transfer(self.stability_fund_address, amount).transact({'from': self.stability_fund_address})
        return tx_hash

    def get_fund_allocations(self):
        allocations = {}
        for address in self.pi_coin_contract.get_token_holders():
            balance = self.pi_coin_contract.functions().balanceOf(address).call()
            if balance > 0:
                allocations[address] = balance
        return allocations

    def rebalance_fund(self):
        allocations = self.get_fund_allocations()
        total_supply = self.pi_coin_contract.get_total_supply()
        for address, balance in allocations.items():
            ratio = balance / total_supply
            if ratio > 0.1:  # adjust this threshold as needed
                amount_to_deallocate = balance - (ratio * total_supply)
                self.deallocate_fund(amount_to_deallocate)
            elif ratio < 0.1:  # adjust this threshold as needed
                amount_to_allocate = (ratio * total_supply) - balance
                self.allocate_fund(address, amount_to_allocate)
