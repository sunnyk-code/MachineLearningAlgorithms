# -*- coding: utf-8 -*-
"""KNNClassifier.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UuiMkG_dmgC6zyv5E5bCt8fZEDT-Yn5Z
"""

# Commented out IPython magic to ensure Python compatibility.
import itertools
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter
import pandas as pd
import numpy as np
import matplotlib.ticker as ticker
from sklearn import preprocessing
# %matplotlib inline

#Import data from IBM Storage (Telecommunications service customer classification)
!wget -O teleCust1000t.csv https://s3-api.us-geo.objectstorage.softlayer.net/cf-courses-data/CognitiveClass/ML0101ENv3/labs/teleCust1000t.csv

df = pd.read_csv("teleCust1000t.csv")
df.head()

# num in each class
df['custcat'].value_counts()

df.hist(column = 'income' , bins = 70)

df.columns
toNP = df[['region', 'tenure', 'age', 'marital', 'address', 'income', 'ed','employ', 'retire', 'gender', 'reside', 'custcat']].values
toNP[0:5]

yVals = df['custcat'].values
yVals[0:5]

toNP = preprocessing.StandardScaler().fit(toNP).transform(toNP.astype(float))
toNP[0:5]



from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(toNP, yVals, test_size = 0.2, random_state = 6 )
print ('Train set:' , x_train.shape , y_train.shape)
print('Test set: X:' , x_test.shape , y_test.shape)

#Import Classification Methods
from sklearn.neighbors import KNeighborsClassifier
k = 6
neigh = KNeighborsClassifier(k).fit(x_train, y_train)
neigh

yhat = neigh.predict(x_test)
print(yhat[0:5], '--------------------------------------------------', x_test[0:5])

from sklearn import metrics
print("Train set Accuracy: ", metrics.accuracy_score(y_train, neigh.predict(x_train)))
print("Test set Accuracy: ", metrics.accuracy_score(y_test, yhat))

Ks = 10
mean_acc = np.zeros((Ks-1))
std_acc = np.zeros((Ks-1))
ConfustionMx = [];
for n in range(1,Ks):
    
    #Train Model and Predict  
    neigh = KNeighborsClassifier(n_neighbors = n).fit(x_train,y_train)
    yhat=neigh.predict(x_test)
    mean_acc[n-1] = metrics.accuracy_score(y_test, yhat)

    
    std_acc[n-1]=np.std(yhat==y_test)/np.sqrt(yhat.shape[0])

mean_acc

plt.plot(range(1,Ks),mean_acc,'g')
plt.fill_between(range(1,Ks),mean_acc - 1 * std_acc,mean_acc + 1 * std_acc, alpha=0.10)
plt.legend(('Accuracy ', '+/- 3xstd'))
plt.ylabel('Accuracy ', color = 'blue')
plt.xlabel('Number of Neighbors (K)', color = 'blue')
plt.tight_layout()
plt.show()
print( "The best accuracy was with", mean_acc.max(), "with k=", mean_acc.argmax()+1)