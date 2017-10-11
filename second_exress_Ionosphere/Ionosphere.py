#coding:utf-8
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
	

#创建训练集和测试集,函数是随机抽取X25%的数据当成训练集
from sklearn.cross_validation import train_test_split
X_train,X_test,Y_train,Y_test=train_test_split(X,Y,random_state=14)

#导入K临近分类器这个类并初始化一个实例
from sklearn.neighbors import KNeighborsClassifier
estimator=KNeighborsClassifier()
#训练数据进行训练，分析训练集中的数据，比较待分类的寻数据点和训练集中的数据
#找到新的进邻
estimator.fit(X_train,Y_train)
#用测试集测试算法，估计他在测试集上的表现
y_predicted=estimator.predict(X_test)
accuracy=np.mean(Y_test==y_predicted)*100
print "The accuracy is %.1f" % accuracy


#一种交叉检验方法,导入导入测试
from sklearn.cross_validation import cross_val_score
scores=cross_val_score(estimator,X,Y,scoring='accuracy')
average_accuracy=np.mean(scores)*100
print "The average accuracy is %.1f" %average_accuracy


#讲解调试参数，n_neighbors
avg_scores=[]
all_scores=[]
parameter_values=list(range(1,21))
for n_neighbors in parameter_values:
	estimator=KNeighborsClassifier(n_neighbors=n_neighbors)
	scores=cross_val_score(estimator,X,Y,scoring='accuracy')
	avg_scores.append(np.mean(scores))
	all_scores.append(scores)
	
from matplotlib import pyplot as plt 
plt.figure(figsize=(32,20))
plt.plot(parameter_values,avg_scores,'-o',linewidth=5, markersize=24)
plt.show()


#吧没一个特征的值域规范到0-1之间，最小的是0,最大的是1,其他的中间分值
from sklearn.preprocessing import MinMaxScaler
x_transformed=MinMaxScaler().fit_transform(X)
print x_transformed
print X

