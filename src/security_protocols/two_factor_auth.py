import pyotp
import base64
import os
import json

class TwoFactorAuth:
    def __init__(self, storage_file='2fa_secrets.json'):
        self.storage_file = storage_file
        self.secrets = {}
        self.load_secrets()

    def load_secrets(self):
        """Load 2FA secrets from a JSON file."""
        if os.path.exists(self.storage_file):
            with open(self.storage_file, 'r') as file:
                self.secrets = json.load(file)

    def save_secrets(self):
        """Save 2FA secrets to a JSON file."""
        with open(self.storage_file, 'w') as file:
            json.dump(self.secrets, file)

    def generate_secret(self, user_id):
        """Generate a new 2FA secret for a user."""
        secret = pyotp.random_base32()
        self.secrets[user_id] = secret
        self.save_secrets()
        return secret

    def get_totp_uri(self, user_id):
        """Get the TOTP URI for the user to set up in an authenticator app."""
        if user_id not in self.secrets:
            return "No 2FA secret found for this user."
        
        secret = self.secrets[user_id]
        return f"otpauth://totp/{user_id}?secret={secret}&issuer=EulerShield"

    def verify_totp(self, user_id, token):
        """Verify the provided TOTP token against the user's secret."""
        if user_id not in self.secrets:
            return False
        
        secret = self.secrets[user_id]
        totp = pyotp.TOTP(secret)
        return totp.verify(token)

# Example usage
if __name__ == "__main__":
    two_fa = TwoFactorAuth()

    # Generate a new 2FA secret for a user
    user_id = "user123"
    secret = two_fa.generate_secret(user_id)
    print(f"Generated 2FA secret for {user_id}: {secret}")

    # Get the TOTP URI for the user
    totp_uri = two_fa.get_totp_uri(user_id)
    print(f"TOTP URI for {user_id}: {totp_uri}")

    # Simulate user entering a TOTP token
    token = input("Enter the TOTP token from your authenticator app: ")
    if two_fa.verify_totp(user_id, token):
        print("2FA verification successful!")
    else:
        print("2FA verification failed.")
