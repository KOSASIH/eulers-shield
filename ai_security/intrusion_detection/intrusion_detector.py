# ai_security/intrusion_detection/intrusion_detector.py

import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from .models.svm_model import SVMModel
from .models.random_forest_model import RandomForestModel

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class IntrusionDetector:
    def __init__(self, model_type='svm'):
        """Initialize the intrusion detector with a specified model type.

        Args:
            model_type (str): The type of model to use ('svm' or 'random_forest').
        """
        if model_type == 'svm':
            self.model = SVMModel()
        elif model_type == 'random_forest':
            self.model = RandomForestModel()
        else:
            raise ValueError("Model type must be 'svm' or 'random_forest'.")
        logging.info(f'Intrusion detector initialized with {model_type} model.')

    def train(self, data, labels, test_size=0.2):
        """Train the intrusion detection model.

        Args:
            data (pd.DataFrame): The input features for training.
            labels (pd.Series): The target labels for training.
            test_size (float): The proportion of the dataset to include in the test split.
        """
        X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=test_size, random_state=42)
        self.model.train(X_train, y_train)
        accuracy = self.model.evaluate(X_test, y_test)
        logging.info(f'Model trained with accuracy: {accuracy:.2f}')

    def predict(self, data):
        """Make predictions on new data.

        Args:
            data (pd.DataFrame): The input features for prediction.

        Returns:
            np.ndarray: Predicted labels.
        """
        return self.model.predict(data)

# Example usage:
# if __name__ == "__main__":
#     # Load your dataset here
#     # data = pd.read_csv('path/to/dataset.csv')
#     # labels = data['label']
#     intrusion_detector = IntrusionDetector(model_type='svm')
#     intrusion_detector.train(data.drop(columns=['label']), labels)
#     # Make predictions
#     # predictions = intrusion_detector.predict(new_data)
