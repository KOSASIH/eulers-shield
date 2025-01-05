import json
import os
from collections import defaultdict

class Governance:
    def __init__(self, storage_file='governance_proposals.json'):
        self.storage_file = storage_file
        self.proposals = []
        self.votes = defaultdict(lambda: defaultdict(int))  # proposal_id -> user_id -> vote_count
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
            'status': 'pending'
        }
        self.proposals.append(proposal)
        self.save_proposals()
        return f"Proposal #{proposal_id} submitted."

    def vote(self, user_id, proposal_id, vote):
        """Vote on a governance proposal."""
        if proposal_id > len(self.proposals) or proposal_id < 1:
            return "Invalid proposal ID."

        proposal = self.proposals[proposal_id - 1]
        if proposal['status'] != 'pending':
            return "Voting is closed for this proposal."

        # Record the vote
        if vote == 'for':
            self.votes[proposal_id][user_id] += 1
            proposal['votes_for'] += 1
        elif vote == 'against':
            self.votes[proposal_id][user_id] -= 1
            proposal['votes_against'] += 1
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

    def get_proposals(self):
        """Get a list of all proposals."""
        return self.proposals

# Example usage
if __name__ == "__main__":
    governance = Governance()

    # Propose a change
    print(governance.propose_change("user123", "Increase block reward to 15 Pi Coins."))

    # Vote on a proposal
    print(governance.vote("user456", 1, "for"))
    print(governance.vote("user789", 1, "against"))

    # Finalize the proposal
    print(governance.finalize_proposal(1))

    # Get all proposals
    proposals = governance.get_proposals()
    print("Current Proposals:")
    for proposal in proposals:
        print(proposal)
