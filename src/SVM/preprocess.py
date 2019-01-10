import numpy as np
import random
from os import path

originalTrainFile = open(path.abspath("svm_data/train.dat"), encoding='utf8')
originalTestFile = open(path.abspath("svm_data/test.dat"), encoding='utf8')

# hash function parameters:h(x) = (a*x + b)%length
a = 40000
b = 13
length = 30311

labels = {"business": 0, "computers": 1, "culture-arts-entertainment": 2, "education-science": 3, "engineering": 4,
          "health": 5, "politics-society": 6, "sports": 7}
word_idx = 0
word_set = {}
new_line_list = []

connect = ""
for line in originalTrainFile.readlines():
    line_list = line.split()
    word_num = 0
    # new_line is str type, and it is the new line that will be written into output file.
    # this step is to add labels' number to its beginning.
    new_line = [str(labels[line_list[-1].lower()]), " "]

    word_list = set(line_list[:-1])

    for word in word_list:
        word_num = word_num + 1
        if word not in word_set:
            word_set[word] = (word_idx*a+b) % length
            word_idx += 1
    # why normalize in this way?
    nomal = 1/np.sqrt(word_num)

    for word in word_list:
        new_line.append(str(word_set[word]) + ":" + "%.6f" % nomal+" ")
    line = connect.join(new_line)
    new_line_list.append(line)


afterTrainFile = open(path.abspath('after_preprocess/train.dat'),'w')
afterTestFile = open(path.abspath('after_preprocess/test.dat'),'w')
random.shuffle(new_line_list)

for member in new_line_list:
    afterTrainFile.write(member)
    afterTrainFile.write("\n")

for line in originalTestFile.readlines():
    line_list = list(line.split())
    new_line = ["0 "]

    word_list=set(line_list)
    for word in word_list:
        word_num += 1
        if word not in word_set:
            word_set[word]=(word_idx*a+b) % length
            word_idx+=1
    nomal=1/np.sqrt(word_num)
    for word in word_list:
        new_line.append(str(word_set[word])+":"+"%.6f" % nomal+" ")
    afterTestFile.write(connect.join(new_line)+"\n")
