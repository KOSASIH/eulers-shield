# generate_market_data.py

import pandas as pd
import numpy as np

# Set the start and end dates
start_date = '2022-01-01'
end_date = '2022-12-31'

# Set the number of days
num_days = (pd.to_datetime(end_date) - pd.to_datetime(start_date)).days + 1

# Generate the dates
dates = pd.date_range(start=start_date, end=end_date, freq='D')

# Generate the market data
np.random.seed(42)
open_prices = np.random.uniform(100.0, 200.0, num_days)
high_prices = np.random.uniform(120.0, 220.0, num_days)
low_prices = np.random.uniform(80.0, 180.0, num_days)
close_prices = np.random.uniform(110.0, 210.0, num_days)
volumes = np.random.uniform(100000.0, 200000.0, num_days)
pi_coin_prices = np.random.uniform(3.14159, 3.14160, num_days)
bitcoin_prices = np.random.uniform(40000.0, 50000.0, num_days)
ethereum_prices = np.random.uniform(3000.0, 4000.0, num_days)
market_caps = np.random.uniform(1000000000.0, 2000000000.0, num_days)

# Create the DataFrame
df = pd.DataFrame({
    'Date': dates,
    'Open': open_prices,
    'High': high_prices,
    'Low': low_prices,
    'Close': close_prices,
    'Volume': volumes,
    'Pi Coin Price': pi_coin_prices,
    'Bitcoin Price': bitcoin_prices,
    'Ethereum Price': ethereum_prices,
    'Market Cap': market_caps
})

# Save the DataFrame to a CSV file
df.to_csv('market_data.csv', index=False)
