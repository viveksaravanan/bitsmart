from flask import Flask, render_template, request, flash
import pickle
import pandas as pd
import datetime as dt
import numpy as np
from datetime import timedelta
import warnings
warnings.filterwarnings("ignore")

app = Flask(__name__)
app.secret_key = 'secretkey'

rf_regressor = pickle.load(open('model.pkl', 'rb'))
df = pd.read_csv("bitsmart/training_data_1.csv")
df['Date'] = pd.to_datetime(df['Date'])

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/predict',methods=['POST', 'GET'])
def predict():
    form_date = request.form['datepicker']
    if not form_date:
        flash('Please select a date.')
        return render_template('index.html')

    input_date = pd.to_datetime(form_date)

    subset = df[df['Date'].between(input_date, input_date + pd.Timedelta(days=6))].drop(columns=['Date','BTC-High', 'BTC-Low', 'BTC-Close'])

    predictions = []
    days_in_data = len(subset)

    for index, row in subset.iterrows():
        X_row = row.values.reshape(1,-1)
        prediction = rf_regressor.predict(X_row)
        prediction = np.append(prediction, input_date.strftime('%m/%d/%Y'))
        input_date += dt.timedelta(days=1)
        predictions.append(prediction)
    if days_in_data < 7:
        for i in range(7 - days_in_data):
            X_row[0][0] = predictions[-1][-2]
            X_row[0][-1] = input_date.year
            X_row[0][-2] = input_date.day
            X_row[0][-3] = input_date.month
            prediction = rf_regressor.predict(X_row)
            prediction = np.append(prediction, input_date.strftime('%Y-%m-%d'))
            input_date += dt.timedelta(days=1)
            predictions.append(prediction)
    
    input_date = form_date

    high_prices = [float(arr[0]) for arr in predictions]
    low_prices = [float(arr[1]) for arr in predictions]
    close_prices = [float(arr[2]) for arr in predictions]

    max_high = int(np.round(max(high_prices)))
    min_low = int(np.round(min(low_prices)))
    avg_close = int(np.round(sum(close_prices)/len(close_prices)))

    return render_template('after.html', date=form_date, max_high=max_high, min_low=min_low, avg_close=avg_close)

if __name__ == "__main__":
    app.run(debug=True)