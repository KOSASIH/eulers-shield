# anomaly_detection.py

import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.preprocessing import StandardScaler

class AnomalyDetector:
    def __init__(self, algorithm, contamination=0.1):
        self.algorithm = algorithm
        self.contamination = contamination
        self.model = self.select_algorithm(algorithm)

    def select_algorithm(self, algorithm):
        if algorithm == 'isolation_forest':
            return IsolationForest(contamination=self.contamination)
        elif algorithm == 'one_class_svm':
            return OneClassSVM(kernel='rbf', gamma=0.1, nu=0.1)
        else:
            raise ValueError('Invalid algorithm. Supported algorithms are isolation_forest and one_class_svm.')

    def fit(self, X):
        self.model.fit(X)

    def predict(self, X):
        return self.model.predict(X)

    def evaluate(self, y_true, y_pred):
        accuracy = accuracy_score(y_true, y_pred)
        precision = precision_score(y_true, y_pred)
        recall = recall_score(y_true, y_pred)
        f1 = f1_score(y_true, y_pred)
        return accuracy, precision, recall, f1

    def detect_anomalies(self, data):
        X = data.drop(['label'], axis=1)
        y = data['label']
        self.fit(X)
        y_pred = self.predict(X)
        accuracy, precision, recall, f1 = self.evaluate(y, y_pred)
        print(f'Accuracy: {accuracy:.3f}, Precision: {precision:.3f}, Recall: {recall:.3f}, F1: {f1:.3f}')
        return y_pred

    def visualize_anomalies(self, data, y_pred):
        import matplotlib.pyplot as plt
        plt.scatter(data[:, 0], data[:, 1], c=y_pred)
        plt.xlabel('Feature 1')
        plt.ylabel('Feature 2')
        plt.title('Anomaly Detection')
        plt.show()

# Example usage:
data = pd.read_csv('anomaly_data.csv')
anomaly_detector = AnomalyDetector(algorithm='isolation_forest')
y_pred = anomaly_detector.detect_anomalies(data)
anomaly_detector.visualize_anomalies(data.drop(['label'], axis=1), y_pred)
