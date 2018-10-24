from sklearn.cluster import KMeans
from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import scale

import sklearn
import numpy as np 
import pandas as pd

import matplotlib.pyplot as plt

X = np.array([[2018], [2017], [2016], [1990], [1991], [1992]])
kmeans = KMeans(n_clusters=2, random_state=0).fit(X)

df = pd.DataFrame(X)
df.columns = ['Year']

color_theme = np.array(['darkgray', 'lightsalmon'])

plt.subplot(1,1,1)
plt.scatter(x=X,y=X,c=color_theme[0], s=6)
plt.show()
