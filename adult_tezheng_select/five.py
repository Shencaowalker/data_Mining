#coding:utf-8
import os
import pandas as pd
#data_folder=os.path.join(os.path.expanduser("~"),"Data","Adult")
#adult_filename=os.path.join(data_folder,"adult.data")
adult_filename="adult.data"
adult=pd.read_csv(adult_filename,header=None,names=["Age","Work-Class", "fnlwgt", "Education","Education-Num", "Marital-Status", "Occupation","Relationship", "Race", "Sex", "Capital-gain","Capital-loss", "Hours-per-week", "Native-Country","Earnings-Raw"])
adult.dropna(how="all",inplace=True)
'''
print adult.columns
print adult["Hours-per-week"].describe()
print adult["Education-Num"].median()

print adult["Education-Num"].mean()
print adult["Education-Num"].count()
print adult["Education-Num"].max()
print adult["Education-Num"].min()
print adult["Work-Class"].unique()
print adult[:20]
'''
adult["LongHours"]=adult["Hours-per-week"]>40


import numpy as np
#删除方差很小的特征值的操作，方差很小不能作为分类的依据,一定先作类似的简单分析和操作去掉无用的数据能提高速度
X=np.arange(30).reshape((10,3))
X[:,1]=1
print X
from sklearn.feature_selection import VarianceThreshold
vt=VarianceThreshold()
Xt=vt.fit_transform(X)
'''
print Xt
print(vt.variances_)

'''
#这里是用卡方检验得到没一个所有特征的符合程度的数值
X=adult[["Age","Education-Num","Capital-gain","Capital-loss","Hours-per-week"]].values
y=(adult["Earnings-Raw"] == ' >50K').values

from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
transformer=SelectKBest(score_func=chi2,k=3)


Xt_chi2=transformer.fit_transform(X,y)
#print (transformer.scores_)
#print Xt_chi2[:5]

#相关性的另一个计算方式，皮尔逊相关系数
from scipy.stats import pearsonr
def multivariate_pearsonr(X,y):
	scores,pvalues=[],[]
	for column in range(X.shape[1]):
		cur_score,cur_p=pearsonr(X[:,column],y)
		scores.append(abs(cur_score))
		pvalues.append(cur_p)
	return (np.array(scores),np.array(pvalues))
transformer=SelectKBest(score_func=multivariate_pearsonr,k=3)
Xt_pearson=transformer.fit_transform(X,y)
#print (transformer.scores_)

from sklearn.tree import DecisionTreeClassifier
from sklearn.cross_validation import cross_val_score
clf=DecisionTreeClassifier(random_state=14)
scores_chi2=cross_val_score(clf,Xt_chi2,y,scoring='accuracy')
scores_pearson=cross_val_score(clf,Xt_pearson,y,scoring='accuracy')
print scores_chi2.mean()
print scores_pearson.mean()

