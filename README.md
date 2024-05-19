# CMPE 257 Section 2 Spring 2024 Term Project - BitSmart, Machine Learning for Bitcoin Price Prediction and Trading

## Group Members

1. Vivek Saravanan: 017553224
- vivek.saravanan@sjsu.edu

2. Sean Finney: 015961075
- sean.finney@sjsu.edu

3. Sharan Patil: 012488489
- sharanbasavaraj.patil@sjsu.edu

4. Brian Ho: 010631517
- brian.d.ho@sjsu.edu

## URL
[https://cmpe257group9.pythonanywhere.com/](https://cmpe257group9.pythonanywhere.com/)


## Getting Started

Before running `app.py`, ensure you have performed the following steps:

1. **Run `bitsmart.py`:**
   - Execute the `bitsmart.py` script to generate the required `model.pkl` file.
   - This script performs the necessary preprocessing and training to generate the machine learning model used by the application.
   - Example command:
     ```sh
     python bitsmart/bitsmart.py
     ```

2. **Install Dependencies:**
   - Install the required Python dependencies by running:
     ```sh
     pip install -r requirements.txt
     ```

3. **Run `app.py`:**
   - After running `bitsmart.py` and installing dependencies, you can start the Flask application by executing `app.py`.
   - Example command:
     ```sh
     python bitsmart/app.py
     ```