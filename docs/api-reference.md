# API Reference for Eulers Shield

This section provides detailed documentation of the functions, classes, and methods available in Eulers Shield.

## Encryption Module

* **`encrypt_file(file_path, key)`:** Encrypts a file using AES-256 encryption.
   - **`file_path` (str):** The path to the file to be encrypted.
   - **`key` (str):** The encryption key to use.

* **`decrypt_file(file_path, key)`:** Decrypts a previously encrypted file.
   - **`file_path` (str):** The path to the encrypted file.
   - **`key` (str):** The decryption key.

## Key Management Module

* **`generate_key()`:** Generates a secure random encryption key.
   - **Returns:** A string representing the generated key.

* **`store_key(key, storage_path)`:** Stores the encryption key securely.
   - **`key` (str):** The key to store.
   - **`storage_path` (str):** The path where the key will be stored.

## Password Management Module

* **`generate_password(length)`:** Generates a random password of specified length.
   - **`length` (int):** The desired length of the password.
   - **Returns:** A string representing the generated password.

* **`store_password(name, password)`:** Stores a password with an associated name.
   - **`name` (str):** The name or label for the password.
   - **`password` (str):** The password to store.

## Additional Information

For security considerations, refer to [Security Considerations](security.md).
