# pow.py

import hashlib
import time
import random

class ProofOfWork:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.target = self.calculate_target()

    def calculate_target(self):
        return "0" * self.difficulty

    def validate_proof(self, block, nonce):
        data_string = str(block.index) + block.previous_hash + str(block.transactions) + str(block.timestamp) + str(nonce)
        hash = hashlib.sha256(data_string.encode()).hexdigest()
        return hash[:self.difficulty] == self.target

    def find_proof(self, block):
        nonce = 0
        while True:
            if self.validate_proof(block, nonce):
                return nonce
            nonce += 1

    def mine(self, block):
        nonce = self.find_proof(block)
        block.nonce = nonce
        return block

    def get_difficulty(self):
        return self.difficulty

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
        self.target = self.calculate_target()
