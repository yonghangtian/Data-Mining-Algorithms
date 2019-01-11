import numpy as np
from Lib import re

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


def show_diff(predict_array, real_array):
    diff = 0.0

    for i in range(0, len(real_array)-1):
        if predict_array[i] == real_array[i]:
            continue
        diff += 1
    print('\n original label array is ')
    print(real_array)
    print('\n the length of original label array')
    print(len(real_array))
    print('\n the predict array is')
    print(predict_array)
    print('\n wrong predict number is')
    print(diff)
    print('\n total labels number is')
    print(len(predict_array))
    print('\n correct predict percentage/precision is ')
    print(1 - diff/len(real_array))


class Preprocess:
    'this class proecess files in four type for svm classifier'

    def preprocess_fourtype(self):
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

        train.extend(train_pos)
        train.extend(train_neg)
        test.extend(test_pos)
        test.extend(test_neg)

        # now start to generate vectors
        # first, create train data label's matrix
        label_pos = np.ones(len(train_pos),np.int)
        label_neg = np.zeros(len(train_neg),np.int)
        train_label = np.concatenate((label_pos, label_neg), axis=None)

        # second, create train words matrix
        train_matrix = np.zeros((len(train), len(words)), np.int)

        for i in range(0, len(train)-1):
            for j in range(0, len(train[i]) - 1):
                index = words.index(train[i][j])
                train_matrix[i][index] = 1

        # third, create test data label's matrix
        label_pos = np.ones(len(test_pos), np.int)
        label_neg = np.zeros(len(test_neg), np.int)
        test_label = np.concatenate((label_pos,label_neg), axis=None)

        # fourth, create test words matrix
        test_matrix = np.zeros((len(test), len(words)), np.int)

        for i in range(0, len(test)-1):
            for j in range(0, len(test[i]) - 1):
                index = words.index(test[i][j])
                test_matrix[i][index] = 1
        return (train_label, train_matrix, test_label, test_matrix)

