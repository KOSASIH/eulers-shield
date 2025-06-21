import os
import time
import json
from web3 import Web3
from openai import OpenAI
from dotenv import load_dotenv

# -- Load environment
load_dotenv()
INFURA_URL = os.getenv("INFURA_URL")
USER_ADDRESS = os.getenv("USER_ADDRESS")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
DAO_CONTRACT_ADDRESS = os.getenv("DAO_CONTRACT_ADDRESS")
DAO_ABI_PATH = os.getenv("DAO_ABI_PATH")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# -- Load ABI
with open(DAO_ABI_PATH) as f:
    DAO_ABI = json.load(f)

web3 = Web3(Web3.HTTPProvider(INFURA_URL))
openai = OpenAI(api_key=OPENAI_API_KEY)
dao = web3.eth.contract(address=DAO_CONTRACT_ADDRESS, abi=DAO_ABI)
account = web3.eth.account.from_key(PRIVATE_KEY)

def get_wallet_activity():
    latest = web3.eth.block_number
    txs = []
    for i in range(latest-10, latest+1):
        block = web3.eth.get_block(i, full_transactions=True)
        for tx in block.transactions:
            if tx['from'].lower() == USER_ADDRESS.lower() or (tx['to'] and tx['to'].lower() == USER_ADDRESS.lower()):
                txs.append(tx)
    return txs

def analyze_activity(txs):
    activities = []
    for tx in txs:
        prompt = (
            f"Analyze this wallet transaction for risk, compliance, and opportunity:\n"
            f"From: {tx['from']}, To: {tx['to']}, Value: {tx['value']}, Data: {tx['input']}"
        )
        resp = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        activities.append({'tx': tx, 'analysis': resp.choices[0].message.content.strip()})
    return activities

def auto_vote_on_dao(proposal_id, vote=True):
    tx = dao.functions.vote(proposal_id, vote).build_transaction({
        'from': account.address,
        'nonce': web3.eth.get_transaction_count(account.address),
        'gas': 200_000,
        'gasPrice': web3.to_wei('30', 'gwei'),
    })
    signed = web3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
    tx_hash = web3.eth.send_raw_transaction(signed.rawTransaction)
    print(f"Auto-voted on proposal {proposal_id}: {web3.to_hex(tx_hash)}")

def main():
    while True:
        txs = get_wallet_activity()
        analyses = analyze_activity(txs)
        for a in analyses:
            print("Transaction analysis:", a['analysis'])
            # Example: If AI flags "urgent risk", you could flag, alert, or even auto-interact with DAO
            if "urgent risk" in a['analysis'].lower():
                print("[ALERT] Urgent risk detected in wallet activity.")
        time.sleep(300)  # Run every 5 minutes

if __name__ == "__main__":
    main()
