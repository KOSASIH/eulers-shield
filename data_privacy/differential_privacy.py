import numpy as np

class DifferentialPrivacy:
    def __init__(self, epsilon):
        """Initialize the differential privacy mechanism with a given epsilon."""
        self.epsilon = epsilon

    def add_noise(self, data):
        """Add Laplace noise to the data for differential privacy."""
        sensitivity = self.calculate_sensitivity(data)
        noise = np.random.laplace(0, sensitivity / self.epsilon, size=len(data))
        return data + noise

    def calculate_sensitivity(self, data):
        """Calculate the sensitivity of the data."""
        # For simplicity, we assume the sensitivity is 1 for each entry
        return 1

# Example Usage:
if __name__ == "__main__":
    # Sample data
    data = np.array([100, 200, 300, 400, 500])

    # Initialize differential privacy with epsilon = 0.5
    dp = DifferentialPrivacy(epsilon=0.5)

    # Add noise to the data
    private_data = dp.add_noise(data)
    print("Original data:", data)
    print("Private data with noise:", private_data)
