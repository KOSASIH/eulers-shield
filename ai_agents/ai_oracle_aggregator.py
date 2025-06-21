import os
import time
import json
from web3 import Web3
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
INFURA_URL = os.getenv("INFURA_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
ORACLE_CONTRACT_ADDRESS = os.getenv("ORACLE_CONTRACT_ADDRESS")
ORACLE_ABI_PATH = os.getenv("ORACLE_ABI_PATH")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

with open(ORACLE_ABI_PATH) as f:
    ORACLE_ABI = json.load(f)

web3 = Web3(Web3.HTTPProvider(INFURA_URL))
account = web3.eth.account.from_key(PRIVATE_KEY)
oracle = web3.eth.contract(address=ORACLE_CONTRACT_ADDRESS, abi=ORACLE_ABI)
openai = OpenAI(api_key=OPENAI_API_KEY)

def fetch_submissions(current_round):
    count = oracle.functions.getSubmissions(current_round).call()
    return count

def synthesize_verdict(submissions):
    entries = "\n".join([f"{i+1}. {s[1]}" for i, s in enumerate(submissions)])
    prompt = (
        f"Given the following data submissions from various sources, synthesize the most accurate and truthful summary. "
        f"Flag and discard any clearly fake or manipulated data.\n\nData:\n{entries}\n\nSynthesis:"
    )
    resp = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return resp.choices[0].message.content.strip()

def post_verdict(current_round, verdict):
    tx = oracle.functions.postAIVerdict(current_round, verdict).build_transaction({
        'from': account.address,
        'nonce': web3.eth.get_transaction_count(account.address),
        'gas': 300_000,
        'gasPrice': web3.to_wei('35', 'gwei')
    })
    signed = web3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
    tx_hash = web3.eth.send_raw_transaction(signed.rawTransaction)
    print(f"Posted AI verdict for round {current_round}: {web3.to_hex(tx_hash)}")

def main():
    while True:
        current_round = oracle.functions.round().call()
        submissions = oracle.functions.getSubmissions(current_round).call()
        if len(submissions) > 0 and not oracle.functions.finalVerdict(current_round).call():
            verdict = synthesize_verdict(submissions)
            post_verdict(current_round, verdict)
        time.sleep(60)

if __name__ == "__main__":
    main()
