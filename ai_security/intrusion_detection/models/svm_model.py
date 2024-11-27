# ai_security/intrusion_detection/models/svm_model.py

import logging
import numpy as np
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import GridSearchCV
from joblib import dump, load

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SVMModel:
    def __init__(self):
        """Initialize the SVM model."""
        self.model = SVC()
        logging.info('SVM model initialized.')

    def train(self, X, y):
        """Train the SVM model with hyperparameter tuning.

        Args:
            X (np.ndarray): Training features.
            y (np.ndarray): Training labels.
        """
        param_grid = {
            'C': [0.1, 1, 10, 100],
            'gamma': ['scale', 'auto', 0.01, 0.1, 1],
            'kernel': ['linear', 'rbf', 'poly']
        }
        grid_search = GridSearchCV(SVC(), param_grid, cv=5, scoring='accuracy', n_jobs=-1)
        grid_search.fit(X, y)
        self.model = grid_search.best_estimator_
        logging.info(f'SVM model trained with best parameters: {grid_search.best_params_}')

    def predict(self, X):
        """Make predictions using the SVM model.

        Args:
            X (np.ndarray): Input features for prediction.

        Returns:
            np.ndarray: Predicted labels.
        """
        return self.model.predict(X)

    def evaluate(self, X, y):
        """Evaluate the SVM model.

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
        logging.info('SVM model evaluated.')
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
