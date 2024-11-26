# ai_security/anomaly_detection/models/prophet_model.py

import pandas as pd
from fbprophet import Prophet
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ProphetAnomalyDetector:
    def __init__(self):
        self.model = Prophet()

    def fit(self, data):
        """Fit the Prophet model to the data."""
        if not isinstance(data, pd.DataFrame) or 'Value' not in data.columns:
            raise ValueError("Data must be a pandas DataFrame with a 'Value' column.")
        
        # Prepare the data for Prophet
        data = data.reset_index().rename(columns={'index': 'ds', 'Value': 'y'})
        self.model.fit(data)
        logging.info('Prophet model fitted.')

    def predict(self, periods=30):
        """Make future predictions."""
        future = self.model.make_future_dataframe(periods=periods)
        forecast = self.model.predict(future)
        logging.info('Future predictions made.')
        return forecast

    def detect_anomalies(self, data, threshold=1.5):
        """Detect anomalies based on forecasted values."""
        if not isinstance(data, pd.DataFrame) or 'Value' not in data.columns:
            raise ValueError("Data must be a pandas DataFrame with a 'Value' column.")
        
        # Prepare the data for Prophet
        data = data.reset_index().rename(columns={'index': 'ds', 'Value': 'y'})
        forecast = self.predict(len(data))
        
        # Merge actual and forecasted values
        merged = pd.merge(data, forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']], on='ds', how='left')
        
        # Identify anomalies
        anomalies = []
        for i in range(len(merged)):
            actual = merged['y'].iloc[i]
            predicted = merged['yhat'].iloc[i]
            if abs(actual - predicted) > threshold:
                anomalies.append((merged['ds'].iloc[i], actual, predicted))
        
        logging.info(f'Detected {len(anomalies)} anomalies.')
        return anomalies

    def evaluate(self, data, threshold=1.5):
        """Evaluate the Prophet model's performance."""
        anomalies = self.detect_anomalies(data, threshold)
        if not anomalies:
            logging.info('No anomalies detected.')
            return 0.0
        
        # Calculate accuracy based on detected anomalies
        actual_anomalies = data[data['anomaly'] == 1]  # Assuming 'anomaly' column exists
        detected_anomalies = len(anomalies)
        true_positive = len([a for a in anomalies if a[1] in actual_anomalies['Value'].values])
        
        accuracy = true_positive / detected_anomalies if detected_anomalies > 0 else 0.0
        logging.info(f'Prophet model accuracy: {accuracy:.3f}')
        return accuracy

# Example usage:
# if __name__ == "__main__":
#     import pandas as pd
#     # Create a sample DataFrame with a 'Value' column
#     data = pd.DataFrame({
#         'Value': [10, 12, 11, 13, 15, 14, 100, 12, 11, 10, 9, 8, 7, 6, 5]
#     })
#     data['anomaly'] = [0] * 14 + [1]  # Mark the last value as an anomaly
#     detector = ProphetAnomalyDetector()
#     detector.fit(data)
#     anomalies = detector.detect_anomalies(data)
#     accuracy = detector.evaluate(data)
