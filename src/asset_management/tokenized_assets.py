import json
import os
from datetime import datetime
from web3 import Web3

class TokenizedAsset:
    def __init__(self, storage_file='tokenized_assets.json', provider_url='https://your.ethereum.node'):
        self.storage_file = storage_file
        self.assets = {}
        self.web3 = Web3(Web3.HTTPProvider(provider_url))
        self.load_assets()

    def load_assets(self):
        """Load tokenized assets from a JSON file."""
        if os.path.exists(self.storage_file):
            with open(self.storage_file, 'r') as file:
                self.assets = json.load(file)

    def save_assets(self):
        """Save tokenized assets to a JSON file."""
        with open(self.storage_file, 'w') as file:
            json.dump(self.assets, file)

    def create_asset(self, asset_id, owner, asset_data):
        """Create a new tokenized asset."""
        if asset_id in self.assets:
            raise ValueError("Asset ID already exists.")

        asset = {
            'asset_id': asset_id,
            'owner': owner,
            'asset_data': asset_data,
            'created_at': datetime.now().isoformat(),
            'transfers': []
        }
        self.assets[asset_id] = asset
        self.save_assets()
        return f"Asset {asset_id} created successfully."

    def transfer_asset(self, asset_id, new_owner):
        """Transfer ownership of a tokenized asset."""
        if asset_id not in self.assets:
            raise ValueError("Asset ID not found.")

        asset = self.assets[asset_id]
        old_owner = asset['owner']
        asset['owner'] = new_owner
        asset['transfers'].append({
            'from': old_owner,
            'to': new_owner,
            'timestamp': datetime.now().isoformat()
        })
        self.save_assets()
        return f"Asset {asset_id} transferred from {old_owner} to {new_owner}."

    def verify_ownership(self, asset_id, user):
        """Verify ownership of a tokenized asset."""
        if asset_id not in self.assets:
            return False
        return self.assets[asset_id]['owner'] == user

    def get_asset_details(self, asset_id):
        """Get details of a specific tokenized asset."""
        if asset_id not in self.assets:
            return "Asset ID not found."
        return self.assets[asset_id]

# Example usage
if __name__ == "__main__":
    asset_manager = TokenizedAsset()

    # Create a new tokenized asset
    asset_id = "asset123"
    owner = "user123"
    asset_data = {
        "name": "Example Real Estate",
        "location": "123 Main St, Anytown, USA",
        "value": 500000
    }
    print(asset_manager.create_asset(asset_id, owner, asset_data))

    # Transfer ownership of the asset
    new_owner = "user456"
    print(asset_manager.transfer_asset(asset_id, new_owner))

    # Verify ownership
    is_owner = asset_manager.verify_ownership(asset_id, new_owner)
    print(f"Is {new_owner} the owner of {asset_id}? {is_owner}")

    # Get asset details
    asset_details = asset_manager.get_asset_details(asset_id)
    print(f"Asset Details: {asset_details}")
