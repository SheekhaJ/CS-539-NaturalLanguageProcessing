from collections import defaultdict
import sys
import math
import string

fin = sys.stdin
fout = sys.stdout
ferr = sys.stderr
iters = int(sys.argv[2])

cipher = [line.strip() for line in fin.readlines()]
trainlines = [line.strip() for line in open(sys.argv[1],'r').readlines()]
trainlines = ['_'.join(line.split()) for line in trainlines]

start, end = ('<s>','</s>')

# trainlines = [[start]+[l for l in line]+[end] for line in trainlines]

#trainChars = [trainChars.add(c) for line in trainlines for c in line]
trainChars = list(string.ascii_lowercase) + [' ']
print('len of trainchars: {}'.format(len(trainChars)))
cipherChars = [c for string in cipher for c in string]
# cipherChars = [start]+[c for string in cipher for c in string]+[end]

trainCharDict, cipherCharDict = defaultdict(int), defaultdict(int)
for c in trainChars:
    trainCharDict[c] += 1

for c in cipherChars:
    cipherCharDict[c] += 1

bigram = defaultdict(lambda : defaultdict(int))
bigramprobs = defaultdict(lambda : defaultdict(float))
for line in trainlines:
    for i in range(len(line)-1):
        bigram[line[i]][line[i+1]] += 1

for c1 in bigram.keys():
    N = sum(bigram[c1].values())
    for c2,count in bigram[c1].items():
        bigramprobs[c1][c2] = bigram[c1][c2]/float(N)

chars = [(i,c) for i,c in enumerate(trainCharDict.keys())]

def printdict(d):
    vals = [v for dv in d.values() for v in dv.values() if v >= 0.01]
    for e in d:
        ferr.write('\n' + e + '|->')
        for j in d[e]:
            if d[e][j] >= 0.01:
                ferr.write('  ' + j + ': ' + '{:0.3f}'.format(d[e][j])+'')
    # ferr.write('\nnonzeros: '+str(len(vals))+'\n')

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
    countDict = {}
    for cc in cDict:
        countDict[cc] = {}
        for tc in tDict:
            countDict[cc][tc] = 1
    return normalize(countDict)
    

pDict = initProbs(trainCharDict, cipherCharDict)
# pDict = initProbs(cipherCharDict, trainCharDict)
for k,v in pDict.items():
    print('{}:{} -- len:{}'.format(k,v,len(v)))
print(len(pDict.keys()))

iters = 1
for k in range(iters):
    # e step
    countDict= defaultdict(lambda : defaultdict(float))
    corpusprob = 0

    # Forward Viterbi    
    fwd = defaultdict(lambda : defaultdict(float))
    fwdTrace = defaultdict(lambda : defaultdict(str))
    fwd[0][' '] = 1

    # Backward Viterbi
    bck = defaultdict(lambda : defaultdict(float))
    bckTrace = defaultdict(lambda : defaultdict(str))
    
    for x in range(len(cipher)):
        for i,cc in enumerate(cipher[x]):
            for curr in pDict[cc]:
                for prev in fwd[i-1]:
                    if curr in bigramprobs[prev]:
                        score = fwd[i-1][prev] * bigramprobs[prev][curr] * pDict[cc][curr]
                        if score > fwd[i][curr]:
                            fwd[i][curr] += score
                            fwdTrace[i][curr] = prev
        
        FTprob = fwd[len(pDict)][end]
            
        # for k,v in fwd.items():
        #     print('len: {} key:{} '.format(len(v),k)) 
            # print('len: {} key:{} val:{}'.format(len(v),k,v)) 
        print('FTprob: {}'.format(FTprob))
        
        cl = len(cipher[x])
        bck[cl][' '] = 1
    
        for i in reversed(range(1,cl+1)):
            i = i - 1
            cc = cipher[x][i]
            for curr in pDict[cc]:
                for next in bck[cc]:
                    if curr in bigramprobs[next]:
                        score = bck[i+1][next] * bigramprobs[next][curr] * pDict[cc][curr]
                        if score > bck[i][curr]:
                            bck[i][curr] += score
                            bckTrace[i][curr] = next

        # for k,v in bck.items():
        #     print('len: {} key:{} '.format(len(v),k)) 
            # print('len: {} key:{} val:{}'.format(len(v),k,v)) 

        # Get fractional counts
        for i,cc in enumerate(cipher[x],1):
            for tc in list(fwd[i].keys()):
                countDict[cc][tc] += pDict[cc][tc] * fwd[i][cc] * bck[i+1][tc] / FTprob

        corpusprob += -math.log10(FTprob)

        # print('countDict: {}'.format(countDict))
        print('corpus prob: {}'.format(corpusprob))

    # m-step
    pDict = normalize(countDict)

    if corpusprob > 120:
        cstr =  '10^ '+str(-round(corpusprob,3))
    else:
        cstr = str(10**-corpusprob)
    
    # for i,cc in enumerate(cipher[x]):
    #     for tc in list(fwd[i].keys()):
    #         print(pDict[cc][tt])

    # for k,v in pDict.items():
    #     print(k,v)

    cstr = str(corpusprob)
    # entropy = str(-sum([(pDict[c][d] * math.log10(pDict[c][d])) for i,c in enumerate(cipher[x]) for d in list(fwd[i].keys())]))
    nonzeros = str(len([v for dv in pDict.values() for v in dv.values() if v >= 0.01]))

    # ferr.write('\n\nepoch '+str(i)+'  logp(corpus)=  '+cstr+' entropy= '+entropy+' non-zeros= '+nonzeros)
    ferr.write('\n\nepoch '+str(k+1)+'  logp(corpus)=  '+cstr+' non-zeros= '+nonzeros+'\n')
    
    # printdict(pDict)
    
    if 10**-corpusprob >= 1:
        break

# for e in sorted(pDict.keys()):
#     for j in sorted(pDict[e]):
#         if pDict[e][j] >=0.01:
#             fout.write(e + ' : ' + j + ' # ' + '{0:.8f}'.format(pDict[e][j]) + '\n')