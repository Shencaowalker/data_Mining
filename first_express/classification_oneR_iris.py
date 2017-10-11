#coding:utf-8
from sklearn.datasets import load_iris
import numpy as np
from collections import defaultdict
from operator import itemgetter
#上面是导入各个需要的库，defaultdict默认格式的字典和itemgetter为排列依据
dataset=load_iris()
x=dataset.data #数据集合
y=dataset.target #所属类别集合
attribute_means=x.mean(axis=0) #计算数据集合的所有特征值的平均值
x_d=np.array(x >=attribute_means,dtype='int') #x_d是对比平均值，大于就是1,小于就是0,得到一个对比
#只包含0-1的和数据集合同维的数组
'''
print x[:3]
print y[:3]
print attribute_means
print x_d[:3]
'''
#print dataset.DESCR，这里得到数据个数和单个数据的特征个数
n_samples, n_features = x.shape
from sklearn.cross_validation import train_test_split

# Set the random state to the same number to get the same results as in the book
random_state = 14

x_train, x_test, y_train, y_test = train_test_split(x_d, y, random_state=random_state)
#train_test_split把数据分开为训练数据和测试数据，防止过拟合，训练数据用来得到规则和创建模型，测试数据用来
#查看模型的分类效果
'''
print x_train
print '\n'
print x_test
print '\n'
print y_train
print '\n'
print y_test
print '\n'
print"There are %d training samples" %(y_train.shape)
print"There are %d testing samples" %(y_test.shape)
'''


'''	
	循环遍历这个列表，提供调用这个train_feature_value这个函数的current_value参数，
	二维数组中x[][feature]这一列进行全部给定特征值和error的获取
	得到的predictors包含所有的values中的特征值所对应的匹配量最多的类别的字典
	得到的total_error是以这行为标准测试的错误率，这一是我们确定最后用那一行来评测的最终对比数据
'''	

def train(x,y_true,feature):
	n_samples, n_features = x.shape
	assert 0 <= feature < n_features
	#断言后面必须为真才好
	s = set(x[:,feature])
	#这个厉害了，这个是找出x这个二维数组中x[][feature]这一列中所有没有重复的特征值并set成列表
	values=[]#应为上面得到的s不太对头，小数位太多，而且和原来不等，round()函数可以回归正常
	for i in s:
		values.append(round(i,1))
	predictors = dict()
	errors = []
	for current_value in values:
	        most_frequent_class, error = train_feature_value(x, y_true, feature, current_value)
	        predictors[current_value] = most_frequent_class
		errors.append(error)
	total_error = sum(errors)
	return predictors, total_error

#这是描述feature_index这个特征输入时的最大支持量的类别和错误率
def train_feature_value(x,y_true,feature_index,value):
	class_counts=defaultdict(int)
	for sample,y in zip(x,y_true):#绑定数据的内容和数据的类别
		if sample[feature_index]==value:#查看特定的特征值和给定的特征值是否一致
			class_counts[y] +=1#一致则把这个类型符合这个给定特征值+1
	sorted_class_counts=sorted(class_counts.items(),key=itemgetter(1),reverse=True)
	#得到特征值最大的那一个类别
	most_frequent_class=sorted_class_counts[0][0]
	incorrect_predictions=[class_count for class_value,class_count in class_counts.items()
	if class_value != most_frequent_class]
	#这里是计算除了特征值最大的以外的其他的类别的数量统计一下，这个就是在给定的特征值在给定的列的
	#错误率
	error=sum(incorrect_predictions)
	return most_frequent_class,error
	#返回特征值最大的类别和错误率

'''
values=set(x[:,3])
s=[]
for i in  values:
	s.append(round(i,1))
riable': best_variable,
         'predictor': all_predictors[best_variable][0]}
	 print(model)
'''
all_predictors={variable: train(x_train, y_train, variable) for variable in range(x_train.shape[1])}
#上面很有意思，是遍历所有的列得到4组数据，{列标:(predictors, total_error)}predictors也是一个字典
#里面记录了每一个当列给定特征值后出现次数最多的类别
#total_error为选当列的错误率
errors = {variable: error for variable, (mapping, error) in all_predictors.items()}
#里面记录了{列标:total_error}
best_variable, best_error = sorted(errors.items(), key=itemgetter(1))[0]
print "The best model is based on variable %d  and has error %.2f" %(best_variable, best_error)

model = {'variable': best_variable,
         'predictor': all_predictors[best_variable][0]}
print(model)

