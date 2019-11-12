from collections import defaultdict
import sys

fin = sys.stdin
fout = sys.stdout

lines = list(filter(lambda x:x!='' ,[w.strip() for w in fin.readlines()]))

ewords, jwords = [], []
for i,line in enumerate(lines):
    if i%2==0:
        ewords.append(line.split())
    else:
        jwords.append(line.split())

print(ewords)
print(jwords)

models = defaultdict(list)

for x in range(len(ewords)):
    for a in range(len(ewords[x])):
        for k in range(1,4):
            tempDict = {}
            e,j=0,0
            while e<len(ewords[x]):
                if e==a:
                    tempDict[(ewords[x][e],e)]=' '.join(jwords[x][j:j+k])
                    j += k
                else:
                    if e==len(ewords[x])-1:
                        tempDict[(ewords[x][e],e)]=' '.join(jwords[x][j:])
                    else:
                        tempDict[(ewords[x][e],e)]=jwords[x][j]
                    j += 1
                e += 1
            models[tuple(ewords[x])].append(tempDict) if '' not in tempDict.values() and len(tempDict.keys())==len(ewords[x]) else None

# print(models)

for x in range(len(ewords)):
    models[tuple(ewords[x])] = [n for i,n in enumerate(models[tuple(ewords[x])]) if n not in models[tuple(ewords[x])][i+1:]]

for k in models[tuple(ewords[0])]:
    print(k)