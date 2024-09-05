# blockchain.py

import hashlib
import time
import json
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend

class Block:
    def __init__(self, index, previous_hash, transactions, timestamp, nonce):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.timestamp = timestamp
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data_string = str(self.index) + self.previous_hash + str(self.transactions) + str(self.timestamp) + str(self.nonce)
        return hashlib.sha256(data_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []
        self.mining_reward = 10
        self.difficulty = 4
        self.target = "0" * self.difficulty

    def create_genesis_block(self):
        return Block(0, "0", [], int(time.time()), 0)

    def get_latest_block(self):
        return self.chain[-1]

    def add_transaction(self, sender, recipient, amount):
        self.pending_transactions.append({
            "sender": sender,
            "recipient": recipient,
            "amount": amount
        })

    def mine_pending_transactions(self, miner):
        if len(self.pending_transactions) < 1:
            return False

        new_block = Block(len(self.chain), self.get_latest_block().hash, self.pending_transactions, int(time.time()), 0)
        new_block.nonce = self.proof_of_work(new_block)
        self.chain.append(new_block)

        self.pending_transactions = [{"recipient": miner, "amount": self.mining_reward}]

        return True

    def proof_of_work(self, block):
        nonce = 0
        while self.validate_proof(block, nonce) is False:
            nonce += 1
        return nonce

    def validate_proof(self, block, nonce):
        data_string = str(block.index) + block.previous_hash + str(block.transactions) + str(block.timestamp) + str(nonce)
        hash = hashlib.sha256(data_string.encode()).hexdigest()
        return hash[:self.difficulty] == self.target

    def validate_chain(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True

    def get_balance_of_address(self, address):
        balance = 0
        for block in self.chain:
            for transaction in block.transactions:
                if transaction["recipient"] == address:
                    balance += transaction["amount"]
                elif transaction["sender"] == address:
                    balance -= transaction["amount"]
        return balance

class Wallet:
    def __init__(self):
        self.private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
        self.public_key = self.private_key.public_key()
        self.address = self.public_key.public_bytes(encoding=serialization.Encoding.OpenSSH, format=serialization.PublicFormat.OpenSSH).decode().replace("ssh-rsa ", "").replace("\n", "")

    def send_transaction(self, recipient, amount, blockchain):
        transaction = {
            "sender": self.address,
            "recipient": recipient,
            "amount": amount
        }
        blockchain.add_transaction(self.address, recipient, amount)

    def get_balance(self, blockchain):
        return blockchain.get_balance_of_address(self.address)

# Example usage:
blockchain = Blockchain()
wallet1 = Wallet()
wallet2 = Wallet()

wallet1.send_transaction(wallet2.address, 10, blockchain)
blockchain.mine_pending_transactions(wallet1.address)

print("Wallet 1 balance:", wallet1.get_balance(blockchain))
print("Wallet 2 balance:", wallet2.get_balance(blockchain))
