# dg.py

import hashlib
import json
from ecdsa import SigningKey, VerifyingKey
from ecdsa.util import sigdecode_der
from ecdsa.numbertheory import inverse_mod
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend

class DecentralizedGovernance:
    def __init__(self, private_key, network_id):
        self.private_key = private_key
        self.network_id = network_id
        self.public_key = self.private_key.verifying_key
        self.blockchain = {}

    def generate_private_key(self):
        private_key = SigningKey.generate(curve=ec.SECP256k1)
        return private_key

    def get_private_key(self):
        return self.private_key

    def set_private_key(self, private_key):
        self.private_key = private_key
        self.public_key = self.private_key.verifying_key

    def get_public_key(self):
        return self.public_key

    def create_proposal(self, proposal_data):
        proposal_id = hashlib.sha256(json.dumps(proposal_data).encode()).hexdigest()
        proposal_data['id'] = proposal_id
        proposal_data['network_id'] = self.network_id
        return proposal_data

    def sign_proposal(self, proposal_data):
        signature = self.private_key.sign(json.dumps(proposal_data).encode())
        return signature

    def verify_signature(self, proposal_data, signature):
        try:
            self.public_key.verify(signature, json.dumps(proposal_data).encode())
            return True
        except:
            return False

    def add_proposal_to_blockchain(self, proposal_data):
        self.blockchain[proposal_data['id']] = proposal_data

    def get_proposal_from_blockchain(self, proposal_id):
        return self.blockchain.get(proposal_id)

    def vote_on_proposal(self, proposal_id, vote):
        proposal = self.get_proposal_from_blockchain(proposal_id)
        if proposal:
            proposal['votes'] = proposal.get('votes', []) + [vote]
            self.add_proposal_to_blockchain(proposal)

    def execute_proposal(self, proposal_id):
        proposal = self.get_proposal_from_blockchain(proposal_id)
        if proposal:
            # Execute the proposal logic here
            print(f'Proposal {proposal_id} executed successfully')

# Example usage:
dg = DecentralizedGovernance(private_key=DecentralizedGovernance().generate_private_key(), network_id='my_network')
proposal_data = {'title': 'My Proposal', 'description': 'This is my proposal'}
proposal = dg.create_proposal(proposal_data)
signature = dg.sign_proposal(proposal)
print(f'Proposal ID: {proposal["id"]}, Signature: {signature.hex()}')
dg.add_proposal_to_blockchain(proposal)
dg.vote_on_proposal(proposal['id'], 'yes')
dg.execute_proposal(proposal['id'])
