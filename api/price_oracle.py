# api/price_oracle.py

import requests

class PriceOracle:
    def __init__(self):
        self.api_url = "https://api.coingecko.com/api/v3/simple/price"

    def get_price(self, coin_id):
        try:
            response = requests.get(f"{self.api_url}?ids={coin_id}&vs_currencies=usd")
            response.raise_for_status()
            data = response.json()
            return data[coin_id]['usd']
        except Exception as e:
            print(f"Error fetching price data: {e}")
            return None
