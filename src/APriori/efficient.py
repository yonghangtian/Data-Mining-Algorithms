from efficient_apriori import apriori
from Lib import re


def load_data_set():
    asso_file = open('./asso.csv', encoding='utf8')
    # initial a list to store lines in asso_file
    line_list = []
    # to store all the numbers
    nums = []

    for line in asso_file:
        words = line.split()

        for i in range(0, len(words)-1):
            # remove ',' in each element in words
            words[i] = re.sub(r'[^\w]', '', words[i])
        nums.extend(words[1:])
        line_list.append(tuple(words[1:]))

    asso_file.close()
    # print(len(nums)) 3562

    # a list to store distinct elements in asso_file
    distinct_nums = list(set(nums))
    # print(len(distinct_nums))  50
    # print(distinct_nums)
    distinct_nums = list(map(frozenset, distinct_nums))
    return line_list, distinct_nums


transactions,_ = load_data_set()

itemsets, rules = apriori(transactions, min_support=0.1,  min_confidence=0.9)

# Print out every rule with 2 items on the left hand side,
# 1 item on the right hand side, sorted by lift
rules_rhs = filter(lambda rule: len(rule.lhs) == 2 and len(rule.rhs) == 1, rules)
for rule in sorted(rules_rhs, key=lambda rule: rule.lift):
    print(rule) # Prints the rule and its confidence, support, lift, ...