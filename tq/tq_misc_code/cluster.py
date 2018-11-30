from sklearn.cluster import KMeans
from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import scale

import sklearn
import numpy as np 
import pandas as pd

import matplotlib.pyplot as plt

#Sample python file to figure out how k means works
#Define dataset of random points
X = np.array([[2018], [2017], [2016], [1990], [1991], [1992]])
#Apply k means algorithm
kmeans = KMeans(n_clusters=2, random_state=0).fit(X)

#Create a matlib plot to show k means works
df = pd.DataFrame(X)
df.columns = ['Year']

color_theme = np.array(['darkgray', 'lightsalmon'])

plt.subplot(1,1,1)
plt.scatter(x=X,y=X,c=color_theme[kmeans.labels_], s=6)
#We really only need to centers of the k means algorithm
print(kmeans.cluster_centers_[0])
plt.show()
