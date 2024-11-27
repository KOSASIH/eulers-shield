# ai_security/utils/data_preprocessing.py

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DataPreprocessor:
    def __init__(self, numerical_features, categorical_features):
        """Initialize the DataPreprocessor.

        Args:
            numerical_features (list): List of numerical feature names.
            categorical_features (list): List of categorical feature names.
        """
        self.numerical_features = numerical_features
        self.categorical_features = categorical_features
        self.pipeline = self.create_pipeline()
        logging.info('DataPreprocessor initialized.')

    def create_pipeline(self):
        """Create a preprocessing pipeline for numerical and categorical features.

        Returns:
            sklearn.pipeline.Pipeline: The preprocessing pipeline.
        """
        numerical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='mean')),
            ('scaler', StandardScaler())
        ])

        categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('onehot', OneHotEncoder(handle_unknown='ignore'))
        ])

        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numerical_transformer, self.numerical_features),
                ('cat', categorical_transformer, self.categorical_features)
            ]
        )
        return preprocessor

    def fit_transform(self, X, y=None):
        """Fit the pipeline to the data and transform it.

        Args:
            X (pd.DataFrame): The input features.
            y (pd.Series, optional): The target labels.

        Returns:
            np.ndarray: The transformed features.
        """
        transformed_X = self.pipeline.fit_transform(X)
        logging.info('Data preprocessing completed.')
        return transformed_X

    def transform(self, X):
        """Transform the data using the fitted pipeline.

        Args:
            X (pd.DataFrame): The input features.

        Returns:
            np.ndarray: The transformed features.
        """
        transformed_X = self.pipeline.transform(X)
        logging.info('Data transformation completed.')
        return transformed_X

    def split_data(self, X, y, test_size=0.2, random_state=42):
        """Split the data into training and testing sets.

        Args:
            X (pd.DataFrame): The input features.
            y (pd.Series): The target labels.
            test_size (float): The proportion of the dataset to include in the test split.
            random_state (int): Random seed for reproducibility.

        Returns:
            tuple: Split data (X_train, X_test, y_train, y_test).
        """
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
        logging.info('Data split into training and testing sets.')
        return X_train, X_test, y_train, y_test
