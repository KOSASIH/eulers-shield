# ai_security/utils/visualization.py

import matplotlib.pyplot as plt
import seaborn as sns
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Visualizer:
    def __init__(self):
        """Initialize the Visualizer."""
        sns.set(style="whitegrid")
        logging.info('Visualizer initialized.')

    def plot_distribution(self, data, feature, title='Feature Distribution'):
        """Plot the distribution of a feature.

        Args:
            data (pd.DataFrame): The input data.
            feature (str): The feature to plot.
            title (str): The title of the plot.
        """
        plt.figure(figsize=(10, 6))
        sns.histplot(data[feature], kde=True , bins=30)
        plt.title(title)
        plt.xlabel(feature)
        plt.ylabel('Frequency')
        plt.show()
        logging.info(f'Distribution plot for {feature} displayed.')

    def plot_correlation_matrix(self, data, title='Correlation Matrix'):
        """Plot the correlation matrix of the features.

        Args:
            data (pd.DataFrame): The input data.
            title (str): The title of the plot.
        """
        plt.figure(figsize=(12, 8))
        correlation = data.corr()
        sns.heatmap(correlation, annot=True, fmt=".2f", cmap='coolwarm', square=True, cbar_kws={"shrink": .8})
        plt.title(title)
        plt.show()
        logging.info('Correlation matrix plot displayed.')

    def plot_confusion_matrix(self, cm, classes, title='Confusion Matrix'):
        """Plot the confusion matrix.

        Args:
            cm (np.ndarray): Confusion matrix.
            classes (list): List of class names.
            title (str): The title of the plot.
        """
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=classes, yticklabels=classes)
        plt.title(title)
        plt.xlabel('Predicted')
        plt.ylabel('True')
        plt.show()
        logging.info('Confusion matrix plot displayed.')

    def plot_feature_importance(self, model, feature_names, title='Feature Importance'):
        """Plot feature importance for tree-based models.

        Args:
            model: Trained model with feature_importances_ attribute.
            feature_names (list): List of feature names.
            title (str): The title of the plot.
        """
        plt.figure(figsize=(10, 6))
        importances = model.feature_importances_
        indices = np.argsort(importances)[::-1]
        plt.title(title)
        plt.bar(range(len(importances)), importances[indices], align='center')
        plt.xticks(range(len(importances)), np.array(feature_names)[indices], rotation=90)
        plt.xlim([-1, len(importances)])
        plt.show()
        logging.info('Feature importance plot displayed.')
