import json
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

class RiskDashboard:
    def __init__(self, transaction_log_file='transaction_log.json'):
        self.transaction_log_file = transaction_log_file
        self.transaction_log = []
        self.load_transaction_log()

    def load_transaction_log(self):
        """Load transaction log from a JSON file."""
        if os.path.exists(self.transaction_log_file):
            with open(self.transaction_log_file, 'r') as file:
                self.transaction_log = json.load(file)

    def save_transaction_log(self):
        """Save transaction log to a JSON file."""
        with open(self.transaction_log_file, 'w') as file:
            json.dump(self.transaction_log, file)

    def add_transaction(self, transaction):
        """Add a new transaction to the log."""
        self.transaction_log.append(transaction)
        self.save_transaction_log()

    def calculate_risk_exposure(self, user_id):
        """Calculate risk exposure for a specific user."""
        user_transactions = [tx for tx in self.transaction_log if tx['user_id'] == user_id]
        total_exposure = sum(tx['amount'] for tx in user_transactions)
        return total_exposure

    def generate_risk_report(self, user_id):
        """Generate a risk report for a specific user."""
        exposure = self.calculate_risk_exposure(user_id)
        report = {
            'user_id': user_id,
            'total_exposure': exposure,
            'timestamp': datetime.now().isoformat()
        }
        return report

    def visualize_risk_exposure(self, user_id):
        """Visualize risk exposure for a specific user."""
        user_transactions = [tx for tx in self.transaction_log if tx['user_id'] == user_id]
        if not user_transactions:
            print("No transactions found for this user.")
            return

        df = pd.DataFrame(user_transactions)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)

        plt.figure(figsize=(10, 5))
        plt.plot(df.index, df['amount'], marker='o', linestyle='-', label='Transaction Amount')
        plt.title(f'Risk Exposure Over Time for User {user_id}')
        plt.xlabel('Date')
        plt.ylabel('Amount')
        plt.legend()
        plt.grid()
        plt.show()

# Example usage
if __name__ == "__main__":
    risk_dashboard = RiskDashboard()

    # Example transaction data
    transaction1 = {
        'transaction_id': 'tx001',
        'user_id': 'user123',
        'amount': 1000,
        'timestamp': datetime.now().isoformat()
    }
    transaction2 = {
        'transaction_id': 'tx002',
        'user_id': 'user123',
        'amount': 500,
        'timestamp': datetime.now().isoformat()
    }

    # Add transactions
    risk_dashboard.add_transaction(transaction1)
    risk_dashboard.add_transaction(transaction2)

    # Generate risk report
    report = risk_dashboard.generate_risk_report('user123')
    print(f"Risk Report: {report}")

    # Visualize risk exposure
    risk_dashboard.visualize_risk_exposure('user123')
