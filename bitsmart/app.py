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

rf_regressor = pickle.load(open('bitsmart/model.pkl', 'rb'))

df = pd.read_csv("bitsmart/data/training_data_4.csv")
df['Date'] = pd.to_datetime(df['Date'])
df['Month'] = df['Date'].dt.month
df['Day'] = df['Date'].dt.day
df['Year'] = df['Date'].dt.year
df.replace(',', '', regex=True, inplace=True)

for col in df.columns[1:]:
    df[col] = pd.to_numeric(df[col], errors='coerce')

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

    subset = df[df['Date'].between(input_date, input_date + pd.Timedelta(days=7))].drop(columns=['Date','BTC-High', 'BTC-Low', 'BTC-Close'])

    predictions = []
    days_in_data = len(subset)

    for index, row in subset.iterrows():
        X_row = row.values.reshape(1,-1)
        prediction = rf_regressor.predict(X_row)
        prediction = np.append(prediction, input_date.strftime('%m/%d/%Y'))
        input_date += dt.timedelta(days=1)
        predictions.append(prediction)
    if days_in_data < 8:
        for i in range(8 - days_in_data):
            X_row[0][0] = predictions[-1][-2]
            X_row[0][-1] = input_date.year
            X_row[0][-2] = input_date.day
            X_row[0][-3] = input_date.month
            prediction = rf_regressor.predict(X_row)
            prediction = np.append(prediction, input_date.strftime('%Y-%m-%d'))
            input_date += dt.timedelta(days=1)
            predictions.append(prediction)
    
    predictions = predictions[1:]
    input_date = pd.to_datetime(form_date) + dt.timedelta(days=1)

    high_prices = [float(arr[0]) for arr in predictions]
    low_prices = [float(arr[1]) for arr in predictions]
    close_prices = [float(arr[2]) for arr in predictions]

    max_high = int(np.round(max(high_prices)))
    min_low = int(np.round(min(low_prices)))
    avg_close = int(np.round(sum(close_prices)/len(close_prices)))

    dates = maxProfit(close_prices)
    print(close_prices)
    if dates == []:
        # if prices just rise, we won't find a max profit
        # no reason to sell or buy
        sell_all = "N/A"
        all_in = "N/A"
    else:
        sell = input_date + dt.timedelta(days=dates[0])
        buy = input_date + dt.timedelta(days=dates[1])
        sell_all = sell.strftime("%m/%d/%Y")
        if dates[1] == 6:
            # if prices only fall, max profit comes from buying at the end
            # don't need to buy at all in that case
            all_in = "N/A"
        else:
            all_in = buy.strftime("%m/%d/%Y")

    return render_template('after.html', date=form_date, max_high=max_high, min_low=min_low, avg_close=avg_close, sell_all=sell_all, all_in=all_in)

# swing trading code
def maxProfit(prices):
        profit = 0
        sell = prices[0]
        result = []
        sell_i = 0
        i = 0
        r = []
        for buy in prices[1:]:
            i += 1
            if sell > buy:
                if profit < sell - buy:
                   profit = sell - buy
                   result.append([profit, sell_i, i])
            else:
                sell = buy
                sell_i += 1
        for item in result:
            if item[0] == profit:
                r = [item[1], item[2]]
        print(result)
        return r

if __name__ == "__main__":
    app.run(debug=True)