# this is tian yonghang's Bid Data Homework 1 part D code
import math


def updatebucket(bdict, tstamp, keys):
    """
    bdict(bucketdict)[i] only store the last timestamp that is '1',
    and the num of '1' before this timestamp must be euqal or larger that bdict[i](not for the last bdict[i]).
     For example:
                bdict[1] means this bucket's size is 1(in the head of bdict),
                so whenever a new '1' comes, it update itself;
                if there are two timestamp in bdict[1](a list), then pop the older timestamp.
     """
    bdict[1].append(tstamp)
    for key in bdict.keys():
        if len(bdict[key]) > 2:
            bdict[key].pop(0)
            oldfirststamp = bdict[key].pop(0)
            # klist[-1] is the last bucket
            if key != keys[-1]:
                # merged by next bucket
                bdict[key * 2].append(oldfirststamp)
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
                count += key
            else:
                count += int(0.5*key)
    print('Estimated number of ones in the last 1000 bits are {0}'.format(count))

# initial parameters
windowsize = 1000
bucketdict = {}
bucketsize = 0
timestamp = 0
# initial the length of bucketnum with O(logN)
bucketnum = int(math.log(1000, 2)+1)
keys = list()

# initialize bucket
for i in range(bucketnum):
    bucketsize = int(math.pow(2, i))
    bucketdict[bucketsize] = list()
    keys.append(bucketsize)

# open file
f = open('./engg5108_stream_data.txt')
stream = f.read()
f.close()

# DGIM algorithm
for i in range(len(stream)):
    # Only care about 1000 timestamps.
    # timestamp is in [0, 1000)
    timestamp = (timestamp + 1) % windowsize
    # iterate all keys(same with bucketdict.keys).
    for key in keys:
        for t in bucketdict[key]:
            # since timestamp is in [0,1000), we need to check like this.
            if timestamp == t:
                # remove timestamp that are out of windows
                # type(bucketdict[key]) = <class 'list'>
                bucketdict[key].remove(t)
    # only update bucket when '1' is coming
    if stream[i] == str(1):
        updatebucket(bucketdict, timestamp,keys)
    else:
        continue

#print(keys)
printoutbucket(bucketdict, keys)
