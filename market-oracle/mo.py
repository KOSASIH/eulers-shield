# mo.py

from web3 import Web3, HTTPProvider
from contract import PiCoinContract
from sf import StabilityFund
from fm import FundManagement
import requests

class MarketOracle:
    def __init__(self, web3, pi_coin_contract_address, stability_fund_address, fund_management_address):
        self.web3 = web3
        self.pi_coin_contract_address = pi_coin_contract_address
        self.stability_fund_address = stability_fund_address
        self.fund_management_address = fund_management_address
        self.pi_coin_contract = PiCoinContract(web3, pi_coin_contract_address)
        self.stability_fund = StabilityFund(web3, stability_fund_address)
        self.fund_management = FundManagement(web3, pi_coin_contract_address, stability_fund_address)

    def get_current_price(self):
        # fetch current price from external API (e.g. CoinGecko)
        response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=pi-coin&vs_currencies=usd')
        data = response.json()
        return data['pi-coin']['usd']

    def get_historical_prices(self, days):
        # fetch historical prices from external API (e.g. CoinGecko)
        response = requests.get(f'https://api.coingecko.com/api/v3/coins/pi-coin/market_chart?vs_currency=usd&days={days}')
        data = response.json()
        return data['prices']

    def calculate_market_cap(self):
        current_price = self.get_current_price()
        total_supply = self.pi_coin_contract.get_total_supply()
        return current_price * total_supply

    def calculate_fund_value(self):
        fund_balance = self.fund_management.get_fund_balance()
        current_price = self.get_current_price()
        return fund_balance * current_price

    def get_market_data(self):
        data = {
            'current_price': self.get_current_price(),
            'historical_prices': self.get_historical_prices(30),
            'market_cap': self.calculate_market_cap(),
            'fund_value': self.calculate_fund_value()
        }
        return data

    def update_stability_fund(self):
        market_data = self.get_market_data()
        target_ratio = 0.5  # adjust this target ratio as needed
        self.fund_management.adjust_fund(target_ratio)

    def update_fund_allocations(self):
        market_data = self.get_market_data()
        self.fund_management.rebalance_fund()
