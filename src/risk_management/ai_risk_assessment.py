import json
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

class AIRiskAssessment:
    def __init__(self, model_file='risk_assessment_model.pkl', data_file='user_transactions.json'):
        self.model_file = model_file
        self.data_file = data_file
        self.model = None
        self.load_data()
        self.load_model()

    def load_data(self):
        """Load user transaction data from a JSON file."""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as file:
                self.data = json.load(file)
                self.df = pd.DataFrame(self.data)
        else:
            self.df = pd.DataFrame()

    def save_data(self):
        """Save user transaction data to a JSON file."""
        with open(self.data_file, 'w') as file:
            json.dump(self.data, file)

    def train_model(self):
        """Train a risk assessment model using user transaction data."""
        if self.df.empty:
            print("No data available for training.")
            return

        # Prepare the data
        X = self.df.drop('risk_label', axis=1)  # Features
        y = self.df['risk_label']  # Target variable

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

    def load_model(self):
        """Load the pre-trained risk assessment model from a file."""
        if os.path.exists(self.model_file):
            self.model = joblib.load(self.model_file)
            print("Risk assessment model loaded successfully.")
        else:
            print("No pre-trained model found. Please train a model first.")

    def assess_risk(self, user_data):
        """Assess risk based on input user data."""
        if self.model is None:
            return "Model not trained. Please train the model first."

        # Convert user data to DataFrame
        user_df = pd.DataFrame([user_data])
        
        # Make a prediction
        risk_prediction = self.model.predict(user_df)
        return risk_prediction[0]

# Example usage
if __name__ == "__main__":
    risk_assessment = AIRiskAssessment()

    # Train the model with historical data
    # Uncomment the line below to train the model with your dataset
    # risk_assessment.train_model()

    # Example user data for risk assessment
    example_user_data = {
        'transaction_amount': 5000,  # Example feature
        'transaction_frequency': 10,  # Example feature
        'account_age': 2,             # Example feature (in years)
        'previous_risks': 1           # Example feature (number of previous risk flags)
    }

    risk_level = risk_assessment.assess_risk(example_user_data)
    print(f"Predicted Risk Level: {risk_level}")
