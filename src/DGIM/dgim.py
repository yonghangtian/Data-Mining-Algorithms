# this is tian yonghang's Bid Data Homework 1 part D code
import math

windowsize = 1000
bucketdict = {}
bucketsize = 0
timestamp = 0
bucketnum = int(math.log(1000,2)+1)# O(logN)
keys = list()
# initialize bucket
for i in range(bucketnum):
    bucketsize = int(math.pow(2,i))
    bucketdict[bucketsize] = list()
    keys.append(bucketsize)

def updatebucket(bdict,tstamp,keys):
    bdict[1].append(tstamp)
    for key in bdict.keys():
        if len(bdict[key]) >2:
            bdict[key].pop(0)
            oldfirststamp = bdict[key].pop(0)
            if key !=keys[-1]:# klist[-1] is the last bucket
                bdict[key * 2].append(oldfirststamp) # merged by next bucket
        else:
            break

def printoutbucket(bdict,keys):
    count = 0
    for key in keys:
        for t in bdict[key]:
            oldeststamp = t
            print('bucket size is: {0}, timestamp is {1}'.format(key,t))
    for key in keys:
        for t in bdict[key]:
            if t != oldeststamp:
                count +=key
            else:
                count +=int(0.5*key)
    print('Estimated number of ones in the last 1000 bits are {0}'.format(count))


f = open('engg5108_stream_data.txt')
stream = f.read()
f.close()

for i in range(len(stream)):
    timestamp = (timestamp+1)%windowsize
    for key in keys:
        for t in bucketdict[key]:
            if timestamp == t:
                # remove timestamp that are out of windows
                bucketdict[key].remove(t)
    if stream[i] == str(1):
        updatebucket(bucketdict,timestamp,keys)
    else:
        continue
#print(keys)
printoutbucket(bucketdict,keys)



