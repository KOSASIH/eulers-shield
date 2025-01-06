import json
import os
from datetime import datetime
from collections import defaultdict

class DecentralizedInsurance:
    def __init__(self, storage_file='insurance_data.json'):
        self.storage_file = storage_file
        self.policies = []
        self.claims = []
        self.load_data()

    def load_data(self):
        """Load insurance policies and claims from a JSON file."""
        if os.path.exists(self.storage_file):
            with open(self.storage_file, 'r') as file:
                data = json.load(file)
                self.policies = data.get('policies', [])
                self.claims = data.get('claims', [])

    def save_data(self):
        """Save insurance policies and claims to a JSON file."""
        with open(self.storage_file, 'w') as file:
            json.dump({
                'policies': self.policies,
                'claims': self.claims
            }, file)

    def create_policy(self, user_id, policy_type, premium, coverage_amount):
        """Create a new insurance policy."""
        policy_id = len(self.policies) + 1
        policy = {
            'policy_id': policy_id,
            'user_id': user_id,
            'policy_type': policy_type,
            'premium': premium,
            'coverage_amount': coverage_amount,
            'status': 'active',
            'created_at': datetime.now().isoformat()
        }
        self.policies.append(policy)
        self.save_data()
        return f"Policy #{policy_id} created for {user_id}."

    def file_claim(self, user_id, policy_id, claim_amount):
        """File a claim against an insurance policy."""
        policy = next((p for p in self.policies if p['policy_id'] == policy_id and p['user_id'] == user_id), None)
        if not policy:
            return "Policy not found or does not belong to the user."

        if claim_amount > policy['coverage_amount']:
            return "Claim amount exceeds coverage amount."

        claim_id = len(self.claims) + 1
        claim = {
            'claim_id': claim_id,
            'policy_id': policy_id,
            'user_id': user_id,
            'claim_amount': claim_amount,
            'status': 'pending',
            'filed_at': datetime.now().isoformat()
        }
        self.claims.append(claim)
        self.save_data()
        return f"Claim #{claim_id} filed for Policy #{policy_id}."

    def process_claim(self, claim_id, approve=True):
        """Process a claim and approve or deny it."""
        claim = next((c for c in self.claims if c['claim_id'] == claim_id), None)
        if not claim:
            return "Claim not found."

        if approve:
            claim['status'] = 'approved'
            return f"Claim #{claim_id} approved."
        else:
            claim['status'] = 'denied'
            return f"Claim #{claim_id} denied."

    def get_policy_details(self, policy_id):
        """Get details of a specific insurance policy."""
        policy = next((p for p in self.policies if p['policy_id'] == policy_id), None)
        if not policy:
            return "Policy not found."
        return policy

    def get_claim_details(self, claim_id):
        """Get details of a specific claim."""
        claim = next((c for c in self.claims if c['claim_id'] == claim_id), None)
        if not claim:
            return "Claim not found."
        return claim

# Example usage
if __name__ == "__main__":
    insurance_system = DecentralizedInsurance()

    # Create a new insurance policy
    print(insurance_system.create_policy("user123", "Health Insurance", 200, 5000))

    # File a claim
    print(insurance_system.file_claim("user123", 1, 3000))

    # Process the claim
    print(insurance_system.process_claim(1, approve=True))

    # Get policy details
    policy_details = insurance_system.get_policy_details(1)
    print(f"Policy Details: {policy_details}")

    # Get claim details
    claim_details = insurance_system.get_claim_details(1)
    print(f"Claim Details: {claim_details}")
