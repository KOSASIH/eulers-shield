import os
import time
from web3 import Web3
from openai import OpenAI
from dotenv import load_dotenv

# Load env vars
load_dotenv()
INFURA_URL = os.getenv("INFURA_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
DAO_CONTRACT_ADDRESS = os.getenv("DAO_CONTRACT_ADDRESS")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DAO_ABI_PATH = os.getenv("DAO_ABI_PATH")

import json
with open(DAO_ABI_PATH) as f:
    DAO_ABI = json.load(f)

web3 = Web3(Web3.HTTPProvider(INFURA_URL))
account = web3.eth.account.from_key(PRIVATE_KEY)
dao = web3.eth.contract(address=DAO_CONTRACT_ADDRESS, abi=DAO_ABI)
openai = OpenAI(api_key=OPENAI_API_KEY)

def get_recent_transactions():
    # Scan for suspicious contract calls (mockup, integrate with block explorer APIs for scale)
    latest = web3.eth.block_number
    txs = []
    for i in range(latest-5, latest+1):
        block = web3.eth.get_block(i, full_transactions=True)
        for tx in block.transactions:
            if tx.to == DAO_CONTRACT_ADDRESS:
                txs.append(tx)
    return txs

def analyze_transactions(txs):
    threat_list = []
    for tx in txs:
        prompt = (
            f"Analyze this Ethereum transaction for malicious or anomalous behavior: "
            f"From: {tx['from']}, To: {tx['to']}, Data: {tx['input']}, Value: {tx['value']}"
        )
        resp = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        analysis = resp.choices[0].message.content.strip()
        if "malicious" in analysis.lower() or "attack" in analysis.lower():
            threat_list.append((tx, analysis))
    return threat_list

def post_threat_alert(threat):
    print("Threat detected:", threat)
    # Optionally submit a DAO proposal or notify admins

def main():
    while True:
        txs = get_recent_transactions()
        threats = analyze_transactions(txs)
        for tx, analysis in threats:
            post_threat_alert((tx, analysis))
        time.sleep(120)

if __name__ == "__main__":
    main()
