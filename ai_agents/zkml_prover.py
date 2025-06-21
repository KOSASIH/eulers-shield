import os
import json
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()
INFURA_URL = os.getenv("INFURA_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
ZKML_CONTRACT_ADDRESS = os.getenv("ZKML_CONTRACT_ADDRESS")
ZKML_ABI_PATH = os.getenv("ZKML_ABI_PATH")

with open(ZKML_ABI_PATH) as f:
    ZKML_ABI = json.load(f)

web3 = Web3(Web3.HTTPProvider(INFURA_URL))
account = web3.eth.account.from_key(PRIVATE_KEY)
zkml = web3.eth.contract(address=ZKML_CONTRACT_ADDRESS, abi=ZKML_ABI)

def post_zkml_proof(proof, public_signals, signal_hash, result):
    tx = zkml.functions.proveDecision(
        proof, public_signals, signal_hash, result
    ).build_transaction({
        'from': account.address,
        'nonce': web3.eth.get_transaction_count(account.address),
        'gas': 700_000,
        'gasPrice': web3.to_wei('30', 'gwei')
    })
    signed = web3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
    tx_hash = web3.eth.send_raw_transaction(signed.rawTransaction)
    print(f"ZKML proof posted: {web3.to_hex(tx_hash)}")

# Example usage after generating proof with snarkjs/zokrates/risczero
# post_zkml_proof(proof_bytes, public_signals_list, b"hash_of_input", True)
