from sklearn import svm
from SEWork.preprocess import *


def train_test_svm(cla):
    p = Preprocess()
    train_label, train_matrix, test_label, test_matrix = p.preprocess_fourtype()
    # train svm
    cla.fit(train_matrix, train_label)

    # predict train matrix to check the model
    print('\n predict train data')
    predict_trainlabel = cla.predict(train_matrix)
    # show diff
    show_diff(predict_trainlabel, train_label)

    # predict test matrix to check the precision
    print('\n predict test data')
    predict_testlabel = cla.predict(test_matrix)
    # show diff
    show_diff(predict_testlabel, test_label)


# default linearSVC have 100% train precision, and 74% test precision.
print('SVM RESULT!!!!   METHOD: default LinearSVC')
cla1 = svm.LinearSVC()
train_test_svm(cla1)

# default SVC have 90% train precision, and 68% test precision
print('SVM RESULT!!!!   METHOD: default SVC')
cla2 = svm.SVC()
train_test_svm(cla2)

