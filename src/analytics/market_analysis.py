import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import joblib
import os

class MarketAnalysis:
    def __init__(self, model_file='market_analysis_model.pkl'):
        self.model_file = model_file
        self.model = None
        self.load_model()

    def load_model(self):
        """Load the pre-trained market analysis model from a file."""
        if os.path.exists(self.model_file):
            self.model = joblib.load(self.model_file)
            print("Market analysis model loaded successfully.")
        else:
            print("No pre-trained model found. Please train a model first.")

    def train_model(self, data_file):
        """Train a market analysis model using historical market data."""
        # Load the dataset
        data = pd.read_csv(data_file)

        # Preprocess the data
        X = data.drop('target_price', axis=1)  # Features
        y = data['target_price']  # Target variable

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train a Random Forest Regressor
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)

        # Evaluate the model
        y_pred = self.model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        print(f"Model trained with Mean Squared Error: {mse:.2f}")

        # Save the trained model
        joblib.dump(self.model, self.model_file)
        print(f"Model trained and saved to {self.model_file}.")

    def predict_price(self, features):
        """Predict the market price based on input features."""
        if self.model is None:
            return "Model not trained. Please train the model first."

        # Convert features to DataFrame
        features_df = pd.DataFrame([features])
        
        # Make a prediction
        predicted_price = self.model.predict(features_df)
        return predicted_price[0]

# Example usage
if __name__ == "__main__":
    market_analyzer = MarketAnalysis()

    # Train the model with historical data
    # Uncomment the line below to train the model with your dataset
    # market_analyzer.train_model('historical_market_data.csv')

    # Example features for prediction
    example_features = {
        'supply': 1000000,         # Example feature
        'demand': 500000,          # Example feature
        'market_sentiment': 0.8,   # Example feature
        'trading_volume': 200000,   # Example feature
        'volatility': 0.05         # Example feature
    }

    predicted_price = market_analyzer.predict_price(example_features)
    print(f"Predicted Market Price: ${predicted_price:.2f}")
