import json
import os
from cryptography.fernet import Fernet

class IdentityManager:
    def __init__(self, storage_file='identities.json'):
        self.storage_file = storage_file
        self.identities = {}
        self.load_identities()

    def load_identities(self):
        """Load identities from a JSON file."""
        if os.path.exists(self.storage_file):
            with open(self.storage_file, 'r') as file:
                self.identities = json.load(file)

    def save_identities(self):
        """Save identities to a JSON file."""
        with open(self.storage_file, 'w') as file:
            json.dump(self.identities, file)

    def create_identity(self, user_id, attributes):
        """Create a new identity."""
        if user_id in self.identities:
            return f"Identity for {user_id} already exists."

        # Encrypt attributes for security
        encrypted_attributes = self.encrypt_attributes(attributes)
        self.identities[user_id] = encrypted_attributes
        self.save_identities()
        return f"Identity for {user_id} created."

    def get_identity(self, user_id):
        """Retrieve an identity."""
        if user_id not in self.identities:
            return "Identity not found."

        # Decrypt attributes before returning
        decrypted_attributes = self.decrypt_attributes(self.identities[user_id])
        return {user_id: decrypted_attributes}

    def update_identity(self, user_id, new_attributes):
        """Update an existing identity."""
        if user_id not in self.identities:
            return "Identity not found."

        # Encrypt new attributes for security
        encrypted_attributes = self.encrypt_attributes(new_attributes)
        self.identities[user_id] = encrypted_attributes
        self.save_identities()
        return f"Identity for {user_id} updated."

    def delete_identity(self, user_id):
        """Delete an identity."""
        if user_id not in self.identities:
            return "Identity not found."

        del self.identities[user_id]
        self.save_identities()
        return f"Identity for {user_id} deleted."

    def encrypt_attributes(self, attributes):
        """Encrypt identity attributes."""
        key = Fernet.generate_key()
        cipher_suite = Fernet(key)
        encrypted_data = cipher_suite.encrypt(json.dumps(attributes).encode())
        return {'key': key.decode(), 'data': encrypted_data.decode()}

    def decrypt_attributes(self, encrypted_data):
        """Decrypt identity attributes."""
        key = encrypted_data['key'].encode()
        cipher_suite = Fernet(key)
        decrypted_data = cipher_suite.decrypt(encrypted_data['data'].encode())
        return json.loads(decrypted_data)

# Example usage
if __name__ == "__main__":
    manager = IdentityManager()
    print(manager.create_identity("user123", {"name": "Alice", "email": "alice@example.com"}))
    print(manager.get_identity("user123"))
    print(manager.update_identity("user123", {"name": "Alice Smith", "email": "alice.smith@example.com"}))
    print(manager.get_identity("user123"))
    print(manager.delete_identity("user123"))
