import json
import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes
from hashlib import sha256

class PrivacyEnhancements:
    def __init__(self, key_storage_file='user_keys.json'):
        self.key_storage_file = key_storage_file
        self.user_keys = {}
        self.load_keys()

    def load_keys(self):
        """Load user keys from a JSON file."""
        if os.path.exists(self.key_storage_file):
            with open(self.key_storage_file, 'r') as file:
                self.user_keys = json.load(file)

    def save_keys(self):
        """Save user keys to a JSON file."""
        with open(self.key_storage_file, 'w') as file:
            json.dump(self.user_keys, file)

    def generate_keys(self, user_id):
        """Generate a new RSA key pair for a user."""
        key = RSA.generate(2048)
        private_key = key.export_key()
        public_key = key.publickey().export_key()

        self.user_keys[user_id] = {
            'private_key': private_key.decode('utf-8'),
            'public_key': public_key.decode('utf-8')
        }
        self.save_keys()
        return public_key.decode('utf-8')

    def encrypt_data(self, user_id, data):
        """Encrypt data using the user's public key."""
        if user_id not in self.user_keys:
            raise ValueError("User  keys not found. Please generate keys first.")

        public_key = RSA.import_key(self.user_keys[user_id]['public_key'])
        cipher = PKCS1_OAEP.new(public_key)
        encrypted_data = cipher.encrypt(data.encode('utf-8'))
        return encrypted_data

    def decrypt_data(self, user_id, encrypted_data):
        """Decrypt data using the user's private key."""
        if user_id not in self.user_keys:
            raise ValueError("User  keys not found. Please generate keys first.")

        private_key = RSA.import_key(self.user_keys[user_id]['private_key'])
        cipher = PKCS1_OAEP.new(private_key)
        decrypted_data = cipher.decrypt(encrypted_data)
        return decrypted_data.decode('utf-8')

    def create_zero_knowledge_proof(self, secret):
        """Create a simple zero-knowledge proof for a secret."""
        # In a real implementation, this would be a more complex ZKP
        proof = sha256(secret.encode()).hexdigest()
        return proof

    def verify_zero_knowledge_proof(self, proof, secret):
        """Verify the zero-knowledge proof."""
        expected_proof = sha256(secret.encode()).hexdigest()
        return proof == expected_proof

# Example usage
if __name__ == "__main__":
    privacy = PrivacyEnhancements()

    # Generate keys for a user
    user_id = "user123"
    public_key = privacy.generate_keys(user_id)
    print(f"Generated public key for {user_id}: {public_key}")

    # Encrypt and decrypt data
    secret_data = "This is a secret message."
    encrypted_data = privacy.encrypt_data(user_id, secret_data)
    print(f"Encrypted data: {encrypted_data}")

    decrypted_data = privacy.decrypt_data(user_id, encrypted_data)
    print(f"Decrypted data: {decrypted_data}")

    # Create and verify a zero-knowledge proof
    secret = "my_secret"
    proof = privacy.create_zero_knowledge_proof(secret)
    print(f"Generated proof: {proof}")

    is_valid = privacy.verify_zero_knowledge_proof(proof, secret)
    print(f"Is the proof valid? {is_valid}")
