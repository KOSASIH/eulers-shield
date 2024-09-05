# api.py

from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from gfsi import GlobalFinancialSystemIntegration

app = Flask(__name__)
api = Api(app)

gfsi = GlobalFinancialSystemIntegration(private_key=GlobalFinancialSystemIntegration().generate_private_key(), network_id='my_network')

class Account(Resource):
    def post(self):
        account_holder = request.json['account_holder']
        initial_balance = request.json['initial_balance']
        account_data = gfsi.create_account(account_holder, initial_balance)
        return jsonify(account_data)

    def get(self, account_id):
        account_data = gfsi.get_account(account_id)
        if account_data:
            return jsonify(account_data)
        else:
            return jsonify({'error': 'Account not found'}), 404

class Transaction(Resource):
    def post(self):
        sender_account_id = request.json['sender_account_id']
        recipient_account_id = request.json['recipient_account_id']
        amount = request.json['amount']
        transaction_data = gfsi.create_transaction(sender_account_id, recipient_account_id, amount)
        signature = gfsi.sign_transaction(transaction_data)
        return jsonify({'transaction_id': transaction_data['id'], 'signature': signature.hex()})

    def put(self, transaction_id):
        signature = request.json['signature']
        transaction_data = gfsi.transactions[transaction_id]
        if gfsi.verify_signature(transaction_data, bytes.fromhex(signature)):
            gfsi.execute_transaction(transaction_data, bytes.fromhex(signature))
            return jsonify({'message': 'Transaction executed successfully'})
        else:
            return jsonify({'error': 'Invalid signature'}), 401

class ExternalSystemIntegration(Resource):
    def post(self):
        external_system_url = request.json['external_system_url']
        transaction_id = request.json['transaction_id']
        transaction_data = gfsi.transactions[transaction_id]
        gfsi.integrate_with_external_system(external_system_url, transaction_data)
        return jsonify({'message': 'Transaction integrated with external system successfully'})

api.add_resource(Account, '/account', '/account/<string:account_id>')
api.add_resource(Transaction, '/transaction', '/transaction/<string:transaction_id>')
api.add_resource(ExternalSystemIntegration, '/external-system')

if __name__ == '__main__':
    app.run(debug=True)
