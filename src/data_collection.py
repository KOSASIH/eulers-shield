import requests
import time

class MarketDataCollector:
    def __init__(self, api_url):
        self.api_url = api_url

    def get_price(self, coin_id):
        """
        Fetch the current price of the specified cryptocurrency.
        
        :param coin_id: The ID of the cryptocurrency (e.g., 'bitcoin', 'ethereum').
        :return: Current price in USD or None if an error occurs.
        """
        try:
            response = requests.get(f"{self.api_url}/simple/price?ids={coin_id}&vs_currencies=usd")
            response.raise_for_status()  # Raise an error for bad responses
            data = response.json()
            return data[coin_id]['usd']
        except Exception as e:
            print(f"Error fetching price data: {e}")
            return None

    def get_market_data(self, coin_id):
        """
        Fetch comprehensive market data for the specified cryptocurrency.
        
        :param coin_id: The ID of the cryptocurrency.
        :return: A dictionary containing market data or None if an error occurs.
        """
        try:
            response = requests.get(f"{self.api_url}/coins/markets?vs_currency=usd&ids={coin_id}")
            response.raise_for_status()
            data = response.json()
            if data:
                return {
                    'id': data[0]['id'],
                    'current_price': data[0]['current_price'],
                    'market_cap': data[0]['market_cap'],
                    'total_volume': data[0]['total_volume'],
                    'price_change_percentage_24h': data[0]['price_change_percentage_24h'],
                }
            else:
                return None
        except Exception as e:
            print(f"Error fetching market data: {e}")
            return None

    def collect_data_periodically(self, coin_id, interval):
        """
        Collect market data periodically.
        
        :param coin_id: The ID of the cryptocurrency.
        :param interval: Time interval in seconds for data collection.
        """
        while True:
            market_data = self.get_market_data(coin_id)
            if market_data:
                print(f"Market Data for {coin_id}: {market_data}")
            time.sleep(interval)

if __name__ == "__main__":
    # Example usage
    api_url = "https://api.coingecko.com/api/v3"  # CoinGecko API URL
    collector = MarketDataCollector(api_url)
    
    # Collect data for Pi Coin (replace 'pi-coin' with the actual ID if available)
    coin_id = "pi-coin"  # Example coin ID
    collector.collect_data_periodically(coin_id, 60)  # Collect data every 60 seconds
