#coding:utf-8

from operator import itemgetter
import numpy as np
data="affinity_dataset.txt"
X=np.loadtxt(data)
n_samples,n_features=X.shape
#print "This dataset has %d sampels and %d features" %(n_samples,n_features) 
#print X[:5]
'''
#得到购买苹果的用户数量
num_apple=0
for sample in X:
	if sample[3]==1:
		num_apple+=1
#print "%d people bought Apples." %num_apple

#得到购买香蕉的用户数量
num_banana=0
for sample in X:
	if sample[4]==1:
		num_banana+=1
#print "%d people bought Bananas." %num_banana
'''
features=["bread","milk","cheese","apples","bananas"]
#这个规则是用户买苹果后再买香蕉
rule_valid=0
rule_invalid=0
num_apple=0
for sample in X:
	if sample[3]==1:
		num_apple+=1
		if sample[4]==1:
			rule_valid +=1
		else:
			rule_invalid +=1
print "%d people bought Apples." %num_apple
print "%d people bought Apples and Bananas" %rule_valid
print "%d people bought Apples but not buy Bananas" %rule_invalid


from collections import defaultdict

valid_rules = defaultdict(int)
invalid_rules = defaultdict(int)
num_occurences = defaultdict(int)

for sample in X:
	for premise in range(n_features):
		if sample[premise]==0:
			continue
		num_occurences[premise]+=1
		for conclusion in range(n_features):
			if premise == conclusion: 
				continue
			if sample[conclusion]==1:
				valid_rules[(premise,conclusion)]+=1
			else:
				invalid_rules[(premise, conclusion)] += 1
support = valid_rules
confidence = defaultdict(float)
for premise, conclusion in valid_rules.keys():
	confidence[(premise, conclusion)] = valid_rules[(premise, conclusion)] / float(num_occurences[premise])
# 	print premise, conclusion,confidence[(premise, conclusion)]
'''
for premise, conclusion in confidence:
	premise_name = features[premise]
	conclusion_name = features[conclusion]
	print "Rule: If a person buys %s they will also buy %s" %(premise_name, conclusion_name)
	print " - Confidence: %.4f" %(confidence[(premise, conclusion)])
	print " - Support: %d" %(support[(premise, conclusion)])
	print " "
'''	
def print_rule(premise, conclusion, support, confidence, features):
	premise_name = features[premise]
	conclusion_name = features[conclusion]

	print "Rule: If a person buys %s they will also buy %s" %(premise_name, conclusion_name)
	print " - Confidence: %.4f" %(confidence[(premise, conclusion)])
	print " - Support: %d" %(support[(premise, conclusion)])
	print " "

def sorted_support_5():
	sorted_support=sorted(support.items(),key=itemgetter(1),reverse=True)
	for index in range(5):
		print "Rule # %d" %(index+1)
		(premise, conclusion)=sorted_support[index][0]
		print_rule(premise, conclusion, support, confidence, features)

def sorted_confidence_5():
	sorted_confidence=sorted(confidence.items(),key=itemgetter(1),reverse=True)
	for index in range(5):
		print "Rule # %d" %(index+1)
		(premise, conclusion)=sorted_confidence[index][0]
		print_rule(premise, conclusion, support, confidence, features)


if __name__=='__main__':
	while 1:
		number=raw_input('''if you want know first 5 in support please enter 1;
if you want know first 5 in confidence please enter 2;
if you want know all data with not sorted please enter 0;
if you want go,please enter 3:\n''')
		try:
			if int(number)==0:
				premise =int(raw_input("Please Enter premise:\n"))
				conclusion =int(raw_input("Please Enter conclusion:\n"))
				print_rule(premise, conclusion, support, confidence, features)
			elif int(number)==1:
				sorted_support_5()
			elif int(number)==2:
				sorted_confidence_5()
			elif int(number)==3:
				exit(0)
		except Exception as e:
			print "enter error,please enter again!"
			continue

