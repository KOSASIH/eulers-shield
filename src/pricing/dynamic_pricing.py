import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib
import os

class DynamicPricing:
    def __init__(self, model_file='dynamic_pricing_model.pkl'):
        self.model_file = model_file
        self.model = None
        self.scaler = StandardScaler()
        self.load_model()

    def load_model(self):
        """Load the pre-trained pricing model from a file."""
        if os.path.exists(self.model_file):
            self.model = joblib.load(self.model_file)
            print("Model loaded successfully.")
        else:
            print("No pre-trained model found. Please train a model first.")

    def train_model(self, data_file):
        """Train a dynamic pricing model using historical market data."""
        # Load the dataset
        data = pd.read_csv(data_file)

        # Preprocess the data
        X = data[['supply', 'demand', 'market_sentiment']]  # Features
        y = data['price']  # Target variable

        # Scale the features
        X_scaled = self.scaler.fit_transform(X)

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

        # Train a Linear Regression model
        self.model = LinearRegression()
        self.model.fit(X_train, y_train)

        # Evaluate the model
        score = self.model.score(X_test, y_test)
        print(f"Model trained with R^2 score: {score:.2f}")

        # Save the trained model
        joblib.dump(self.model, self.model_file)
        print(f"Model trained and saved to {self.model_file}.")

    def predict_price(self, supply, demand, market_sentiment):
        """Predict the price based on supply, demand, and market sentiment."""
        if self.model is None:
            return "Model not trained. Please train the model first."

        # Scale the input features
        input_data = np.array([[supply, demand, market_sentiment]])
        input_scaled = self.scaler.transform(input_data)

        # Make a prediction
        predicted_price = self.model.predict(input_scaled)
        return predicted_price[0]

# Example usage
if __name__ == "__main__":
    pricing_model = DynamicPricing()

    # Train the model with historical data
    # Uncomment the line below to train the model with your dataset
    # pricing_model.train_model('historical_market_data.csv')

    # Example prediction
    supply = 1000000  # Example supply
    demand = 500000   # Example demand
    market_sentiment = 0.8  # Example market sentiment (0 to 1 scale)

    predicted_price = pricing_model.predict_price(supply, demand, market_sentiment)
    print(f"Predicted Price: ${predicted_price:.2f}")
