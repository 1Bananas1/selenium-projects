import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle

# Load data and preprocess (initial or new data)
data = pd.read_csv('covidData.csv')
X = data[['age', 'gender', 'income group', 'asthma', 'fever']]
y = data['status']

# Preprocess features...
X = pd.get_dummies(X, columns=['gender', 'asthma', 'income group'], drop_first=True)

# Train the model
model = RandomForestClassifier()
model.fit(X, y)

# Save the model
with open('covid_predictor.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Model trained and saved to covid_predictor.pkl")
