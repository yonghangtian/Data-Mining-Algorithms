# -*- coding: utf-8 -*-
"""
Created on Thu Dec  6 18:22:47 2018

@author: 62674
"""
from sklearn import svm
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

train_data =[]
test_data = []
data =[]
train_label =[]

with open('./svm_data/train.dat', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip().split()
        train_data.append(' '.join(line[:-1]))
        train_label.append(line[-1]) 
    train_num = len(train_label)

with open('./svm_data/test.dat', 'r', encoding='utf-8') as g:
    for line in g:
        line = line.strip().split()
        test_data.append(' '.join(line))

#generate TF-IDF matrix X for train data
data.extend(train_data)
data.extend(test_data)
vectorizer = TfidfVectorizer()
X_train = vectorizer.fit_transform(train_data)
X_test = vectorizer.transform(test_data)

#print(X.shape)
# matrix of train value
#X_train = X[:train_num,:]
#X_test= X[train_num  : ,:]

# generate the list of labels for svm by transfer catelogs to numbers
labels = np.unique(train_label)
trans_dic1 = {}

for index, item in enumerate(labels):
    trans_dic1[item] = index

numb_labels = [trans_dic1[x] for x in train_label]
#print(len(numb_labels))

#build the classifier
cla = svm.SVC(max_iter=500, gamma='scale', decision_function_shape='ovo')
cla.fit(X_train,numb_labels)
predict_trainlabel = cla.predict(X_train)

'''
 print to show the prediction accuracy on the trainning data 
 tune parameters according to the prediction accuracy
 after tuning parameters the accuracy achieve 93.4%, which is good enough to make predictions
'''
print(np.mean(predict_trainlabel==numb_labels))

predict_testlabel =cla.predict(X_test)
#transfer numbers to catalogs
trans_dic2 ={}
for index,item in enumerate(labels):
    trans_dic2[index] = item
results =[trans_dic2[x] for x in predict_testlabel]
with open('results.txt','w',encoding='utf-8') as f:
    f.write('\n'.join(results))
