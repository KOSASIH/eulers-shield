# voting.py

import hashlib
import json
from ecdsa import SigningKey, VerifyingKey
from ecdsa.util import sigdecode_der
from ecdsa.numbertheory import inverse_mod
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend

class VotingSystem:
    def __init__(self, private_key, election_id):
        self.private_key = private_key
        self.election_id = election_id
        self.public_key = self.private_key.verifying_key
        self.ballots = {}

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

    def create_ballot(self, voter_id, candidate_id):
        ballot_id = hashlib.sha256(json.dumps({'voter_id': voter_id, 'candidate_id': candidate_id}).encode()).hexdigest()
        ballot_data = {'id': ballot_id, 'voter_id': voter_id, 'candidate_id': candidate_id, 'election_id': self.election_id}
        return ballot_data

    def sign_ballot(self, ballot_data):
        signature = self.private_key.sign(json.dumps(ballot_data).encode())
        return signature

    def verify_signature(self, ballot_data, signature):
        try:
            self.public_key.verify(signature, json.dumps(ballot_data).encode())
            return True
        except:
            return False

    def cast_ballot(self, ballot_data, signature):
        if self.verify_signature(ballot_data, signature):
            self.ballots[ballot_data['id']] = ballot_data
            print(f'Ballot {ballot_data["id"]} cast successfully')
        else:
            print('Invalid signature')

    def count_votes(self):
        vote_counts = {}
        for ballot in self.ballots.values():
            candidate_id = ballot['candidate_id']
            if candidate_id in vote_counts:
                vote_counts[candidate_id] += 1
            else:
                vote_counts[candidate_id] = 1
        return vote_counts

    def declare_winner(self):
        vote_counts = self.count_votes()
        winner = max(vote_counts, key=vote_counts.get)
        print(f'Candidate {winner} wins with {vote_counts[winner]} votes')

# Example usage:
voting_system = VotingSystem(private_key=VotingSystem().generate_private_key(), election_id='my_election')
voter_id = 'voter1'
candidate_id = 'candidateA'
ballot_data = voting_system.create_ballot(voter_id, candidate_id)
signature = voting_system.sign_ballot(ballot_data)
voting_system.cast_ballot(ballot_data, signature)
voting_system.declare_winner()
