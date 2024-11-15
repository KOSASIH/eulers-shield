import pytest
from eulers_shield.password_management import generate_password, store_password, retrieve_password

def test_generate_password_length():
    """Test that generated passwords are of the specified length."""
    password = generate_password(12)
    assert len(password) == 12

def test_store_retrieve_password():
    """Test that passwords can be stored and retrieved correctly."""
    password = "my_strong_password"
    name = "my_account"
    store_password(name, password)
    retrieved_password = retrieve_password(name)
    assert password == retrieved_password
