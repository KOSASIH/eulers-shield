import secrets
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def generate_session_key():
    """Generates a random session key for secure communication."""
    return secrets.token_bytes(32)

def encrypt_data(data, session_key):
    """Encrypts data using the session key with AES-256 CFB."""
    iv = secrets.token_bytes(16)  # Generate a random IV
    cipher = Cipher(algorithms.AES(session_key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(data.encode()) + encryptor.finalize()
    return iv + ciphertext  # Prepend IV for decryption

def decrypt_data(ciphertext, session_key):
    """Decrypts data using the session key with AES-256 CFB."""
    iv = ciphertext[:16]  # Extract the IV
    actual_ciphertext = ciphertext[16:]  # Get the actual ciphertext
    cipher = Cipher(algorithms.AES(session_key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(actual_ciphertext) + decryptor.finalize()
    return decrypted_data.decode()  # Return as string

# Example Usage:
if __name__ == "__main__":
    # Generate a session key
    session_key = generate_session_key()

    # Data to encrypt
    data = "This is a confidential message."

    # Encrypt data
    encrypted_data = encrypt_data(data, session_key)
    print("Encrypted data:", encrypted_data.hex())

    # Decrypt data
    decrypted_data = decrypt_data(encrypted_data, session_key)
    print("Decrypted data:", decrypted_data)
