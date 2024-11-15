# This example uses the `simple-smpc` library for secure multi-party computation
# You'll need to install it: pip install simple-smpc

import simple_smpc

def setup_parties(party_count):
    """Sets up parties for secure multi-party communication."""
    parties = []
    for i in range(party_count):
        parties.append(simple_smpc.Party(i, party_count))
    return parties

def secure_sum(parties, values):
    """Securely computes the sum of values across multiple parties."""
    shares = simple_smpc.share_secret(values, parties)
    sum_shares = sum(shares)
    return simple_smpc.reconstruct_secret(sum_shares, parties)

# Example Usage:
if __name__ == "__main__":
    # Set up parties
    parties = setup_parties(3)

    # Values to be summed by each party
    values = [10, 20, 30]

    # Securely calculate the sum
    secure_sum_result = secure_sum(parties, values)

    print("Secure sum:", secure_sum_result ```python
)
