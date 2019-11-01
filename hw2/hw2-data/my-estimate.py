from collections import defaultdict

lines = [l.strip() for l in open('given1.data','r').readlines()]
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

mapping = defaultdict(list)
for i,al in enumerate(alignlines):
    temp = [[None,1] for _ in range(max(map(int,al.split())))]
    jchars = jlines[i].split()
    echars = elines[i].split()
    
    for j,a in enumerate(al.split()):
        a = int(a)
        if temp[a-1][0]!=None and len(temp[a-1][0]+jchars[j]) > 3:
            continue
        temp[a-1][0] = temp[a-1][0]+jchars[j] if temp[a-1][0]!=None else jchars[j]
    tempDict = {echars[j]:temp[j] for j in range(len(temp))}
    
    # print(''.join(echars), mapping, tempDict)
    for k,v in tempDict.items():
        # print([t[0] for t in mapping[k]])
        # print(k, mapping[k], v[0])
        # if v[0] not in [t[0] for t in mapping[k]]:
        if v not in mapping[k]:
            mapping[k].append(v)
        else:
            x = mapping[k].index(v)
            mapping[k][x][1] += 1

print(mapping)
