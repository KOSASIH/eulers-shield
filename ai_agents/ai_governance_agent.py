import os
import time
from web3 import Web3
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configurations (fill with your real values)
INFURA_URL = os.getenv("INFURA_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
DAO_CONTRACT_ADDRESS = os.getenv("DAO_CONTRACT_ADDRESS")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Solidity ABI for the EulersShieldDAO contract (truncated for clarity, use full ABI in real use)
DAO_ABI = [
    # Add full ABI here
]

# Setup Web3
web3 = Web3(Web3.HTTPProvider(INFURA_URL))
account = web3.eth.account.from_key(PRIVATE_KEY)
dao = web3.eth.contract(address=DAO_CONTRACT_ADDRESS, abi=DAO_ABI)

# Setup OpenAI
openai = OpenAI(api_key=OPENAI_API_KEY)

def fetch_new_proposals():
    # You may want to use event logs for efficiency
    count = dao.functions.proposalCount().call()
    proposals = []
    for i in range(1, count + 1):
        prop = dao.functions.getProposal(i).call()
        if not prop[10]:  # aiEvaluated == False
            proposals.append((i, prop))
    return proposals

def analyze_proposal(title, description):
    prompt = (
        f"Review this DAO proposal.\n"
        f"Title: {title}\n"
        f"Description: {description}\n"
        f"Summarize the intent, point out risks, and recommend whether to accept or reject with rationale. "
        f"Flag as SPAM if malicious, else provide actionable suggestions."
    )
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    ai_summary = response.choices[0].message.content.strip()
    # Simple logic to extract recommendation
    rec = "reject" if "spam" in ai_summary.lower() or "reject" in ai_summary.lower() else "accept"
    return ai_summary, rec

def post_ai_summary(proposal_id, summary, recommendation):
    tx = dao.functions.postAISummary(proposal_id, summary, recommendation).build_transaction({
        'from': account.address,
        'nonce': web3.eth.get_transaction_count(account.address),
        'gas': 500_000,
        'gasPrice': web3.to_wei('30', 'gwei')
    })
    signed = web3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
    tx_hash = web3.eth.send_raw_transaction(signed.rawTransaction)
    print(f"Posted AI summary for proposal {proposal_id}: {web3.to_hex(tx_hash)}")

def main():
    while True:
        proposals = fetch_new_proposals()
        for pid, prop in proposals:
            print(f"Analyzing proposal {pid}: {prop[2]}")
            ai_summary, ai_rec = analyze_proposal(prop[2], prop[3])
            post_ai_summary(pid, ai_summary, ai_rec)
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    main()
