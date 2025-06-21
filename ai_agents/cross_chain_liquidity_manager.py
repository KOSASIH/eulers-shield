import os
import time
import json
from web3 import Web3
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
ETH_INFURA = os.getenv("ETH_INFURA_URL")
BSC_RPC = os.getenv("BSC_RPC_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Add additional chains as needed

# Setup Web3 for Ethereum and BSC
w3_eth = Web3(Web3.HTTPProvider(ETH_INFURA))
w3_bsc = Web3(Web3.HTTPProvider(BSC_RPC))
openai = OpenAI(api_key=OPENAI_API_KEY)

def fetch_balances(address):
    eth_balance = w3_eth.eth.get_balance(address)
    bsc_balance = w3_bsc.eth.get_balance(address)
    return {
        "eth": w3_eth.from_wei(eth_balance, "ether"),
        "bsc": w3_bsc.from_wei(bsc_balance, "ether"),
    }

def fetch_prices():
    # For real deployment, integrate with on-chain oracles or use trusted APIs
    # Here, mock data is used
    return {
        "eth_usd": 3500,
        "bsc_usd": 600,
    }

def ai_liquidity_strategy(balances, prices):
    prompt = (
        f"Given these cross-chain balances: {balances} and market prices: {prices}, "
        "devise the optimal arbitrage or liquidity move to maximize total protocol value. "
        "Output a JSON with 'action', 'from_chain', 'to_chain', 'amount', and 'reason'."
    )
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
    )
    return response.choices[0].message.content.strip()

def execute_transfer(chain, from_account, to_address, amount):
    # This is a placeholder. Integrate with bridges (e.g., LayerZero, Axelar, Wormhole) for real cross-chain swaps.
    print(f"Would transfer {amount} ETH from {from_account.address} to {to_address} on {chain}")

def main():
    address = w3_eth.eth.account.from_key(PRIVATE_KEY).address
    while True:
        balances = fetch_balances(address)
        prices = fetch_prices()
        strategy_json = ai_liquidity_strategy(balances, prices)
        try:
            strategy = json.loads(strategy_json)
            print("AI Strategy:", strategy)
            if strategy["action"] == "swap" and strategy["amount"] > 0:
                execute_transfer(
                    strategy["from_chain"],
                    w3_eth.eth.account.from_key(PRIVATE_KEY) if strategy["from_chain"] == "eth" else w3_bsc.eth.account.from_key(PRIVATE_KEY),
                    address,  # For simplicity, self-transfer; use bridge address in production
                    strategy["amount"]
                )
        except Exception as e:
            print("Error parsing AI response:", e)
        time.sleep(60 * 30)  # Run every 30 minutes

if __name__ == "__main__":
    main()
