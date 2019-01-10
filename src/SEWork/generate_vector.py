import numpy as np
from Lib import re
from sklearn import svm

train = []
test = []
# positive data in train
train_pos = []
# negative data in train
train_neg = []
# pos data in test
test_pos = []
# neg data in test
test_neg = []

# record all the words
words = []

def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

# replace date and 'eta' related word, meanwhile delete all symbols except numbers and alphanumeric characters
def replace_date_and_eta(a_list):
    after_list = []
    for word in a_list:
        word = re.sub(r'[^\w]', '', word)
        if 'eta' in word:
            word = 'eta'
        if RepresentsInt(word):
            word = 'certainDate'
        after_list.append(word)
    return after_list


with open('./fourtype/ask-eta.txt', encoding='utf8') as f1:
    count = 0
    for line in f1:
        # print(type(line))
        if line == '\n':
            continue
        count += 1
        line = line.strip().split()
        new_line = replace_date_and_eta(line)
        words.extend(new_line)
        if count < 50:
            train_pos.append(new_line)
        else:
            test_pos.append(new_line)

neg_lines = []
with open('./fourtype/others.txt', encoding='utf8') as f2:
    neg_lines = f2.readlines()

with open('./fourtype/request-early-eta.txt', encoding='utf8') as f3:
    neg_lines.extend(f3.readlines())

with open('./fourtype/request-eta-status.txt', encoding='utf8') as f4:
    neg_lines.extend(f4.readlines())


count = 0
for line in neg_lines:
    # print(type(line))
    if line == '\n':
        continue
    count += 1
    line = line.strip().split()
    new_line = replace_date_and_eta(line)
    words.extend(new_line)
    if count < 50:
        train_neg.append(new_line)
    else:
        test_neg.append(new_line)

# remove duplicate word in words
words = list(set(words))
# print(words)
# print('\n')
# print(len(words))

# print(len(train_pos))
# print(len(train_neg))
# print(len(test_pos))
# print(len(test_neg))

train.extend(train_pos)
train.extend(train_neg)
test.extend(test_pos)
test.extend(test_neg)

# now start to generate vectors
# first, create train data label's matrix
length = len(train)
label_pos = np.ones(len(train_pos),np.int)
label_neg = np.zeros(len(train_neg),np.int)
train_label = np.concatenate((label_pos, label_neg), axis=None)
print(train_label)
print(len(train_label))

# second, create train words matrix
train_matrix = np.zeros((length, len(words)), np.int)

for i in range(0, length-1):
    for j in range(0, len(train[i]) - 1):
        index = words.index(train[i][j])
        train_matrix[i][index] = 1

# third, create test data label's matrix
label_pos = np.ones(len(test_pos), np.int)
label_neg = np.zeros(len(test_neg), np.int)
test_label = np.concatenate((label_pos,label_neg), axis=None)
print(test_label)
print(len(test_label))

# fourth, create test words matrix
test_matrix = np.zeros((len(test), len(words)), np.int)

for i in range(0, len(test)-1):
    for j in range(0, len(test[i]) - 1):
        index = words.index(test[i][j])
        test_matrix[i][index] = 1

# train svm
cla = svm.SVC(max_iter=500, gamma='scale', decision_function_shape='ovo')
cla.fit(train_matrix, train_label)

predict_testlabel = cla.predict(test_matrix)

print(np.mean(predict_testlabel == train_label))

