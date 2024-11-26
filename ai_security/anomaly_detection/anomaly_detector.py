# ai_security/anomaly_detection/anomaly_detector.py

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
from sklearn.neighbors import LocalOutlierFactor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AnomalyDetector:
    def __init__(self, algorithm='IsolationForest', **kwargs):
        self.algorithm = algorithm
        self.model = self._initialize_model(**kwargs)
        self.scaler = StandardScaler()

    def _initialize_model(self, **kwargs):
        if self.algorithm == 'IsolationForest':
            return IsolationForest(**kwargs)
        elif self.algorithm == 'OneClassSVM':
            return OneClassSVM(**kwargs)
        elif self.algorithm == 'LocalOutlierFactor':
            return LocalOutlierFactor(**kwargs)
        else:
            raise ValueError("Unsupported algorithm: choose 'IsolationForest', 'OneClassSVM', or 'LocalOutlierFactor'.")

    def preprocess_data(self, data):
        """Preprocess the data by scaling and handling missing values."""
        if isinstance(data, pd.DataFrame):
            data.fillna(data.mean(), inplace=True)  # Handle missing values
            return self.scaler.fit_transform(data)
        else:
            raise ValueError("Data must be a pandas DataFrame.")

    def fit(self, data):
        """Fit the model to the data."""
        processed_data = self.preprocess_data(data)
        self.model.fit(processed_data)
        logging.info(f'Model fitted using {self.algorithm}.')

    def predict(self, data):
        """Predict anomalies in the data."""
        processed_data = self.preprocess_data(data)
        predictions = self.model.predict(processed_data)
        return predictions

    def evaluate(self, true_labels, predictions):
        """Evaluate the model's performance."""
        report = classification_report(true_labels, predictions, target_names=['Normal', 'Anomaly'])
        logging.info("Model Evaluation:\n" + report)

    def visualize(self, data, predictions):
        """Visualize the results of the anomaly detection."""
        plt.figure(figsize=(10, 6))
        plt.scatter(data.iloc[:, 0], data.iloc[:, 1], c=predictions, cmap='coolwarm', edgecolor='k', s=20)
        plt.title('Anomaly Detection Results')
        plt.xlabel('Feature 1')
        plt.ylabel('Feature 2')
        plt.colorbar(label='Predicted Class')
        plt.show()

# Example usage:
# if __name__ == "__main__":
#     import pandas as pd
#     data = pd.DataFrame(np.random.randn(100, 2), columns=['Feature1', 'Feature2'])
#     detector = AnomalyDetector(algorithm='IsolationForest', contamination=0.1)
#     detector.fit(data)
#     predictions = detector.predict(data)
#     detector.visualize(data, predictions)
