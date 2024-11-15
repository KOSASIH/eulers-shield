import numpy as np

def add_laplace_noise(data, epsilon):
    """Adds Laplace noise to data for differential privacy."""
    sensitivity = 1  # Assuming sensitivity of 1 for your data
    scale = sensitivity / epsilon
    noise = np.random.laplace(scale=scale)
    return data + noise

# Example Usage:
if __name__ == "__main__":
    # Original data (example: number of users in each city)
    original_data = np.array([100, 250, 150, 300]) 

    # Privacy parameter (epsilon)
    epsilon = 1.0

    # Add Laplace noise
    noisy_data = add_laplace_noise(original_data, epsilon)

    print("Original data:", original_data)
    print("Noisy data:", noisy_data)
