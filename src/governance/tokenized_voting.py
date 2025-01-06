import json
import os
from collections import defaultdict
from datetime import datetime

class TokenizedVoting:
    def __init__(self, storage_file='voting_data.json'):
        self.storage_file = storage_file
        self.proposals = []
        self.votes = defaultdict(lambda: defaultdict(int))  # proposal_id -> user_id -> vote_count
        self.user_tokens = defaultdict(int)  # user_id -> token balance
        self.load_data()

    def load_data(self):
        """Load proposals and voting data from a JSON file."""
        if os.path.exists(self.storage_file):
            with open(self.storage_file, 'r') as file:
                data = json.load(file)
                self.proposals = data.get('proposals', [])
                self.votes = defaultdict(lambda: defaultdict(int), data.get('votes', {}))
                self.user_tokens = defaultdict(int, data.get('user_tokens', {}))

    def save_data(self):
        """Save proposals and voting data to a JSON file."""
        with open(self.storage_file, 'w') as file:
            json.dump({
                'proposals': self.proposals,
                'votes': self.votes,
                'user_tokens': self.user_tokens
            }, file)

    def create_proposal(self, proposer_id, description):
        """Create a new governance proposal."""
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
        self.save_data()
        return f"Proposal #{proposal_id} created."

    def stake_tokens(self, user_id, amount):
        """Stake tokens for voting."""
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")
        self.user_tokens[user_id] += amount
        self.save_data()
        return f"{amount} tokens staked by {user_id}. Total tokens: {self.user_tokens[user_id]}."

    def vote(self, user_id, proposal_id, vote):
        """Vote on a governance proposal using staked tokens."""
        if proposal_id > len(self.proposals) or proposal_id < 1:
            return "Invalid proposal ID."

        proposal = self.proposals[proposal_id - 1]
        if proposal['status'] != 'pending':
            return "Voting is closed for this proposal."

        if user_id not in self.user_tokens or self.user_tokens[user_id] <= 0:
            return "User  has no staked tokens to vote."

        # Record the vote based on the number of tokens staked
        token_balance = self.user_tokens[user_id]
        if vote == 'for':
            self.votes[proposal_id][user_id] += token_balance
            proposal['votes_for'] += token_balance
        elif vote == 'against':
            self.votes[proposal_id][user_id] -= token_balance
            proposal['votes_against'] += token_balance
        else:
            return "Invalid vote. Use 'for' or 'against'."

        self.save_data()
        return f"Vote recorded for Proposal #{proposal_id} by {user_id}."

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
    voting_system = TokenizedVoting()

    # Create a new proposal
    print(voting_system.create_proposal("user123", "Increase the reward for liquidity providers."))

    # Stake tokens
    print(voting_system.stake_tokens("user123", 100))
    print(voting_system.stake_tokens("user456", 50))

    # Vote on a proposal
    ```python
    print(voting_system.vote("user123", 1, "for"))
    print(voting_system.vote("user456", 1, "against"))

    # Finalize the proposal
    print(voting_system.finalize_proposal(1))

    # Get all proposals
    proposals = voting_system.get_proposals()
    for proposal in proposals:
        print(f"Proposal ID: {proposal['id']}, Status: {proposal['status']}, Votes For: {proposal['votes_for']}, Votes Against: {proposal['votes_against']}")
