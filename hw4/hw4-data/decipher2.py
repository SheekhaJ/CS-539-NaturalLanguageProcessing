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
bigramprobs = defaultdict(lambda : defaultdict(float))
for line in trainlines:
    for i in range(len(line)-1):
        bigram[line[i]][line[i+1]] += 1

reversebigram = defaultdict(lambda : defaultdict(int))
reversebigramprobs = defaultdict(lambda : defaultdict(float))
for l,line in enumerate(trainlines):
    for i in range(len(line)-1,0,-1):
        reversebigram[line[i]][line[i-1]] += 1

for c1 in bigram.keys():
    N = sum(bigram[c1].values())
    for c2,count in bigram[c1].items():
        bigramprobs[c1][c2] = bigram[c1][c2]/float(N)

for c1 in reversebigram.keys():
    N = sum(reversebigram[c1].values())
    for c2,count in reversebigram[c1].items():
        reversebigramprobs[c1][c2] = reversebigram[c1][c2]/float(N)

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
for k,v in pDict.items():
    print('{}:{}'.format(k,v))
# for k in range(iters):
    # e step
countDict= defaultdict(lambda : defaultdict(float))
corpusprob = 0

# Forward Viterbi    
fwd = defaultdict(lambda : defaultdict(float))
# fwdTrace = defaultdict(lambda : defaultdict(str))
fwd[0][start] = 1

# Backward Viterbi
bck = defaultdict(lambda : defaultdict(float))
# bckTrace = defaultdict(lambda : defaultdict(str))
# cl = len(cipher[x])
cl = len(cipher[0])
bck[cl][end] = 1

# for x in range(len(cipher)):
for x in range(1):
    for i,c in enumerate(cipher[0],1):
        for curr in pDict[c]:
            for prev in fwd[i-1]:
                if curr in bigramprobs[prev]:
                    score = fwd[i-1][prev] * pDict[c][curr] * bigramprobs[prev][curr]
                    fwd[i][curr] += score
    # FTprob = fwd[-1][]
        
# for k,v in fwd.items():
#     print('len: {} key:{} val:{}'.format(len(v),k,v)) 
    
    for i in reversed(range(1,cl+1)):
        i = i - 1
        c = cipher[0][i]
        for curr in pDict[c]:
            for next in list(bck[i+1].keys()):
                if curr in reversebigramprobs[next]:
                    score = bck[i+1][next] * pDict[c][curr] * reversebigramprobs[next][curr]
                    bck[i][curr] += score

for k,v in bck.items():
    print('len: {} key:{} val:{}'.format(len(v),k,v))
