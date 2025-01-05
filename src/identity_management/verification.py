import json
import os
from cryptography.fernet import Fernet

class Verification:
    def __init__(self, storage_file='verifications.json'):
        self.storage_file = storage_file
        self.verifications = {}
        self.load_verifications()

    def load_verifications(self):
        """Load verifications from a JSON file."""
        if os.path.exists(self.storage_file):
            with open(self.storage_file, 'r') as file:
                self.verifications = json.load(file)

    def save_verifications(self):
        """Save verifications to a JSON file."""
        with open(self.storage_file, 'w') as file:
            json.dump(self.verifications, file)

    def request_verification(self, user_id, credentials):
        """Request verification for a user."""
        if user_id in self.verifications:
            return f"Verification for {user_id} is already in process."

        # Encrypt credentials for security
        encrypted_credentials = self.encrypt_credentials(credentials)
        self.verifications[user_id] = encrypted_credentials
        self.save_verifications()
        return f"Verification requested for {user_id}."

    def verify_credentials(self, user_id, provided_credentials):
        """Verify the provided credentials against stored credentials."""
        if user_id not in self.verifications:
            return "No verification request found for this user."

        # Decrypt stored credentials
        encrypted_credentials = self.verifications[user_id]
        stored_credentials = self.decrypt_credentials(encrypted_credentials)

        # Check if provided credentials match stored credentials
        if provided_credentials == stored_credentials:
            del self.verifications[user_id]  # Remove verification after success
            self.save_verifications()
            return f"Verification successful for {user_id}."
        else:
            return "Verification failed. Credentials do not match."

    def encrypt_credentials(self, credentials):
        """Encrypt user credentials."""
        key = Fernet.generate_key()
        cipher_suite = Fernet(key)
        encrypted_data = cipher_suite.encrypt(json.dumps(credentials).encode())
        return {'key': key.decode(), 'data': encrypted_data.decode()}

    def decrypt_credentials(self, encrypted_data):
        """Decrypt user credentials."""
        key = encrypted_data['key'].encode()
        cipher_suite = Fernet(key)
        decrypted_data = cipher_suite.decrypt(encrypted_data['data'].encode())
        return json.loads(decrypted_data)

# Example usage
if __name__ == "__main__":
    verifier = Verification()
    user_id = "user123"
    credentials = {"email": "alice@example.com", "password": "securepassword"}

    print(verifier.request_verification(user_id, credentials))
    print(verifier.verify_credentials(user_id, {"email": "alice@example.com", "password": "securepassword"}))
    print(verifier.verify_credentials(user_id, {"email": "alice@example.com", "password": "wrongpassword"}))
