#coding:utf-8
import sys
import os
import pandas as pd
#生成可执行路径
data=os.path.join("ml-100k",'u.data')
#with open(data) as da:
#	print da.read()
#下面一条代码是格式化data文件用csv，并生成集合
all_ratings=pd.read_csv(data,delimiter='\t',header=None,names=["UserID","MovieID","Rating","Datetime"])
#下面的函数是解析时间戳数据，把时间转化成标准格式
all_ratings["Datetime"]=pd.to_datetime(all_ratings["Datetime"],unit='s')
#print all_ratings[:5]
#下面代码是给集合加上一列，列名是Favorable,值根据后面的代码确定>3 True ;<3 False
all_ratings["Favorable"]=all_ratings["Rating"]>3
#print all_ratings[10:15]
#下面的语句是得到测试集合，前0-199个用户的所有的评论信息
ratings=all_ratings[all_ratings['UserID'].isin(range(200))]
'''
count=0
for i in ratings:
	count+=1
print count
print len(ratings["UserID"])
'''
#根据上面的到的所有的200个用户的信息筛选出Favorable是正确的集合
favorable_ratings=ratings[ratings["Favorable"]]
#print favorable_ratings[:5]
#下面的代码是把一个所有的用户的True评论整合到一起，（UserID,forzenset(为 True的"MovieID")）
favorable_reviews_by_users=dict((k,frozenset(v.values)) for k,v in favorable_ratings.groupby("UserID")["MovieID"])
'''
for i in range(1,11):
	print favorable_reviews_by_users[i]
print len(favorable_reviews_by_users)
'''
#下面的代码是得到一个包含
num_favorable_by_movie=ratings[["MovieID","Favorable"]].groupby("MovieID").sum()
print num_favorable_by_movie[:5]
#num_favorable_by_movie.sort("Favorable",ascending=False)[:5]



frequent_itemsets={}
min_support=50
frequent_itemsets[1]=dict((frozenset((movie_id,)),row["Favorable"]) for movie_id,row in num_favorable_by_movie.iterrows() if row["Favorable"] >min_support)
print frequent_itemsets[1]

from collections import defaultdict
def find_frequent_itemsets(favorable_reviews_by_users,k_1_items, min_support):
	counts = defaultdict(int)
	for user, reviews in favorable_reviews_by_users.items():
		for itemset in k_1_items:
			if itemset.issubset(reviews):
				for other_reviewed_movie in reviews - itemset:
					current_superset = itemset | frozenset((other_reviewed_movie,))
					counts[current_superset] += 1
	return dict([(itemset, frequency) for itemset, frequency in counts.items() if frequency >= min_support])


for k in range(2,20):
	cur_frequent_itemsets=find_frequent_itemsets(favorable_reviews_by_users,frequent_itemsets[k-1],min_support)
	if len(cur_frequent_itemsets)==0:
		print "Did not find any frequent itemsets of length %d" %k
		sys.stdout.flush()
		break
	else:
		print "I find %d frequent of length %d" %(len(cur_frequent_itemsets),k)
		sys.stdout.flush()
		frequent_itemsets[k]=cur_frequent_itemsets


del frequent_itemsets[1]
#print "This have %f frequents" %(sum(len(i)) for i in frequent_itemsets.values())

candidate_rules=[]
for itemset_length,itemset_counts in frequent_itemsets.items():
	for itemset in itemset_counts.keys():
		for conclusion in itemset:
			permise=itemset - set((conclusion,))
			candidate_rules.append((permise,conclusion))

#print (candidate_rules[:5])

movie_name_filename = os.path.join("ml-100k", "u.item")
movie_name_data = pd.read_csv(movie_name_filename, delimiter="|", header=None, encoding = "mac-roman")
movie_name_data.columns = ["MovieID", "Title", "Release Date", "Video Release", "IMDB", "<UNK>", "Action", "Adventure",
                           "Animation", "Children's", "Comedy", "Crime", "Documentary", "Drama", "Fantasy", "Film-Noir",
                           "Horror", "Musical", "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western"]

def get_movie_name(movie_id):
	title_object=movie_name_data[movie_name_data["MovieID"]==movie_id]["Title"]
	title = title_object.values[0]
	return title 
	
print get_movie_name(4)



a=int(raw_input("Please enter 1 for test or 0 for train:"))
if a==0:
	test_dataset=all_ratings[~all_ratings["UserID"].isin(range(200))]
	test_favorable=test_dataset[test_dataset["Favorable"]]
	favorable_reviews_by_users=dict((k,frozenset(v.values)) for k,v in test_favorable.groupby("UserID")["MovieID"])


correct_counts=defaultdict(int)
incorrect_counts=defaultdict(int)

for user,reviews in favorable_reviews_by_users.items():
	for candidate_rule in candidate_rules:
		permise,conclusion=candidate_rule
		if permise.issubset(reviews):
			if conclusion in reviews:
				correct_counts[candidate_rule]+=1
			else:
				incorrect_counts[candidate_rule]+=1
rule_confidence={candidate_rule:correct_counts[candidate_rule] / float(correct_counts[candidate_rule] + incorrect_counts[candidate_rule]) for candidate_rule in candidate_rules}
from operator import itemgetter
sorted_confidence=sorted(rule_confidence.items(),key=itemgetter(1),reverse=True)
for i in range(5):
	(premise,conclusion)=sorted_confidence[i][0]
	premise_names=",".join(get_movie_name(idx) for idx in premise)
	conclusion_name=get_movie_name(conclusion)
	print "Rule %d" %(i+1)
	print "if a person recommends" +`premise`+"and they will also recommend"+`conclusion`
	print "if a person recommends" +`premise_names`+"and they will also recommend"+`conclusion_name`
	print "confidence %.3f"% sorted_confidence[i][1]
	print "\n"

