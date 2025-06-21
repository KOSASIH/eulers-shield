import os
import time
import json
from web3 import Web3
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
INFURA_URL = os.getenv("INFURA_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
GRANT_CONTRACT_ADDRESS = os.getenv("GRANT_CONTRACT_ADDRESS")
GRANT_ABI_PATH = os.getenv("GRANT_ABI_PATH")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Load contract ABI
with open(GRANT_ABI_PATH) as f:
    GRANT_ABI = json.load(f)

# Set.HTTPProvider(INFURA3.eth.contract(address=GR, abi=GRI)
account = web3.eth.account.from_key(PRIVATE_KEY)
openai = OpenAI(api_key=OPENAI_API_KEY)

def fetch_pending_apps():
    total = grant.functions.totalApps().call()
    items = []
    for i in range(1, total + 1):
        app = grant.functions.applications(i).call()
        if not app[4]:  # aiReviewed == False
            items.append((i, app))
    return items

def ai_review_grant(project, requested):
    prompt = (
        "You are an AI DAO grant reviewer. Review the application for impact, feasibility, and fairness. "
        "Recommend an award (<= requested, up to 10 ETH max). "
        "Output JSON: {'review': ..., 'award': ...}.\n"
        f"Project: {project}\nRequested: {requested / 1e18} ETH"
    )
    resp = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.18,
    )
    return resp.choices[0].message.content.strip()

def post_ai_review(app_id, review_json):
    review = json.loads(review_json)
    award_wei = int(float(review["award"]) * 1e18)
    tx = grant.functions.aiReviewGrant(
        app_id,
        review["review"],
        award_wei
    ).build_transaction({
        'from': account.address,
        'nonce': web3.eth.get_transaction_count(account.address),
        'gas': 250_000,
        'gasPrice': web3.to_wei('30', 'gwei')
    })
    signed = web3.eth.account.sign_transaction(tx, private_key=account.key)
    tx_hash = web3.eth.send_raw_transaction(signed.rawTransaction)
    print(f"AI reviewed grant {app_id}: {web3.to_hex(tx_hash)}")

def main():
    while True:
        pending = fetch_pending_apps()
        for app_id, app in pending:
            review_json = ai_review_grant(app[1], app[2])
            post_ai_review(app_id, review_json)
        time.sleep(180)

if __name__ == "__main__":
    main()
