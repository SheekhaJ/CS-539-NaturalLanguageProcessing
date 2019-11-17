from collections import defaultdict
import sys

fin = sys.stdin
fout = sys.stdout
iters = int(sys.argv[2])

cipher = [line.strip() for line in fin.readlines()]
trainlines = [line.strip() for line in open(sys.argv[1],'r').readlines()]
trainlines = ['_'.join(line.split()) for line in trainlines]

start, end = ('<s>','</s>')

trainlines = [[start]+[l for l in line]+[end] for line in trainlines]

bigram = defaultdict(lambda : defaultdict(int))
bigramprobs = defaultdict(lambda : defaultdict(int))
for line in trainlines:
    for i in range(len(line)-1):
        bigram[line[i]][line[i+1]] += 1

for c1 in bigram.keys():
    N = sum(bigram[c1].values())
    for c2,count in bigram[c1].items():
        bigramprobs[c1][c2] = bigram[c1][c2]/float(N)

trainChars = [c for line in trainlines for c in line]
cipherChars = [start]+[c for string in cipher for c in string]+[end]

trainCharDict, cipherCharDict = defaultdict(int), defaultdict(int)
for c in trainChars:
    trainCharDict[c] += 1

for c in cipherChars:
    cipherCharDict[c] += 1

chars = [(i,c) for i,c in enumerate(trainCharDict.keys())]

def normalize(d):
    for k in d:
        vals = d[k].values()
        N = sum(vals)
        if N==0:
            continue
        for i,j in enumerate(d[k]):
            d[k][j] = min(1, float(d[k][j])/N)
    return d


def initProbs(tDict, cDict):
    countDict = defaultdict(lambda : defaultdict(float))
    for tc in tDict:
        for cc in cDict:
            countDict[tc][cc] = 1
    return normalize(countDict)
    

pDict = initProbs(trainCharDict, cipherCharDict)

for k in range(iters):
    # e step
    countDict= defaultdict(lambda : defaultdict(float))
    corpusprob = 0
    
    # Forward Viterbi    
    fwd = defaultdict(lambda : defaultdict(float))
    # fwdTrace = defaultdict(lambda : defaultdict(str))
    fwd[0][start] = 1
    for x in range(len(cipher)):
        for i,c in enumerate(cipher[0],1):
            for curr in pDict[c]:
                for prev in fwd[i-1]:
                    if curr in bigramprobs[prev]:
                        score = fwd[i-1][prev] * pDict[c][curr] * bigramprobs[prev][curr]
                        fwd[i][curr] += score

            
    for k,v in fwd.items():
        print('len: {} key:{} val:{}'.format(len(v),k,v))
        