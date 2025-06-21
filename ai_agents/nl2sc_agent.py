import os
import time
from web3 import Web3
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
INFURA_URL = os.getenv("INFURA_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
DAO_CONTRACT_ADDRESS = os.getenv("DAO_CONTRACT_ADDRESS")
DAO_ABI_PATH = os.getenv("DAO_ABI_PATH")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

import json
with open(DAO_ABI_PATH) as f:
    DAO_ABI = json.load(f)

web3 = Web3(Web3.HTTPProvider(INFURA_URL))
account = web3.eth.account.from_key(PRIVATE_KEY)
dao = web3.eth.contract(address=DAO_CONTRACT_ADDRESS, abi=DAO_ABI)
openai = OpenAI(api_key=OPENAI_API_KEY)

def listen_for_nl_proposals():
    # Assume proposals are submitted via a file or dApp frontend (for demo, read from proposals.txt)
    if not os.path.exists('nl_proposals.txt'):
        return []
    with open('nl_proposals.txt', 'r') as f:
        lines = f.readlines()
    return [line.strip() for line in lines if line.strip()]

def nl_to_contract_snippet(nl_text):
    prompt = (
        "Translate the following governance proposal into a secure Solidity function or upgrade snippet. "
        "Explain the logic after the code. Proposal:\n"
        f"{nl_text}\n"
    )
    resp = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return resp.choices[0].message.content.strip()

def submit_proposal(title, description):
    tx = dao.functions.createProposal(title, description).build_transaction({
        'from': account.address,
        'nonce': web3.eth.get_transaction_count(account.address),
        'gas': 600_000,
        'gasPrice': web3.to_wei('35', 'gwei')
    })
    signed = web3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
    tx_hash = web3.eth.send_raw_transaction(signed.rawTransaction)
    print(f"NL2SC proposal submitted: {web3.to_hex(tx_hash)}")

def main():
    while True:
        proposals = listen_for_nl_proposals()
        for nl_text in proposals:
            snippet = nl_to_contract_snippet(nl_text)
            submit_proposal(nl_text[:64], snippet)
        time.sleep(180)

if __name__ == "__main__":
    main()
