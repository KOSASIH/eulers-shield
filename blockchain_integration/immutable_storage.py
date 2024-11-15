import json
import os
from hashlib import sha256

class ImmutableStorage:
    def __init__(self, storage_path):
        """Initialize the immutable storage."""
        self.storage_path = storage_path
        if not os.path.exists(storage_path):
            os.makedirs(storage_path)

    def store_data(self, data):
        """Store data immutably by hashing and saving it."""
        data_hash = sha256(json.dumps(data).encode()).hexdigest()
        file_path = os.path.join(self.storage_path, f"{data_hash}.json")
        with open(file_path, 'w') as f:
            json.dump(data, f)
        return data_hash

    def retrieve_data(self, data_hash):
        """Retrieve data using its hash."""
        file_path = os.path.join(self.storage_path, f"{data_hash}.json")
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return json.load(f)
        else:
            raise FileNotFoundError("Data not found.")

# Example Usage
if __name__ == "__main__":
    storage = ImmutableStorage('immutable_storage')
    data = {'name': 'Alice', 'age': 30}
    data_hash = storage.store_data(data)
    print("Data stored with hash:", data_hash)
    retrieved_data = storage.retrieve_data(data_hash)
    print("Retrieved data:", retrieved_data)
