import json
import os
import hashlib
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes

class IdentityVerification:
    def __init__(self, storage_file='user_identities.json'):
        self.storage_file = storage_file
        self.user_identities = {}
        self.load_identities()

    def load_identities(self):
        """Load user identities from a JSON file."""
        if os.path.exists(self.storage_file):
            with open(self.storage_file, 'r') as file:
                self.user_identities = json.load(file)

    def save_identities(self):
        """Save user identities to a JSON file."""
        with open(self.storage_file, 'w') as file:
            json.dump(self.user_identities, file)

    def generate_keys(self, user_id):
        """Generate a new RSA key pair for a user."""
        key = RSA.generate(2048)
        private_key = key.export_key()
        public_key = key.publickey().export_key()

        self.user_identities[user_id] = {
            'private_key': private_key.decode('utf-8'),
            'public_key': public_key.decode('utf-8'),
            'identity_data': {}
        }
        self.save_identities()
        return public_key.decode('utf-8')

    def register_identity(self, user_id, identity_data):
        """Register a new identity for a user."""
        if user_id not in self.user_identities:
            raise ValueError("User keys not found. Please generate keys first.")

        self.user_identities[user_id]['identity_data'] = identity_data
        self.save_identities()
        return f"Identity registered for user {user_id}."

    def encrypt_data(self, user_id, data):
        """Encrypt identity data using the user's public key."""
        if user_id not in self.user_identities:
            raise ValueError("User keys not found. Please generate keys first.")

        public_key = RSA.import_key(self.user_identities[user_id]['public_key'])
        cipher = PKCS1_OAEP.new(public_key)
        encrypted_data = cipher.encrypt(data.encode('utf-8'))
        return encrypted_data

    def decrypt_data(self, user_id, encrypted_data):
        """Decrypt identity data using the user's private key."""
        if user_id not in self.user_identities:
            raise ValueError("User keys not found. Please generate keys first.")

        private_key = RSA.import_key(self.user_identities[user_id]['private_key'])
        cipher = PKCS1_OAEP.new(private_key)
        decrypted_data = cipher.decrypt(encrypted_data)
        return decrypted_data.decode('utf-8')

    def verify_identity(self, user_id):
        """Verify the identity of a user."""
        if user_id not in self.user_identities:
            return "Identity not found."

        identity_data = self.user_identities[user_id]['identity_data']
        return identity_data if identity_data else "Identity data not registered."

    def create_verifiable_credential(self, user_id, credential_data):
        """Create a verifiable credential for a user."""
        if user_id not in self.user_identities:
            raise ValueError("User keys not found. Please generate keys first.")

        credential_hash = hashlib.sha256(json.dumps(credential_data).encode()).hexdigest()
        return {
            'user_id': user_id,
            'credential_data': credential_data,
            'credential_hash': credential_hash
        }

    def verify_credential(self, credential):
        """Verify a verifiable credential."""
        expected_hash = hashlib.sha256(json.dumps(credential['credential_data']).encode()).hexdigest()
        return expected_hash == credential['credential_hash']

# Example usage
if __name__ == "__main__":
    identity_manager = IdentityVerification()

    # Generate keys for a user
    user_id = "user123"
    public_key = identity_manager.generate_keys(user_id)
    print(f"Generated public key for {user_id}: {public_key}")

    # Register an identity
    identity_data = {
        "name": "Alice",
        "age": 30,
        "email": "alice@example.com"
    }
    print(identity_manager.register_identity(user_id, identity_data))

    # Verify identity
    verified_identity = identity_manager.verify_identity(user_id)
    print(f"Verified identity data: {verified_identity}")

    # Encrypt and decrypt identity data
    encrypted_data = identity_manager.encrypt_data(user_id, json.dumps(identity_data))
    print(f"Encrypted identity data: {encrypted_data}")

    decrypted _data = identity_manager.decrypt_data(user_id, encrypted_data)
    print(f"Decrypted identity data: {decrypted_data}")

    # Create and verify a verifiable credential
    credential_data = {
        "degree": "Bachelor of Science",
        "institution": "University of Example",
        "year": 2023
    }
    credential = identity_manager.create_verifiable_credential(user_id, credential_data)
    print(f"Created verifiable credential: {credential}")

    is_valid = identity_manager.verify_credential(credential)
    print(f"Is the credential valid? {is_valid}") ```python
    # Continue with the example usage
    # Generate keys for another user
    user_id_2 = "user456"
    public_key_2 = identity_manager.generate_keys(user_id_2)
    print(f"Generated public key for {user_id_2}: {public_key_2}")

    # Register an identity for the second user
    identity_data_2 = {
        "name": "Bob",
        "age": 28,
        "email": "bob@example.com"
    }
    print(identity_manager.register_identity(user_id_2, identity_data_2))

    # Verify identity for the second user
    verified_identity_2 = identity_manager.verify_identity(user_id_2)
    print(f"Verified identity data for {user_id_2}: {verified_identity_2}")

    # Encrypt and decrypt identity data for the second user
    encrypted_data_2 = identity_manager.encrypt_data(user_id_2, json.dumps(identity_data_2))
    print(f"Encrypted identity data for {user_id_2}: {encrypted_data_2}")

    decrypted_data_2 = identity_manager.decrypt_data(user_id_2, encrypted_data_2)
    print(f"Decrypted identity data for {user_id_2}: {decrypted_data_2}")

    # Create and verify a verifiable credential for the second user
    credential_data_2 = {
        "degree": "Master of Science",
        "institution": "Institute of Example",
        "year": 2024
    }
    credential_2 = identity_manager.create_verifiable_credential(user_id_2, credential_data_2)
    print(f"Created verifiable credential for {user_id_2}: {credential_2}")

    is_valid_2 = identity_manager.verify_credential(credential_2)
    print(f"Is the credential for {user_id_2} valid? {is_valid_2}")
