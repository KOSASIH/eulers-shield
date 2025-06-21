import os
import time
import json
from web3 import Web3
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
INFURA_URL = os.getenv("INFURA_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
BOUNTY_CONTRACT_ADDRESS = os.getenv("BOUNTY_CONTRACT_ADDRESS")
BOUNTY_ABI_PATH = os.getenv("BOUNTY_ABI_PATH")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

with open(BOUNTY_ABI_PATH) as f:
    BOUNTY_ABI = json.load(f)

web3 = Web3(Web3.HTTPProvider(INFURA_URL))
bounty = web3.eth.contract(address=BOUNTY_CONTRACT_ADDRESS, abi=BOUNTY_ABI)
account = web3.eth.account.from_key(PRIVATE_KEY)
openai = OpenAI(api_key=OPENAI_API_KEY)

def fetch_pending_reports():
    total = bounty.functions.totalReports().call()
    items = []
    for i in range(1, total+1):
        report = bounty.functions.reports(i).call()
        if not report[5]:  # aiEvaluated == False
            items.append((i, report))
    return items

def ai_assess_bug(description):
    prompt = (
        "You are an AI security expert. Analyze the following bug report. "
        "Summarize severity, impact, and recommend a reward (ETH, up to 1 ETH for critical). "
        "Output JSON: {'assessment': ..., 'reward': ...}. Bug report:\n"
        f"{description}"
    )
    resp = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return resp.choices[0].message.content.strip()

def post_ai_assessment(report_id, assessment_json):
    assessment = json.loads(assessment_json)
    reward_wei = int(float(assessment["reward"]) * 1e18)
    tx = bounty.functions.aiEvaluateBug(
        report_id,
        assessment["assessment"],
        reward_wei
    ).build_transaction({
        'from': account.address,
        'nonce': web3.eth.get_transaction_count(account.address),
        'gas': 250_000,
        'gasPrice': web3.to_wei('30', 'gwei')
    })
    signed = web3.eth.account.sign_transaction(tx, private_key=account.key)
    tx_hash = web3.eth.send_raw_transaction(signed.rawTransaction)
    print(f"AI assessed bug {report_id}: {web3.to_hex(tx_hash)}")

def main():
    while True:
        pending = fetch_pending_reports()
        for report_id, report in pending:
            assessment_json = ai_assess_bug(report[1])
            post_ai_assessment(report_id, assessment_json)
        time.sleep(180)

if __name__ == "__main__":
    main()
