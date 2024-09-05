# aimm.py

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.callbacks import EarlyStopping
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from scipy.stats import norm
from scipy.optimize import minimize

class AI_Market_Maker:
    def __init__(self, data, target, features, test_size=0.2, random_state=42):
        self.data = data
        self.target = target
        self.features = features
        self.test_size = test_size
        self.random_state = random_state
        self.X_train, self.X_test, self.y_train, self.y_test = self.split_data()
        self.scaler = StandardScaler()
        self.X_train_scaled = self.scaler.fit_transform(self.X_train)
        self.X_test_scaled = self.scaler.transform(self.X_test)
        self.model = self.create_model()

    def split_data(self):
        return train_test_split(self.data[self.features], self.data[self.target], test_size=self.test_size, random_state=self.random_state)

    def create_model(self):
        model = Sequential()
        model.add(LSTM(units=50, return_sequences=True, input_shape=(self.X_train_scaled.shape[1], 1)))
        model.add(LSTM(units=50))
        model.add(Dense(1))
        model.compile(loss='mean_squared_error', optimizer='adam')
        return model

    def train_model(self, epochs=100, batch_size=32, verbose=0):
        early_stopping = EarlyStopping(monitor='val_loss', patience=5, min_delta=0.001)
        self.model.fit(self.X_train_scaled, self.y_train, epochs=epochs, batch_size=batch_size, validation_data=(self.X_test_scaled, self.y_test), callbacks=[early_stopping], verbose=verbose)

    def evaluate_model(self):
        y_pred = self.model.predict(self.X_test_scaled)
        return mean_squared_error(self.y_test, y_pred)

    def make_predictions(self, data):
        data_scaled = self.scaler.transform(data)
        return self.model.predict(data_scaled)

    def plot_predictions(self, data, predictions):
        plt.plot(data[self.target], label='Actual')
        plt.plot(predictions, label='Predicted')
        plt.legend()
        plt.show()

    def analyze_stationarity(self):
        adf_test = adfuller(self.data[self.target])
        print('ADF Statistic:', adf_test[0])
        print('p-value:', adf_test[1])
        plot_acf(self.data[self.target])
        plot_pacf(self.data[self.target])
        plt.show()

    def optimize_hyperparameters(self):
        def objective(params):
            self.model = self.create_model()
            self.model.compile(loss='mean_squared_error', optimizer='adam')
            self.train_model(epochs=params[0], batch_size=params[1], verbose=0)
            return self.evaluate_model()

        bounds = [(10, 100), (16, 64)]
        result = minimize(objective, [50, 32], method='SLSQP', bounds=bounds)
        print('Optimal Hyperparameters:', result.x)

    def feature_importance(self):
        importance = self.model.feature_importances_
        plt.barh(range(len(importance)), importance)
        plt.xlabel('Importance')
        plt.ylabel('Feature')
        plt.show()

    def correlation_matrix(self):
        corr_matrix = self.data.corr()
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', square=True)
        plt.show()

    def arima_model(self):
        model = ARIMA(self.data[self.target], order=(1,1,1))
        model_fit = model.fit()
        print('ARIMA Model Summary:')
        print(model_fit.summary())
        return model_fit

    def forecast(self, steps):
        model_fit = self.arima_model()
        forecast = model_fit.forecast(steps=steps)
        return forecast
