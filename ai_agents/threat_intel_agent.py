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
THREAT_INTEL_CONTRACT_ADDRESS = os.getenv("THREAT_INTEL_CONTRACT_ADDRESS")
THREAT_INTEL_ABI_PATH = os.getenv("THREAT_INTEL_ABI_PATH")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Load contract ABI
with open(THREAT_INTEL_ABI_PATH) as f:
    THREAT_INTEL_ABI = json.load(f)

web3 = Web3(Web3.HTTPProvider(INFURA_URL))
threat_intel = web3.eth.contract(address=THREAT_INTEL_CONTRACT_ADDRESS, abi=THREAT_INTEL_ABI)
account = web3.eth.account.from_key(PRIVATE_KEY)
openai = OpenAI(api_key=OPENAI_API_KEY)

def fetch_unvalidated_threats():
    total = threat_intel.functions.totalThreats().call()
    pending = []
    for i in range(1, total + 1):
        threat = threat_intel.functions.threats(i).call()
        if not threat[6]:  # aiValidated == False
            pending.append((i, threat))
    return pending

def ai_assess_threat(target, description):
    prompt = (
        "You are an AI threat intelligence analyst. Assess the following threat, provide a concise risk assessment, "
        "and rate severity from 1 (Critical) to 5 (Low). Output JSON: {'assessment': ..., 'severity': ...}.\n"
        f"Target: {target}\nDescription: {description}"
    )
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.05,
    )
    return response.choices[0].message.content.strip()

def post_assessment(report_id, result_json):
    result = json.loads(result_json)
    severity = int(result["severity"])
    tx = threat_intel.functions.aiAssessThreat(
        report_id, result["assessment"], severity
    ).build_transaction({
        'from': account.address,
        'nonce': web3.eth.get_transaction_count(account.address),
        'gas': 200_000,
        'gasPrice': web3.to_wei('30', 'gwei')
    })
    signed = web3.eth.account.sign_transaction(tx, private_key=account.key)
    tx_hash = web3.eth.send_raw_transaction(signed.rawTransaction)
    print(f"AI assessed threat {report_id}: {web3.to_hex(tx_hash)}")

def main():
    while True:
        for report_id, threat in fetch_unvalidated_threats():
            result_json = ai_assess_threat(threat[1], threat[2])
            post_assessment(report_id, result_json)
        time.sleep(300)

if __name__ == "__main__":
    main()
