import json
import os
from datetime import datetime

class ComplianceMonitor:
    def __init__(self, compliance_rules_file='compliance_rules.json', transaction_log_file='transaction_log.json'):
        self.compliance_rules_file = compliance_rules_file
        self.transaction_log_file = transaction_log_file
        self.compliance_rules = {}
        self.transaction_log = []
        self.load_compliance_rules()
        self.load_transaction_log()

    def load_compliance_rules(self):
        """Load compliance rules from a JSON file."""
        if os.path.exists(self.compliance_rules_file):
            with open(self.compliance_rules_file, 'r') as file:
                self.compliance_rules = json.load(file)

    def load_transaction_log(self):
        """Load transaction log from a JSON file."""
        if os.path.exists(self.transaction_log_file):
            with open(self.transaction_log_file, 'r') as file:
                self.transaction_log = json.load(file)

    def save_transaction_log(self):
        """Save transaction log to a JSON file."""
        with open(self.transaction_log_file, 'w') as file:
            json.dump(self.transaction_log, file)

    def validate_transaction(self, transaction):
        """Validate a transaction against compliance rules."""
        for rule in self.compliance_rules:
            if not self.check_rule(transaction, rule):
                return False, rule['description']
        return True, "Transaction is compliant."

    def check_rule(self, transaction, rule):
        """Check a single compliance rule against a transaction."""
        if rule['type'] == 'amount_limit':
            return transaction['amount'] <= rule['limit']
        elif rule['type'] == 'blacklist':
            return transaction['user_id'] not in rule['blacklisted_users']
        # Add more rule types as needed
        return True

    def log_transaction(self, transaction, is_compliant, reason):
        """Log the transaction and its compliance status."""
        log_entry = {
            'transaction_id': transaction['transaction_id'],
            'user_id': transaction['user_id'],
            'amount': transaction['amount'],
            'timestamp': datetime.now().isoformat(),
            'is_compliant': is_compliant,
            'reason': reason
        }
        self.transaction_log.append(log_entry)
        self.save_transaction_log()

    def monitor_transaction(self, transaction):
        """Monitor a transaction for compliance."""
        is_compliant, reason = self.validate_transaction(transaction)
        self.log_transaction(transaction, is_compliant, reason)
        return is_compliant, reason

# Example usage
if __name__ == "__main__":
    compliance_monitor = ComplianceMonitor()

    # Example transaction
    transaction = {
        'transaction_id': 'tx123456',
        'user_id': 'user123',
        'amount': 5000  # Example amount
    }

    is_compliant, reason = compliance_monitor.monitor_transaction(transaction)
    print(f"Transaction Compliance Status: {is_compliant}, Reason: {reason}")
