import json
import os
import hashlib
import time

class CrossChainBridge:
    def __init__(self, storage_file='cross_chain_transfers.json'):
        self.storage_file = storage_file
        self.transfers = []
        self.load_transfers()

    def load_transfers(self):
        """Load previous cross-chain transfers from a JSON file."""
        if os.path.exists(self.storage_file):
            with open(self.storage_file, 'r') as file:
                self.transfers = json.load(file)

    def save_transfers(self):
        """Save cross-chain transfers to a JSON file."""
        with open(self.storage_file, 'w') as file:
            json.dump(self.transfers, file)

    def transfer_asset(self, asset, amount, target_chain):
        """Initiate a cross-chain asset transfer."""
        transfer_id = self.generate_transfer_id(asset, amount, target_chain)
        timestamp = time.time()

        # Log the transfer
        transfer_record = {
            'transfer_id': transfer_id,
            'asset': asset,
            'amount': amount,
            'target_chain': target_chain,
            'timestamp': timestamp,
            'status': 'pending'
        }
        self.transfers.append(transfer_record)
        self.save_transfers()

        # Simulate the transfer process
        self.simulate_transfer(transfer_record)

        return f"Transfer initiated: {transfer_id} for {amount} {asset} to {target_chain}."

    def generate_transfer_id(self, asset, amount, target_chain):
        """Generate a unique transfer ID based on asset, amount, and target chain."""
        unique_string = f"{asset}-{amount}-{target_chain}-{time.time()}"
        return hashlib.sha256(unique_string.encode()).hexdigest()

    def simulate_transfer(self, transfer_record):
        """Simulate the transfer process (this would be replaced with actual cross-chain logic)."""
        time.sleep(2)  # Simulate network delay
        transfer_record['status'] = 'completed'
        self.save_transfers()
        print(f"Transfer {transfer_record['transfer_id']} completed successfully.")

    def get_transfer_status(self, transfer_id):
        """Get the status of a specific transfer."""
        for transfer in self.transfers:
            if transfer['transfer_id'] == transfer_id:
                return transfer
        return "Transfer ID not found."

# Example usage
if __name__ == "__main__":
    bridge = CrossChainBridge()
    print(bridge.transfer_asset('PiCoin', 100, 'Ethereum'))  # Initiate a transfer
    time.sleep(3)  # Wait for the transfer to complete
    transfer_id = bridge.transfers[-1]['transfer_id']  # Get the last transfer ID
    print(bridge.get_transfer_status(transfer_id))  # Check the status of the transfer
