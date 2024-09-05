# lstm.py

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.optimizers import Adam
from keras.regularizers import L1L2

class LSTMModel:
    def __init__(self, data, target, features, seq_len, batch_size, epochs, units, dropout, recurrent_dropout, l1, l2):
        self.data = data
        self.target = target
        self.features = features
        self.seq_len = seq_len
        self.batch_size = batch_size
        self.epochs = epochs
        self.units = units
        self.dropout = dropout
        self.recurrent_dropout = recurrent_dropout
        self.l1 = l1
        self.l2 = l2
        self.scaler = MinMaxScaler()
        self.X_train, self.X_test, self.y_train, self.y_test = self.split_data()
        self.model = self.create_model()

    def split_data(self):
        X = self.data[self.features]
        y = self.data[self.target]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        return X_train, X_test, y_train, y_test

    def create_model(self):
        model = Sequential()
        model.add(LSTM(units=self.units, return_sequences=True, input_shape=(self.seq_len, len(self.features)), 
                        dropout=self.dropout, recurrent_dropout=self.recurrent_dropout, 
                        kernel_regularizer=L1L2(l1=self.l1, l2=self.l2)))
        model.add(Dropout(self.dropout))
        model.add(LSTM(units=self.units, return_sequences=False, dropout=self.dropout, recurrent_dropout=self.recurrent_dropout, 
                        kernel_regularizer=L1L2(l1=self.l1, l2=self.l2)))
        model.add(Dropout(self.dropout))
        model.add(Dense(1))
        model.compile(loss='mean_squared_error', optimizer=Adam(lr=0.001))
        return model

    def train_model(self):
        early_stopping = EarlyStopping(monitor='val_loss', patience=5, min_delta=0.001)
        model_checkpoint = ModelCheckpoint('lstm_model.h5', monitor='val_loss', save_best_only=True, mode='min')
        self.model.fit(self.X_train, self.y_train, epochs=self.epochs, batch_size=self.batch_size, 
                        validation_data=(self.X_test, self.y_test), callbacks=[early_stopping, model_checkpoint], verbose=0)

    def evaluate_model(self):
        y_pred = self.model.predict(self.X_test)
        return mean_squared_error(self.y_test, y_pred)

    def make_predictions(self, data):
        data_scaled = self.scaler.transform(data)
        return self.model.predict(data_scaled)

    def plot_predictions(self, data, predictions):
        plt.plot(data[self.target], label='Actual')
        plt.plot(predictions, label='Predicted')
        plt.legend()
        plt.show()
