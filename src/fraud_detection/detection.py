import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import os

class FraudDetector:
    def __init__(self, model_file='fraud_model.pkl'):
        self.model_file = model_file
        self.model = None
        self.load_model()

    def load_model(self):
        """Load the pre-trained model from a file."""
        if os.path.exists(self.model_file):
            self.model = joblib.load(self.model_file)
        else:
            print("No pre-trained model found. Please train a model first.")

    def train_model(self, data_file):
        """Train a fraud detection model using historical transaction data."""
        # Load the dataset
        data = pd.read_csv(data_file)

        # Preprocess the data
        X = data.drop('is_fraud', axis=1)  # Features
        y = data['is_fraud']  # Target variable

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train a Random Forest Classifier
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)

        # Evaluate the model
        y_pred = self.model.predict(X_test)
        print(classification_report(y_test, y_pred))

        # Save the trained model
        joblib.dump(self.model, self.model_file)
        print(f"Model trained and saved to {self.model_file}.")

    def detect_fraud(self, transaction):
        """Detect fraud in a given transaction."""
        if self.model is None:
            return "Model not trained. Please train the model first."

        # Convert the transaction to a DataFrame
        transaction_df = pd.DataFrame([transaction])

        # Make a prediction
        prediction = self.model.predict(transaction_df)
        return prediction[0] == 1  # Return True if fraud is detected

# Example usage
if __name__ == "__main__":
    detector = FraudDetector()

    # Train the model with historical data
    # Uncomment the line below to train the model with your dataset
    # detector.train_model('historical_transactions.csv')

    # Example transaction to check for fraud
    example_transaction = {
        'amount': 1000,
        'transaction_type': 1,  # Example feature
        'user_id': 12345,       # Example feature
        'timestamp': 1625250000  # Example feature
    }

    is_fraud = detector.detect_fraud(example_transaction)
    print(f"Fraud detected: {is_fraud}")
