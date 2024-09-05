# css.py

import hashlib
import hmac
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

class CybersecurityShield:
    def __init__(self, private_key, password):
        self.private_key = private_key
        self.password = password
        self.kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'cybersecurityshield',
            iterations=100000,
            backend=default_backend()
        )
        self.key = self.kdf.derive(self.password.encode())

    def encrypt(self, data):
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(b'\00' * 16), backend=default_backend())
        encryptor = cipher.encryptor()
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(data) + padder.finalize()
        return encryptor.update(padded_data) + encryptor.finalize()

    def decrypt(self, encrypted_data):
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(b'\00' * 16), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
        unpadder = padding.PKCS7(128).unpadder()
        return unpadder.update(decrypted_padded_data) + unpadder.finalize()

    def sign(self, data):
        signer = hmac.HMAC(self.key, hashes.SHA256(), default_backend())
        signer.update(data)
        return signer.finalize()

    def verify(self, data, signature):
        verifier = hmac.HMAC(self.key, hashes.SHA256(), default_backend())
        verifier.update(data)
        return hmac.compare_digest(verifier.finalize(), signature)

    def generate_private_key(self):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        return private_key

    def get_private_key(self):
        return self.private_key

    def set_private_key(self, private_key):
        self.private_key = private_key

    def get_password(self):
        return self.password

    def set_password(self, password):
        self.password = password
        self.kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'cybersecurityshield',
            iterations=100000,
            backend=default_backend()
        )
        self.key = self.kdf.derive(self.password.encode())
