import pytest
from eulers_shield.key_management import generate_key, store_key, load_key

def test_generate_key_length():
    """Test that generated keys are of the expected length."""
    key = generate_key()
    assert len(key) == 32  # Assuming AES-256 

def test_store_load_key(tmp_path):
    """Test that keys can be stored and loaded correctly."""
    key = generate_key()
    key_file = tmp_path / "key.txt"
    store_key(key, str(key_file))
    loaded_key = load_key(str(key_file))
    assert key == loaded_key
