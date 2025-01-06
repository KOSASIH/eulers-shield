import json
import os
from datetime import datetime

class ComplianceAutomation:
    def __init__(self, rules_file='compliance_rules.json', transaction_log_file='transaction_log.json'):
        self.rules_file = rules_file
        self.transaction_log_file = transaction_log_file
        self.compliance_rules = []
        self.transaction_log = []
        self.load_compliance_rules()
        self.load_transaction_log()

    def load_compliance_rules(self):
        """Load compliance rules from a JSON file."""
        if os.path.exists(self.rules_file):
            with open(self.rules_file, 'r') as file:
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

    def monitor_transaction(self, transaction):
        """Monitor a transaction for compliance."""
        is_compliant, reasons = self.validate_transaction(transaction)
        self.log_transaction(transaction, is_compliant, reasons)
        return is_compliant, reasons

    def validate_transaction(self, transaction):
        """Validate a transaction against compliance rules."""
        reasons = []
        for rule in self.compliance_rules:
            if not self.check_rule(transaction, rule):
                reasons.append(rule['description'])
        is_compliant = len(reasons) == 0
        return is_compliant, reasons

    def check_rule(self, transaction, rule):
        """Check a single compliance rule against a transaction."""
        if rule['type'] == 'amount_limit':
            return transaction['amount'] <= rule['limit']
        elif rule['type'] == 'blacklist':
            return transaction['user_id'] not in rule['blacklisted_users']
        # Add more rule types as needed
        return True

    def log_transaction(self, transaction, is_compliant, reasons):
        """Log the transaction and its compliance status."""
        log_entry = {
            'transaction_id': transaction['transaction_id'],
            'user_id': transaction['user_id'],
            'amount': transaction['amount'],
            'timestamp': datetime.now().isoformat(),
            'is_compliant': is_compliant,
            'reasons': reasons
        }
        self.transaction_log.append(log_entry)
        self.save_transaction_log()

    def generate_compliance_report(self):
        """Generate a compliance report based on the transaction log."""
        report = {
            'total_transactions': len(self.transaction_log),
            'compliant_transactions': sum(1 for tx in self.transaction_log if tx['is_compliant']),
            'non_compliant_transactions': sum(1 for tx in self.transaction_log if not tx['is_compliant']),
            'details': self.transaction_log
        }
        return report

# Example usage
if __name__ == "__main__":
    compliance_automation = ComplianceAutomation()

    # Example transaction
    transaction = {
        'transaction_id': 'tx123456',
        'user_id': 'user123',
        'amount': 5000  # Example amount
    }

    # Monitor the transaction
    is_compliant, reasons = compliance_automation.monitor_transaction(transaction)
    print(f"Transaction Compliance Status: {is_compliant}, Reasons: {reasons}")

    # Generate compliance report
    report = compliance_automation.generate_compliance_report()
    print(f"Compliance Report: {report}")
