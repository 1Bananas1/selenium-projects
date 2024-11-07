import pickle
import pandas as pd

def load_model(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

def make_prediction(model, gender, asthma, fever):
    # Convert features into a DataFrame and process them
    input_data = pd.DataFrame([[gender, asthma, fever]], columns=['gender', 'asthma', 'fever'])
    input_data = pd.get_dummies(input_data, columns=['gender', 'asthma'], drop_first=True)
    prediction = model.predict(input_data)
    return prediction[0]
