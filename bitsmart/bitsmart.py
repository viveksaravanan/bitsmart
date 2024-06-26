import pandas as pd
import numpy as np
import datetime as dt
from datetime import timedelta
import pickle

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

df = pd.read_csv("bitsmart/data/training_data_4.csv")
df['Date'] = pd.to_datetime(df['Date'])
df['Month'] = df['Date'].dt.month
df['Day'] = df['Date'].dt.day
df['Year'] = df['Date'].dt.year
df.replace(',', '', regex=True, inplace=True)

for col in df.columns[1:]:
    df[col] = pd.to_numeric(df[col], errors='coerce')

X = df.drop(columns=['Date','BTC-High', 'BTC-Low', 'BTC-Close'])
y = df[['BTC-High', 'BTC-Low', 'BTC-Close']]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

rf_regressor = RandomForestRegressor(max_depth=90, min_samples_leaf=2, n_estimators=2000)

rf_regressor.fit(X_train, y_train)

pickle.dump(rf_regressor,open('bitsmart/model.pkl', 'wb'))