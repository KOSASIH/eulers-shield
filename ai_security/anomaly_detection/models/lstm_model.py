# ai_security/anomaly_detection/models/lstm_model.py

import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import MinMaxScaler
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class LSTMAnomalyDetector:
    def __init__(self, input_shape, epochs=50, batch_size=32):
        self.model = self._build_model(input_shape)
        self.epochs = epochs
        self.batch_size = batch_size
        self.scaler = MinMaxScaler()

    def _build_model(self, input_shape):
        model = Sequential()
        model.add(LSTM(50, return_sequences=True, input_shape=input_shape))
        model.add(Dropout(0.2))
        model.add(LSTM(50, return_sequences=False))
        model.add(Dropout(0.2))
        model.add(Dense(1))
        model.compile(optimizer='adam', loss='mean_squared_error')
        return model

    def fit(self, data):
        """Fit the LSTM model to the data."""
        data = self.scaler.fit_transform(data)
        X, y = self._create_dataset(data)
        self.model.fit(X, y, epochs=self.epochs, batch_size=self.batch_size)
        logging.info('LSTM model fitted.')

    def _create_dataset(self, data, time_step=1):
        X, y = [], []
        for i in range(len(data) - time_step - 1):
            X.append(data[i:(i + time_step), 0])
            y.append(data[i + time_step, 0])
        return np.array(X), np.array(y)

    def predict(self, data):
        """Predict anomalies using the LSTM model."""
        data = self.scaler.transform(data)
        X, _ = self._create_dataset(data)
        predictions = self.model.predict(X)
        return self.scaler.inverse_transform(predictions)

    def detect_anomalies(self, data, threshold=1.5):
        """Detect anomalies based on prediction errors."""
        predictions = self.predict(data)
        errors = np.abs(data - predictions)
        anomalies = errors > threshold
        return anomalies

# Example usage:
# if __name__ == "__main__":
#     import pandas as pd
#     data = pd.DataFrame(np.random.randn(100, 1), columns=['Value'])
#     detector = LSTMAnomalyDetector(input_shape=(1, 1))
#     detector.fit(data)
#     anomalies = detector.detect_anomalies(data)
