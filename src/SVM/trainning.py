
from svmutil import *

trainA, trainB = svm_read_problem('./after_preprocess/train.dat')

testA, testB = svm_read_problem('./after_preprocess/test.dat')

m = svm_train(trainA, trainB,'-c 8')

predict_value = svm_predict(testA, testB, m)

predict_label = predict_value[0]

labels = {"0": "business", "1": "computers", "2": "culture-arts-entertainment", "3": "education-science",
          "4": "engineering", "5": "health", "6": "politics-society", "7": "sports"}

output = open('./after_preprocess/output.dat','w')

for line in predict_label:
    output.write(labels[str(int(line))])
    output.write("\n")
