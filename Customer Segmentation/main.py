import pandas as pd 
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
from sklearn.cluster import KMeans
from scipy.cluster.hierarchy import dendrogram, linkage 
import matplotlib.pyplot as plt
from yellowbrick.cluster import KElbowVisualizer

# original CSV
segmentation = pd.read_csv('segmentation.csv')




categorialdata = ['Sex', 'Marital status']


# What does our data look like for unique
# print(segmentation['Settlement size'].unique())

#Normal Encoding
occupation_rank = ['Unemployed', 'Skilled Employee', 'Management']
education_rank = ['Unknown', 'High School', 'University', 'Graduate School']
settlement_rank = ['Small City', 'Mid-sized City', 'Big City']


# #occupation
# # 0 = smallest and or worst
# # max = largest or best

enc = OrdinalEncoder(categories= [occupation_rank])
enc.fit_transform(segmentation[['Occupation']])
segmentation['Occupation'] = enc.fit_transform(segmentation[['Occupation']])



# #education
enc = OrdinalEncoder(categories= [education_rank])
enc.fit_transform(segmentation[['Education']])
segmentation['Education'] = enc.fit_transform(segmentation[['Education']])

# #Settlement Size
enc = OrdinalEncoder(categories= [settlement_rank])
enc.fit_transform(segmentation[['Settlement size']])
segmentation['Settlement size'] = enc.fit_transform(segmentation[['Settlement size']])


# One Hot Encoding:
# Transfer categorical data into nonordinal data
ohe = OneHotEncoder(handle_unknown='ignore', sparse_output=False).set_output(transform='pandas')

# Change all of my catagroical data into OHE
for categorical_data_column in categorialdata:
    ohetransform = ohe.fit_transform(segmentation[[categorical_data_column]])
    segmentation = pd.concat([segmentation,ohetransform], axis=1).drop(columns = categorical_data_column)

segmentation.drop('ID',axis=1,inplace=True)
print(segmentation)
#there is absolutely no reason that ID should have any impact on our data so i dropped it

# segmentation.to_csv('OneHotEncodingSegmentation.csv')


#
#
# OK, Encoding and OneHotEncoding done, now time for PCA!
#
#

# tbh the scikit learn PCA tutorial confused me so I used statsbuddy, woopsies

#   PC1    PC2    PC3    PC4    PC5    PC6    PC7    PC8    PC9 
# 39.084 25.535 15.979  9.181  5.438  3.096  1.686  0.000  0.000 


segmentationALLPCA = pd.read_csv('OneHotEncodingSegmentation_PCA.csv')




segmentationSelectedPCA = segmentationALLPCA[['PC1','PC2','PC3','PC4','PC5']]



z = linkage(segmentationSelectedPCA.sample(n=200))
# dendrogram(z)
# plt.show()


# km = KMeans()
# visualizer = KElbowVisualizer(km, k=(5,10))
# visualizer.fit(z)        # Fit the data to the visualizer
# visualizer.show() 

kmeans = KMeans(n_clusters=7)
kmeans.fit(segmentationSelectedPCA)
labels = kmeans.labels_
segmentation['cluster'] = labels


segmentation.to_csv('clusters.csv')