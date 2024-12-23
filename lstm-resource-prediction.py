import numpy as np
import pandas as pd
import json
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import MinMaxScaler

def load_charging_history(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def preprocess_data(data):
    data_scaled = MinMaxScaler(feature_range=(0, 1)).fit_transform(data)
    return data_scaled

def create_dataset(data, time_step=1):
    X, y = [], []
    for i in range(len(data) - time_step - 1):
        X.append(data[i:(i + time_step), 0])
        y.append(data[i + time_step, 0])
    return np.array(X), np.array(y)

def build_lstm_model(input_shape):
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=input_shape))
    model.add(Dropout(0.2))
    model.add(LSTM(50))
    model.add(Dropout(0.2))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

def predict_resource_usage(charging_history, threshold):
    results = {}
    for station_id, matrix in charging_history.items():
        data = np.array(matrix)
        data_scaled = preprocess_data(data)
        X, y = create_dataset(data_scaled, time_step=10)

        X = X.reshape(X.shape[0], X.shape[1], 1)
        model = build_lstm_model((X.shape[1], 1))
        model.fit(X, y, epochs=50, batch_size=32, verbose=0)

        predictions = model.predict(X)
        average_usage = np.mean(predictions)
        results[station_id] = 'overloaded' if average_usage > threshold else 'underloaded'
    return results

if __name__ == "__main__":
    charging_history = load_charging_history('charging_history.json')
    threshold = 0.7  
    state = predict_resource_usage(charging_history, threshold)
    print(state)
