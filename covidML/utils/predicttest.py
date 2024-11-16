from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
import pandas as pd
import sys, os


dataframe = pd.read_csv('test.csv')

dataframe.drop('age',axis=1,inplace=True)

X = dataframe.iloc[:,1:8]
Y = dataframe.iloc[:,-1]

best_features= SelectKBest(score_func=chi2, k=3)
fit= best_features.fit(X,Y)

df_scores= pd.DataFrame(fit.scores_)
df_columns= pd.DataFrame(X.columns)

features_scores= pd.concat([df_columns, df_scores], axis=1)
features_scores.columns= ['Features', 'Score']
features_scores.sort_values(by = 'Score')

print(features_scores)