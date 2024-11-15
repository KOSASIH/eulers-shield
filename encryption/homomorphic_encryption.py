# You'll need to install the SEAL library: pip install seal 
from seal import EncryptionParameters, SEALContext, KeyGenerator, Encryptor, Decryptor, CKKSEncoder, CKKSDecryptor

def generate_keys(poly_modulus_degree, bit_count):
    """Generates encryption keys for CKKS homomorphic encryption."""
    parms = EncryptionParameters(EncryptionParameters.SchemeType.CKKS)
    parms.set_poly_modulus_degree(poly_modulus_degree)
    parms.set_coeff_modulus(
        CKKSEncoder.get_default_params(poly_modulus_degree, bit_count)
    )
    context = SEALContext(parms)
    keygen = KeyGenerator(context)
    public_key = keygen.public_key()
    secret_key = keygen.secret_key()
    return public_key, secret_key

def encrypt_data(data, public_key):
    """Encrypts data using CKKS homomorphic encryption."""
    context = SEALContext.Context(public_key.parms())
    encryptor = Encryptor(context, public_key)
    encoder = CKKSEncoder(context)
    plain = encoder.encode(data)
    ciphertext = encryptor.encrypt(plain)
    return ciphertext

def decrypt_data(ciphertext, secret_key):
    """Decrypts data using CKKS homomorphic encryption."""
    context = SEALContext.Context(secret_key.parms())
    decryptor = Decryptor(context, secret_key)
    encoder = CKKSEncoder(context)
    plain = decryptor.decrypt(ciphertext)
    data = encoder.decode(plain)
    return data

# Example Usage:
if __name__ == "__main__":
    # Set parameters for homomorphic encryption (adjust as needed)
    poly_modulus_degree = 8192
    bit_count = 20
    
    # Generate keys
    public_key, secret_key = generate_keys(poly_modulus_degree, bit_count)

    # Data to encrypt
    data = [1.2, 3.4, 5.6]

    # Encrypt data
    ciphertext = encrypt_data(data, public_key)

    # Decrypt data
    decrypted_data = decrypt_data(ciphertext, secret_key)

    print("Original data:", data)
    print("Decrypted data:", decrypted_data)
