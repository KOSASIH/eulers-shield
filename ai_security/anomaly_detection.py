import numpy as np
from sklearn.ensemble import IsolationForest

class AnomalyDetection:
    def __init__(self):
        """Initialize the anomaly detection model."""
        self.model = IsolationForest()

    def fit(self, data):
        """Fit the model to the training data."""
        self.model.fit(data)

    def predict(self, data):
        """Predict anomalies in the provided data."""
        predictions = self.model.predict(data)
        return predictions == -1  # Return True for anomalies

# Example Usage
if __name__ == "__main__":
    detector = AnomalyDetection()
    # Sample training data
    training_data = np.array([[1], [2], [3], [4], [5], [100]])
    detector.fit(training_data)

    # Sample data for anomaly detection
    test_data = np.array([[1], [2], [3], [100]])
    anomalies = detector.predict(test_data)
    print("Anomalies detected:", anomalies)
