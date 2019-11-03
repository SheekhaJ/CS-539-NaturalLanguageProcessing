from collections import defaultdict

lines = [l.strip() for l in open('epron-jpron.data','r').readlines()]
elines, jlines, alignlines = [], [], []

for i,l in enumerate(lines):
    if i%3==0:
        elines.append(l)
    elif i%3==1:
        jlines.append(l)
    elif i%3==2:
        alignlines.append(l)

# print(elines)
# print(jlines)
# print(alignlines)

mapping, mappingCount = defaultdict(list), defaultdict(lambda : defaultdict(lambda:float(0)))
for i,al in enumerate(alignlines):
    temp = [None for _ in range(max(map(int,al.split())))]
    jchars = jlines[i].split()
    echars = elines[i].split()
    
    for j,a in enumerate(al.split()):
        a = int(a)
        if temp[a-1]!=None and len(temp[a-1]+jchars[j]) > 3:
            continue
        temp[a-1] = temp[a-1]+jchars[j] if temp[a-1]!=None else jchars[j]
    tempDict = {echars[j]:temp[j] for j in range(len(temp))}
    
    # print(''.join(echars),tempDict)

    for k,v in tempDict.items():
        mapping[k].append(v)

for echar,jchars in mapping.items():
    for jchar in jchars:
        mappingCount[echar][jchar] += 1 

# print(mapping)
# print(mappingCount)

probs = {echar : {jchar:mappingCount[echar][jchar]/sum(mappingCount[echar].values()) for jchar in jcharcounts} for echar,jcharcounts in mappingCount.items()}

for echar, jcharprobs in probs.items():
    for jchar, prob in jcharprobs.items():
        if prob<0.01:
            probs[echar][jchar] = float(0)

probs = {echar : {jchar:probs[echar][jchar]/sum(probs[echar].values()) for jchar in jcharcounts} for echar,jcharcounts in probs.items()}

outStr = ''
for echar, jchars in sorted(probs.items()):
    for jchar,prob in sorted(jchars.items()):
        if len(jchar.split()) > 0:
            for c in jchar.split():
                outStr += echar+' : '+ c +' # '+str(prob)+'\n'
print(outStr)