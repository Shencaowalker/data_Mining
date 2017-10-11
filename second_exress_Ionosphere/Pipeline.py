from sklearn.pipeline import Pipeline
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cross_validation import cross_val_score
from sklearn.preprocessing import MinMaxScaler



import numpy as np
import csv
#ceshi
data_filename="ionosphere.data.txt"
X=np.zeros((351,34),dtype='float')
Y=np.zeros((351, ),dtype='bool')

with open(data_filename,'r') as input_file:
	reader=csv.reader(input_file)
	for i,row in enumerate(reader):
		data=[float(datum) for datum in row[:-1]]
		X[i]=data
		Y[i]=row[-1]=='g'
	

X_broken=np.array(X)
X_broken[:,::2] /=10



scaling_pipeline=Pipeline([('scale',MinMaxScaler()),('predict',KNeighborsClassifier())])
scores=cross_val_score(scaling_pipeline,X_broken,Y,scoring='accuracy')
print "The pipeline scored an average accuracy for is  %.1f" %(np.mean(scores)*100)
