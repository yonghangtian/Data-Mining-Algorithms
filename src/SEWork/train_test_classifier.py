from sklearn import svm
from SEWork.preprocess import *
from sklearn.linear_model import Perceptron
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_recall_fscore_support as prf
import sys
import warnings

if not sys.warnoptions:
    warnings.simplefilter("ignore")


def train_test_svm(cla):
    p = Preprocess()
    train_label, train_matrix, test_label, test_matrix = p.preprocess_fourtype()
    # train svm
    cla.fit(train_matrix, train_label)

    # predict train matrix to check the model
    print('\n predict train data')
    predict_trainlabel = cla.predict(train_matrix)
    # show diff
    # show_diff(predict_trainlabel, train_label)
    p,r,f,s = prf(train_label,predict_trainlabel)
    print(p,r,f,s)

    # predict test matrix to check the precision
    print('\n predict test data')
    predict_testlabel = cla.predict(test_matrix)
    # show diff
    # show_diff(predict_testlabel, test_label)
    p,r,f,s = prf(test_label,predict_testlabel)
    print(p,r,f,s)


print('SVM RESULT!!!!   METHOD: default LinearSVC')
cla1 = svm.LinearSVC()
train_test_svm(cla1)

print('SVM RESULT!!!!   METHOD: default SVC')
cla2 = svm.SVC()
train_test_svm(cla2)

print()
# add perceptron and linear regression predict.

p1 = Preprocess()
train_label, train_matrix, test_label, test_matrix = p1.preprocess_fourtype()

# preceptron
clf = Perceptron()
clf.fit(train_matrix, train_label)
# predict_trainlabel = clf.predict(train_matrix)
predict_testlabel = clf.predict(test_matrix)

# find TP,FP,TN,FN and calculate the precision, recall and f1 value.
p, r, f, s = prf(test_label, predict_testlabel)
# support is the occurrences of each class(since we have 0,1 two labels, all the results below is a 1*2 matrix)

print('precison, recall ,f1-score and support of preceptron')
print(p)
print(r)
print(f)
print(s)
print()
# logistic regression
clf_lr = LogisticRegression()
clf_lr.fit(train_matrix, train_label)
predict_testlabel = clf_lr.predict(test_matrix)

p, r, f, s = prf(test_label, predict_testlabel)
print('precison, recall ,f1-score and support of preceptron')
print(p)
print(r)
print(f)
print(s)
print()