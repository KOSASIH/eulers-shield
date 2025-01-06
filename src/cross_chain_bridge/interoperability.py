import json
import os
from web3 import Web3

class CrossChainInteroperability:
    def __init__(self, storage_file='cross_chain_assets.json', provider_url='https://your.ethereum.node'):
        self.storage_file = storage_file
        self.assets = {}
        self.web3 = Web3(Web3.HTTPProvider(provider_url))
        self.load_assets()

    def load_assets(self):
        """Load cross-chain assets from a JSON file."""
        if os.path.exists(self.storage_file):
            with open(self.storage_file, 'r') as file:
                self.assets = json.load(file)

    def save_assets(self):
        """Save cross-chain assets to a JSON file."""
        with open(self.storage_file, 'w') as file:
            json.dump(self.assets, file)

    def register_asset(self, asset_id, chain_id, owner, asset_data):
        """Register a new cross-chain asset."""
        if asset_id in self.assets:
            raise ValueError("Asset ID already exists.")

        asset = {
            'asset_id': asset_id,
            'chain_id': chain_id,
            'owner': owner,
            'asset_data': asset_data,
            'transfers': []
        }
        self.assets[asset_id] = asset
        self.save_assets()
        return f"Asset {asset_id} registered successfully on chain {chain_id}."

    def transfer_asset(self, asset_id, new_owner, target_chain):
        """Transfer ownership of a cross-chain asset."""
        if asset_id not in self.assets:
            raise ValueError("Asset ID not found.")

        asset = self.assets[asset_id]
        old_owner = asset['owner']
        asset['owner'] = new_owner
        asset['transfers'].append({
            'from': old_owner,
            'to': new_owner,
            'target_chain': target_chain,
            'timestamp': self.web3.eth.getBlock('latest')['timestamp']
        })
        self.save_assets()
        return f"Asset {asset_id} transferred from {old_owner} to {new_owner} on chain {target_chain}."

    def get_asset_details(self, asset_id):
        """Get details of a specific cross-chain asset."""
        if asset_id not in self.assets:
            return "Asset ID not found."
        return self.assets[asset_id]

    def swap_assets(self, asset_id_a, asset_id_b):
        """Swap two cross-chain assets."""
        if asset_id_a not in self.assets or asset_id_b not in self.assets:
            raise ValueError("One or both asset IDs not found.")

        asset_a = self.assets[asset_id_a]
        asset_b = self.assets[asset_id_b]

        # Swap ownership
        old_owner_a = asset_a['owner']
        old_owner_b = asset_b['owner']
        asset_a['owner'] = old_owner_b
        asset_b['owner'] = old_owner_a

        # Log the transfers
        asset_a['transfers'].append({
            'from': old_owner_a,
            'to': old_owner_b,
            'timestamp': self.web3.eth.getBlock('latest')['timestamp']
        })
        asset_b['transfers'].append({
            'from': old_owner_b,
            'to': old_owner_a,
            'timestamp': self.web3.eth.getBlock('latest')['timestamp']
        })

        self.save_assets()
        return f"Assets {asset_id_a} and {asset_id_b} swapped successfully."

# Example usage
if __name__ == "__main__":
    interoperability_manager = CrossChainInteroperability()

    # Register a new cross-chain asset
    asset_id = "asset123"
    chain_id = "Ethereum"
    owner = "user123"
    asset_data = {
        "name": "Example Digital Art",
        "value": 1000
    }
    print(interoperability_manager.register_asset(asset_id, chain_id, owner, asset_data))

    # Transfer ownership of the asset
    new_owner = "user456"
    print(interoperability_manager.transfer_asset(asset_id, new_owner, chain_id))

    # Get asset details
    asset_details = interoperability_manager.get_asset_details(asset_id)
    print(f"Asset Details: {asset_details}")

    # Swap two assets
    asset_id_b = "asset456"  # Assume this asset is already registered
    print(interoperability_manager.swap_assets(asset_id, asset_id_b))
