import pytest
from eulers_shield.encryption import encrypt_file, decrypt_file 

def test_encrypt_decrypt_file(tmp_path):
    """Test that a file can be encrypted and then decrypted correctly."""
    key = "your_secret_key"
    test_file = tmp_path / "test.txt"
    test_file.write_text("This is a test file.") 
    encrypted_file = encrypt_file(str(test_file), key)
    decrypted_file = decrypt_file(encrypted_file, key)
    assert decrypted_file.read_text() == "This is a test file."

def test_encrypt_with_invalid_key(tmp_path):
    """Test that encryption fails with an invalid key."""
    key = "wrong_key" 
    test_file = tmp_path / "test.txt"
    test_file.write_text("This is a test file.") 
    with pytest.raises(ValueError):  # Adjust the exception type if needed
        encrypt_file(str(test_file), key)
