import json
import os
from collections import defaultdict
from datetime import datetime

class AdvancedGovernance:
    def __init__(self, storage_file='governance_proposals.json'):
        self.storage_file = storage_file
        self.proposals = []
        self.votes = defaultdict(lambda: defaultdict(int))  # proposal_id -> user_id -> vote_count
        self.reputation = defaultdict(int)  # user_id -> reputation score
        self.load_proposals()

    def load_proposals(self):
        """Load existing proposals from a JSON file."""
        if os.path.exists(self.storage_file):
            with open(self.storage_file, 'r') as file:
                data = json.load(file)
                self.proposals = data.get('proposals', [])
                self.votes = defaultdict(lambda: defaultdict(int), data.get('votes', {}))

    def save_proposals(self):
        """Save proposals and votes to a JSON file."""
        with open(self.storage_file, 'w') as file:
            json.dump({
                'proposals': self.proposals,
                'votes': self.votes
            }, file)

    def propose_change(self, proposer_id, description):
        """Submit a new governance proposal."""
        proposal_id = len(self.proposals) + 1
        proposal = {
            'id': proposal_id,
            'proposer_id': proposer_id,
            'description': description,
            'votes_for': 0,
            'votes_against': 0,
            'status': 'pending',
            'created_at': datetime.now().isoformat()
        }
        self.proposals.append(proposal)
        self.save_proposals()
        return f"Proposal #{proposal_id} submitted."

    def vote(self, user_id, proposal_id, vote):
        """Vote on a governance proposal using quadratic voting."""
        if proposal_id > len(self.proposals) or proposal_id < 1:
            return "Invalid proposal ID."

        proposal = self.proposals[proposal_id - 1]
        if proposal['status'] != 'pending':
            return "Voting is closed for this proposal."

        # Calculate the voting power based on reputation
        voting_power = self.reputation[user_id] ** 0.5  # Quadratic voting
        if vote == 'for':
            self.votes[proposal_id][user_id] += voting_power
            proposal['votes_for'] += voting_power
        elif vote == 'against':
            self.votes[proposal_id][user_id] -= voting_power
            proposal['votes_against'] += voting_power
        else:
            return "Invalid vote. Use 'for' or 'against'."

        self.save_proposals()
        return f"Vote recorded for Proposal #{proposal_id}."

    def finalize_proposal(self, proposal_id):
        """Finalize a proposal based on the voting results."""
        if proposal_id > len(self.proposals) or proposal_id < 1:
            return "Invalid proposal ID."

        proposal = self.proposals[proposal_id - 1]
        if proposal['status'] != 'pending':
            return "Proposal has already been finalized."

        # Determine the outcome
        if proposal['votes_for'] > proposal['votes_against']:
            proposal['status'] = 'approved'
            return f"Proposal #{proposal_id} approved."
        else:
            proposal['status'] = 'rejected'
            return f"Proposal #{proposal_id} rejected."

    def delegate_vote(self, delegator_id, delegatee_id, proposal_id):
        """Delegate voting rights to another user."""
        if delegator_id not in self.reputation:
            return "Delegator not found."
        if delegatee_id not in self.reputation:
            return "Delegatee not found."
        if proposal_id > len(self.proposals) or proposal_id < 1:
            return "Invalid proposal ID."

        # Logic to delegate votes (this is a simplified version)
        self.votes[proposal_id][delegatee_id] += self.votes[proposal_id][delegator_id]
        self.votes[proposal_id][delegator_id] = 0  # Clear the delegator's votes

        return f"Votes from {delegator_id} delegated to {delegatee_id} for Proposal #{proposal_id}."

    def get_proposals(self):
        """Get a list of all proposals."""
        return self.proposals

    def set_reputation(self, user_id, score):
        """Set the reputation score for a user."""
        self.reputation[user_id] = score

# Example usage
if __name__ == "__main
