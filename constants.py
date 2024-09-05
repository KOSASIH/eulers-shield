# eulers_shield/constants.py

"""
Euler's Shield Constants Module
=============================

This module contains essential constants and mathematical formulas
related to Euler's Shield and Pi Coin, a stable cryptocurrency.
"""

# Pi Coin value (USD)
PI_COIN_VALUE = 314.159  # stable coin value

# Euler's Number (approximation)
EULER_NUMBER = 2.718281828459045

# Mathematical constants
PI = 3.141592653589793  # Pi
E = 2.718281828459045  # Euler's Number
PHI = 1.618033988749895  # Golden Ratio

# Cryptographic constants (for Pi Coin transactions)
CRYPTO_SALT = b'\x13\x37\x42\x59'  # random salt value
CRYPTO_ITERATIONS = 10000  # number of iterations for key derivation
HASH_FUNCTION = 'sha3_256'  # hash function for transaction verification

# Euler's Shield algorithm parameters
SHIELD_PRIME = 257  # prime number for Euler's Shield
SHIELD_MODULUS = 65537  # modulus for Euler's Shield
SHIELD_KEY_SIZE = 2048  # key size for Euler's Shield

# Blockchain parameters
BLOCKCHAIN_NAME = 'PiChain'  # name of the blockchain
BLOCKCHAIN_SYMBOL = 'π'  # symbol for the blockchain
BLOCK_TIME = 60  # block time in seconds
BLOCK_REWARD = 10  # block reward in Pi Coins

# Debugging flag
DEBUG_MODE = False

# Pi Coin precision (number of decimal places)
PI_COIN_PRECISION = 8
