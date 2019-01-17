from Lib import re


def load_data_set():
    asso_file = open('./asso.csv', encoding='utf8')
    # initial a list to store lines in asso_file
    line_list = []

    for line in asso_file:
        words = line.split()

        for i in range(0, len(words)-1):
            # remove ',' in each element in words
            words[i] = re.sub(r'[^\w]', '', words[i])
        line_list.append(words[1:])

    asso_file.close()
    return line_list


def createC1(dataSet):
    C1 = []
    for transaction in dataSet:
        for item in transaction:
            if not [item] in C1:
                #store all the item unrepeatly
                C1.append([item])

    C1.sort()
    # return map(frozenset, C1)
    # frozen set, user can't change it.
    return list(map(frozenset, C1))


def scanD(D,Ck,minSupport):
    # parameters: dataset, a list of candidate set: Ck, and the minmun support(minsupport).
    ssCnt={}
    # traversing all tid(item lists) in dataset.
    for tid in D:
        # traversing all sets in candidate sets.
        for can in Ck:
            # check whether (set in candidate set) are subset of (item list in dataset).
            if can.issubset(tid):
                # python3 can not support
                # if not ssCnt.has_key(can):
                if not can in ssCnt:
                    # initial with 1
                    ssCnt[can] = 1
                # update the frequency of can
                else: ssCnt[can] += 1
    # the size of dataset
    numItems = float(len(D))
    # initial Lk, which is a list of frequent item-set.
    retList = []
    # store the support of each item-set
    supportData = {}
    for key in ssCnt:
        # calculate the support, where support is between (0,1).
        support = ssCnt[key]/numItems
        if support >= minSupport:
            # add frequent itemset to retList.
            retList.insert(0, key)
        supportData[key] = support
    return retList, supportData



def aprioriGen(Lm, k):
    """
    :param Lm: a list of frequent itemsets:Lm (m = k-1)
    :param k:  k is the item size of Ck
    :return: Ck, a list of candidate itemset of size k
    """
    # creates Ck, this retList is different from retList in func: scanD.
    retList = []
    lenLm = len(Lm)
    for i in range(lenLm):
        for j in range(i+1, lenLm):
            L1 = list(Lm[i])[:k-2]
            L2 = list(Lm[j])[:k-2]
            L1.sort()
            L2.sort()
            # 若两个集合的前k-2即（m-1）个项相同时,则将两个集合合并
            # 理解好apriori的单调性原则，就会发现，这样能够遍历到所有的候选项。
            if L1 == L2:
                # set union
                retList.append(Lm[i] | Lm[j])
    return retList


def apriori(dataSet, minSupport = 0.5):
    # candiante itemsets of size 1(itemset that only contains one item)
    C1 = createC1(dataSet)
    D = list(map(set, dataSet)) #python3
    # L1 is freqent itemsets of size 1
    L1, supportData = scanD(D, C1, minSupport)#单项最小支持度判断 0.5，生成L1
    L = [L1]
    k = 2
    # 创建包含更大项集的更大列表,直到下一个大的项集为空
    # continue to generate L(k+1) until last Lk is empty.
    while (len(L[k-2]) > 0):
        #Ck
        Ck = aprioriGen(L[k-2], k)
        #get Lk
        Lk, supK = scanD(D, Ck, minSupport)
        supportData.update(supK)
        L.append(Lk)
        k += 1
    return L, supportData


def generateRules(L, supportData, minConf=0.7):
    #频繁项集列表、包含那些频繁项集支持数据的字典、最小可信度阈值
    #存储所有的关联规则
    bigRuleList = []
    #只获取有两个或者更多集合的项目，从1, 即第二个元素开始，L[0]是单个元素的
    for i in range(1, len(L)):
        # 两个及以上的才可能有关联一说，单个元素的项集不存在关联问题
        for freqSet in L[i]:
            #该函数遍历L中的每一个频繁项集并对每个频繁项集创建只包含单个元素集合的列表H1
            H1 = [frozenset([item]) for item in freqSet]
            if (i > 1):
                #如果频繁项集元素数目超过2,那么会考虑对它做进一步的合并
                rulesFromConseq(freqSet, H1, supportData, bigRuleList, minConf)
            else:
                # i = 1, which means that the size of frequent itemset is 2
                # calcConf
                calcConf(freqSet, H1, supportData, bigRuleList, minConf)
    return bigRuleList


def calcConf(freqSet, H, supportData, brl, minConf=0.7):
    #针对项集中只有两个元素时，计算可信度
    #返回一个满足最小可信度要求的规则列表
    prunedH = []
    #后件，遍历 H中的所有项集并计算它们的可信度值
    for conseq in H:
        #可信度计算，结合支持度数据
        conf = supportData[freqSet]/supportData[freqSet-conseq]
        if conf >= minConf:
            #如果某条规则满足最小可信度值,那么将这些规则输出到屏幕显示
            print (freqSet-conseq,'-->', conseq, 'conf:', conf)
            #添加到规则里，brl 是前面通过检查的 bigRuleList
            brl.append((freqSet-conseq, conseq, conf))
            #同样需要放入列表到后面检查
            prunedH.append(conseq)
    return prunedH


def rulesFromConseq(freqSet, H, supportData, brl, minConf=0.7):
    #参数:一个是频繁项集,另一个是可以出现在规则右部的元素列表 H
    m = len(H[0])
    #频繁项集元素数目大于单个集合的元素数
    if (len(freqSet) > (m + 1)):
        #存在不同顺序、元素相同的集合，合并具有相同部分的集合
        Hmp1 = aprioriGen(H, m+1)
        #计算可信度
        Hmp1 = calcConf(freqSet, Hmp1, supportData, brl, minConf)
        if (len(Hmp1) > 1):
            #满足最小可信度要求的规则列表多于1,则递归来判断是否可以进一步组合这些规则
            rulesFromConseq(freqSet, Hmp1, supportData, brl, minConf)


dataSet= load_data_set()
L, suppData=apriori(dataSet, 0.1)
rules = generateRules(L, suppData, 0.9)
