import os
import pandas as pd
import numpy as np
from collections import defaultdict
data_filename="ad.data"


def convert_number(x):
	try:
		return float(x)
	except ValueError:
		return np.nan


converters=defaultdict(convert_number)
converters[1558]=lambda x:1 if x.strip() =='ad.' else 0
ads=pd.read_csv(data_filename,header=None,converters=converters)
#ads.dropna(how='all',inplace=True)
#print ads[:5]
X=ads.drop(1558,axis=1).values
y=ads[1558]
print X[:5]
print y[:5]

from sklearn.decomposition import PCA
pca=PCA(n_components=5)
Xd=pca.fit_transform(X)
np.set_printoptions(precision=3, suppress=True)
#print (pca.explained_variance_ratio_)
#print pca.components_[0]

from sklearn.tree import DecisionTreeClassifier
from sklearn.cross_validation import cross_val_score
clf = DecisionTreeClassifier(random_state=14)
scores_reduced = cross_val_score(clf, Xd, y, scoring='accuracy')
print "The average score from reduced dataset is %.4f" %scores_reduced

