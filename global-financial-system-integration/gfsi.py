# gfsi.py

import hashlib
import json
from ecdsa import SigningKey, VerifyingKey
from ecdsa.util import sigdecode_der
from ecdsa.numbertheory import inverse_mod
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
import requests

class GlobalFinancialSystemIntegration:
    def __init__(self, private_key, network_id):
        self.private_key = private_key
        self.network_id = network_id
        self.public_key = self.private_key.verifying_key
        self.accounts = {}
        self.transactions = {}

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

    def create_account(self, account_holder, initial_balance):
        account_id = hashlib.sha256(json.dumps({'account_holder': account_holder}).encode()).hexdigest()
        account_data = {'id': account_id, 'account_holder': account_holder, 'balance': initial_balance}
        self.accounts[account_id] = account_data
        return account_data

    def get_account(self, account_id):
        return self.accounts.get(account_id)

    def create_transaction(self, sender_account_id, recipient_account_id, amount):
        transaction_id = hashlib.sha256(json.dumps({'sender_account_id': sender_account_id, 'recipient_account_id': recipient_account_id, 'amount': amount}).encode()).hexdigest()
        transaction_data = {'id': transaction_id, 'sender_account_id': sender_account_id, 'recipient_account_id': recipient_account_id, 'amount': amount}
        self.transactions[transaction_id] = transaction_data
        return transaction_data

    def sign_transaction(self, transaction_data):
        signature = self.private_key.sign(json.dumps(transaction_data).encode())
        return signature

    def verify_signature(self, transaction_data, signature):
        try:
            self.public_key.verify(signature, json.dumps(transaction_data).encode())
            return True
        except:
            return False

    def execute_transaction(self, transaction_data, signature):
        if self.verify_signature(transaction_data, signature):
            sender_account = self.get_account(transaction_data['sender_account_id'])
            recipient_account = self.get_account(transaction_data['recipient_account_id'])
            if sender_account and recipient_account:
                if sender_account['balance'] >= transaction_data['amount']:
                    sender_account['balance'] -= transaction_data['amount']
                    recipient_account['balance'] += transaction_data['amount']
                    print(f'Transaction {transaction_data["id"]} executed successfully')
                else:
                    print('Insufficient balance')
            else:
                print('Invalid account')
        else:
            print('Invalid signature')

    def integrate_with_external_system(self, external_system_url, transaction_data):
        response = requests.post(external_system_url, json=transaction_data)
        if response.status_code == 200:
            print(f'Transaction {transaction_data["id"]} integrated with external system successfully')
        else:
            print(f'Error integrating with external system: {response.text}')

# Example usage:
gfsi = GlobalFinancialSystemIntegration(private_key=GlobalFinancialSystemIntegration().generate_private_key(), network_id='my_network')
account1 = gfsi.create_account('Alice', 1000)
account2 = gfsi.create_account('Bob', 500)
transaction_data = gfsi.create_transaction(account1['id'], account2['id'], 200)
signature = gfsi.sign_transaction(transaction_data)
gfsi.execute_transaction(transaction_data, signature)
gfsi.integrate_with_external_system('https://example.com/external-system', transaction_data)
