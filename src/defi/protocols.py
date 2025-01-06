import json
import os
from datetime import datetime

class DeFiProtocol:
    def __init__(self, storage_file='defi_protocols.json'):
        self.storage_file = storage_file
        self.users = {}
        self.loans = []
        self.load_data()

    def load_data(self):
        """Load user data and loans from a JSON file."""
        if os.path.exists(self.storage_file):
            with open(self.storage_file, 'r') as file:
                data = json.load(file)
                self.users = data.get('users', {})
                self.loans = data.get('loans', [])

    def save_data(self):
        """Save user data and loans to a JSON file."""
        with open(self.storage_file, 'w') as file:
            json.dump({
                'users': self.users,
                'loans': self.loans
            }, file)

    def deposit(self, user_id, amount):
        """Deposit funds into the DeFi protocol."""
        if user_id not in self.users:
            self.users[user_id] = {'balance': 0, 'loans': []}
        
        self.users[user_id]['balance'] += amount
        self.save_data()
        return f"{amount} deposited. New balance: {self.users[user_id]['balance']}."

    def borrow(self, user_id, amount, interest_rate, duration):
        """Borrow funds from the DeFi protocol."""
        if user_id not in self.users:
            return "User  not found. Please deposit funds first."

        if self.users[user_id]['balance'] < amount:
            return "Insufficient balance to borrow."

        loan = {
            'loan_id': len(self.loans) + 1,
            'user_id': user_id,
            'amount': amount,
            'interest_rate': interest_rate,
            'duration': duration,
            'start_date': datetime.now().isoformat(),
            'status': 'active'
        }
        self.loans.append(loan)
        self.users[user_id]['balance'] -= amount
        self.save_data()
        return f"Loan of {amount} granted to {user_id}."

    def repay_loan(self, user_id, loan_id):
        """Repay a loan."""
        loan = next((loan for loan in self.loans if loan['loan_id'] == loan_id and loan['user_id'] == user_id), None)
        if not loan:
            return "Loan not found or does not belong to the user."

        # Calculate total repayment amount
        total_repayment = loan['amount'] + (loan['amount'] * loan['interest_rate'] / 100)
        self.users[user_id]['balance'] += total_repayment
        loan['status'] = 'repaid'
        self.save_data()
        return f"Loan {loan_id} repaid. Total repayment: {total_repayment}."

    def get_user_balance(self, user_id):
        """Get the balance of a user."""
        if user_id not in self.users:
            return "User  not found."
        return f"User  {user_id} balance: {self.users[user_id]['balance']}."

    def get_loans(self, user_id):
        """Get all loans for a user."""
        if user_id not in self.users:
            return "User  not found."
        return self.users[user_id]['loans']

# Example usage
if __name__ == "__main__":
    defi_protocol = DeFiProtocol()

    # Deposit funds
    print(defi_protocol.deposit("user123", 1000))

    # Borrow funds
    print(defi_protocol.borrow("user123", 500, 5, 30))  # Borrowing 500 with 5% interest for 30 days

    # Get user balance
    print(defi_protocol.get_user_balance("user123"))

    # Repay loan
    print(defi_protocol.repay_loan("user123", 1))  # Repaying loan with ID 1

    # Get loans
    print(defi_protocol.get_loans("user123"))
