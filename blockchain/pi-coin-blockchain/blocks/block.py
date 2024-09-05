# block.py

import hashlib
import time
import json
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend

class Block:
    def __init__(self, index, previous_hash, transactions, timestamp, nonce, miner, block_reward):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.timestamp = timestamp
        self.nonce = nonce
        self.miner = miner
        self.block_reward = block_reward
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data_string = str(self.index) + self.previous_hash + str(self.transactions) + str(self.timestamp) + str(self.nonce) + self.miner + str(self.block_reward)
        return hashlib.sha256(data_string.encode()).hexdigest()

    def __str__(self):
        return json.dumps(self.__dict__, sort_keys=True, indent=4)

    def to_json(self):
        return self.__str__()

    def from_json(json_string):
        data = json.loads(json_string)
        return Block(data['index'], data['previous_hash'], data['transactions'], data['timestamp'], data['nonce'], data['miner'], data['block_reward'])

    def get_transaction_count(self):
        return len(self.transactions)

    def get_transaction(self, index):
        return self.transactions[index]

    def add_transaction(self, transaction):
        self.transactions.append(transaction)
        self.hash = self.calculate_hash()

    def remove_transaction(self, transaction):
        self.transactions.remove(transaction)
        self.hash = self.calculate_hash()

    def get_miner(self):
        return self.miner

    def get_block_reward(self):
        return self.block_reward

    def get_nonce(self):
        return self.nonce

    def set_nonce(self, nonce):
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def get_timestamp(self):
        return self.timestamp

    def get_previous_hash(self):
        return self.previous_hash

    def get_index(self):
        return self.index

    def get_hash(self):
        return self.hash

    def is_valid(self, previous_block):
        if self.index != previous_block.index + 1:
            return False
        if self.previous_hash != previous_block.hash:
            return False
        if not self.validate_transactions():
            return False
        return True

    def validate_transactions(self):
        for transaction in self.transactions:
            if not transaction.is_valid():
                return False
        return True

    def __eq__(self, other):
        return self.hash == other.hash

    def __lt__(self, other):
        return self.index < other.index

    def __gt__(self, other):
        return self.index > other.index

    def __le__(self, other):
        return self.index <= other.index

    def __ge__(self, other):
        return self.index >= other.index
