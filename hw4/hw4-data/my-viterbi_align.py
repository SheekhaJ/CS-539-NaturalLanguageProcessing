from collections import defaultdict
from collections import OrderedDict
import sys

fin = sys.stdin
lines = list(filter(lambda x:x!='' ,[w.strip() for w in fin.readlines()]))

ewords, jwords = [], []
for i,line in enumerate(lines):
    if i%3==0:
        ewords.append(line.split())
    else:
        if '1' not in line:
            jwords.append(line.split())

print(ewords[:5], jwords[:5])
probs = [line.strip() for line in open(sys.argv[1],'r')]
# probsDict = defaultdict(list)
probsDict = defaultdict(lambda : defaultdict(float))

for line in probs:
    line = line.split()
    epron, jpron, prob = line[0], ' '.join(line[2:line.index('#')]), line[-1]
    # probsDict[epron].append({jpron:prob})
    probsDict[epron][jpron] = prob

# print(probsDict.keys())
# print([(k,len(v)) for k,v in probsDict.items()])
# print(probsDict['EY'])
# print(probsDict['B'])
# print(probsDict['AH'])
# print(probsDict['L'])

# for k in ['AH', 'K', 'EY', 'SH', 'AH']:
#     print(probsDict[k])
print(probsDict['T'])
# alignments = defaultdict(lambda : defaultdict(str))
alignments = OrderedDict()
for x in range(len(ewords)):
# for x in range(1):
    # for i, epron in enumerate(['EY', 'B', 'AH', 'L']):
    # for i, epron in enumerate(['AH', 'K', 'EY', 'SH', 'AH']):
    m, maxJpronProbs = 0, {}
    for i, epron in enumerate(ewords[x]):
        jpronsList = []
        # if i == 0:
        for k in range(1,4):
            jprons = ' '.join(jwords[x][m:m+k])
            jpronsList.append((jprons,m+k)) if jprons not in jpronsList else None
        print(jpronsList)
        maxJpronProbs[epron] = [(jpr,probsDict[epron][jpr],z) for jpr,z in jpronsList if jpr in probsDict[epron].keys()]
        # if len(maxJpronProbs[epron]) != 0:
        maxJpronProb,m = max(maxJpronProbs[epron], key=lambda x:x[1])[1], max(maxJpronProbs[epron], key=lambda x:x[1])[2]
        print(epron, maxJpronProbs[epron], m)
        alignments[epron] = {jpr : i+1 for (jpr,prob,z) in maxJpronProbs[epron] if prob==maxJpronProb}
        # else:
        #     i, epron 
        # else:
        #     for k in range(1,4):
        #         jprons = ' '.join(jwords[x][m:m+k])
        #         jpronsList.append(jprons) if jprons not in jpronsList else None
        #     print(jpronsList)
        #     maxJpronProbs = [(jpr,probsDict[epron][jpr]) for jpr in jpronsList if jpr in probsDict[epron].keys()]
        #     maxJpronProb = max(maxJpronProbs, key=lambda x:x[1])[1]
        #     print(epron, maxJpronProbs)
        #     alignments[epron] = {jpr : i+1 for (jpr,prob) in maxJpronProbs if prob==maxJpronProb}
        # print(maxJpronProb)
        print(m,alignments[epron])
        # print(set([k.keys() for k in probsDict[epron]]).intersection(set([jpron for jpron in jpronsList]) ))
        # alignments[epron] = {jpron:probsDict[epron] for jpron in jpronsList if jpron in [k.keys() for k in probsDict[epron]]}
    print('---------------')
    
for k,v in alignments.items():
    print('{}:{}'.format(k,v))