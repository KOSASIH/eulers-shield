from cryptography.fernet import Fernet

def generate_encryption_key():
    """Generates a Fernet encryption key."""
    return Fernet.generate_key()

def encrypt_message(message, key):
    """Encrypts a message using Fernet."""
    f = Fernet(key)
    return f.encrypt(message.encode())

def decrypt_message(ciphertext, key):
    """Decrypts a message using Fernet."""
    f = Fernet(key)
    return f.decrypt(ciphertext).decode()

# Example Usage:
if __name__ == "__main__":
    # Generate a key
    key = generate_encryption_key()

    # Message to encrypt
    message = "This is a secret message!"

    # Encrypt the message
    ciphertext = encrypt_message(message, key)
    print("Encrypted message:", ciphertext.decode())

    # Decrypt the message
    decrypted_message = decrypt_message(ciphertext, key)
    print("Decrypted message:", decrypted_message)
