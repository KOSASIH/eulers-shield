import os
import time
import json
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()
INFURA_URL = os.getenv("INFURA_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
MODEL_REGISTRY_CONTRACT_ADDRESS = os.getenv("MODEL_REGISTRY_CONTRACT_ADDRESS")
MODEL_REGISTRY_ABI_PATH = os.getenv("MODEL_REGISTRY_ABI_PATH")

with open(MODEL_REGISTRY_ABI_PATH) as f:
    MODEL_REGISTRY_ABI = json.load(f)

web3 = Web3(Web3.HTTPProvider(INFURA_URL))
model_registry = web3.eth.contract(
    address=MODEL_REGISTRY_CONTRACT_ADDRESS, abi=MODEL_REGISTRY_ABI
)
account = web3.eth.account.from_key(PRIVATE_KEY)

def fetch_unverified_models():
    total = model_registry.functions.totalModels().call()
    unverified = []
    for i in range(1, total + 1):
        model = model_registry.functions.models(i).call()
        if not model[4]:
            unverified.append((i, model))
    return unverified

def verify_model(model_id, status=True):
    tx = model_registry.functions.verifyModel(model_id, status).build_transaction({
        'from': account.address,
        'nonce': web3.eth.get_transaction_count(account.address),
        'gas': 200_000,
        'gasPrice': web3.to_wei('30', 'gwei')
    })
    signed = web3.eth.account.sign_transaction(tx, private_key=account.key)
    tx_hash = web3.eth.send_raw_transaction(signed.rawTransaction)
    print(f"Model {model_id} verification status set to {status}: {web3.to_hex(tx_hash)}")

def main():
    while True:
        for model_id, model in fetch_unverified_models():
            # Add your AI/automated verification logic here (e.g., check IPFS hash, scan code, run tests)
            status = True  # Assume always valid for this example
            verify_model(model_id, status=status)
        time.sleep(600)

if __name__ == "__main__":
    main()
