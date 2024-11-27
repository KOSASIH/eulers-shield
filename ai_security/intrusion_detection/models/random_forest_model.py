# ai_security/intrusion_detection/models/random_forest_model.py

import logging
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import GridSearchCV
from joblib import dump, load

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class RandomForestModel:
    def __init__(self):
        """Initialize the Random Forest model."""
        self.model = RandomForestClassifier(random_state=42)
        logging.info('Random Forest model initialized.')

    def train(self, X, y):
        """Train the Random Forest model with hyperparameter tuning.

        Args:
            X (np.ndarray): Training features.
            y (np.ndarray): Training labels.
        """
        param_grid = {
            'n_estimators': [50, 100, 200],
            'max_features': ['auto', 'sqrt'],
            'max_depth': [None, 10, 20, 30],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4]
        }
        grid_search = GridSearchCV(RandomForestClassifier(random_state=42), param_grid, cv=5, scoring='accuracy', n_jobs=-1)
        grid_search.fit(X, y)
        self.model = grid_search.best_estimator_
        logging.info(f'Random Forest model trained with best parameters: {grid_search.best_params _}')

    def predict(self, X):
        """Make predictions using the Random Forest model.

        Args:
            X (np.ndarray): Input features for prediction.

        Returns:
            np.ndarray: Predicted labels.
        """
        return self.model.predict(X)

    def evaluate(self, X, y):
        """Evaluate the Random Forest model.

        Args:
            X (np.ndarray): Test features.
            y (np.ndarray): Test labels.

        Returns:
            dict: A dictionary containing accuracy and classification report.
        """
        predictions = self.model.predict(X)
        accuracy = accuracy_score(y, predictions)
        report = classification_report(y, predictions)
        cm = confusion_matrix(y, predictions)
        logging.info('Random Forest model evaluated.')
        return {
            'accuracy': accuracy,
            'classification_report': report,
            'confusion_matrix': cm
        }

    def save_model(self, filename):
        """Save the trained model to a file.

        Args:
            filename (str): The filename to save the model.
        """
        dump(self.model, filename)
        logging.info(f'Model saved to {filename}.')

    def load_model(self, filename):
        """Load a model from a file.

        Args:
            filename (str): The filename to load the model from.
        """
        self.model = load(filename)
        logging.info(f'Model loaded from {filename}.')
