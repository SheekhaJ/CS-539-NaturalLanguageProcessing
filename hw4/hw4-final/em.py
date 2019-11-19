from collections import defaultdict
import sys, math

fin = sys.stdin
fout = sys.stdout
ferr = sys.stderr

args = sys.argv[1:]

iters = 1
for arg in args:
    try:
        iters = int(arg)
    except:
        None

lines = []
lines = [lines+x.strip().split('\\n') for x in fin]
if isinstance(lines[0][0],list):
    lines = lines[0]

ewords, jwords = [], []
for i,line in enumerate(lines):
    if isinstance(line,list):
        line = line[0]
    if i%3==0:
        ewords.append(line.split())
    else:
        if '1' not in line:
            jwords.append(line.split())

            
def get_alignments(ewords,jwords, pDict=None):
    alignments = []
    for x, eword in enumerate(ewords):
        aligns = defaultdict(lambda : defaultdict(lambda : defaultdict(str)))
        paths = [[0]]

        for i in range(len(jwords[x])):
            for k in range(0,min(i,3)+1):
                jnum = i-k
                jpron = ''.join([j+' ' for j in jwords[x][jnum:i+1]]).strip()
                for e,ephon in enumerate(ewords[x][:jnum+1]):
                    if pDict is not None:
                        if pDict[ephon][jpron] == 0:
                            continue

                    if jnum <= e*3:
                        if i == len(jwords[x])-1 and e != len(ewords[x])-1:
                            continue
                        if i != len(jwords[x])-1 and e == len(ewords[x])-1:
                            continue
                        if len(jwords[x])-i < len(ewords[x])-e:
                            continue

                        aligns[i,jnum][e,ephon][jpron] = jpron

        paths = [[0]]
        for e,ephon in enumerate(ewords[x]):
            jstarts = [x for x in aligns if x[1]==e]
            newpaths = []
            for i, jnum in aligns:
                for ne, nephon in aligns[i,jnum]:
                    for jphon in aligns[i,jnum][ne,nephon]:
                        for path in paths:
                            if path[0] == jnum and len(path) == ne+1:
                                p = [i+1]+path[1:]+[{nephon:jphon}]
                                newpaths.append(p)
                            else:
                                if path[0]>e:
                                    if path not in newpaths:
                                        newpaths.append(path)

            if len(newpaths) != 0:
                paths = newpaths

        paths = [p[1:] for p in paths if p[0] == len(jwords[x])]
        alignments += paths
    return alignments


######################## EM ######################

def get_fracs(aligns, prob_dict):
    frac_counts = []
    for i, line in enumerate(aligns):
        f = 0
        for x in line:
            for e in x:
                f += -math.log(float(prob_dict[e][x[e]]),2)
        frac_counts.append(f)
    
    # normalize
    N = -math.log(sum([float(2**-x) for x in frac_counts]),2)
    frac_counts = [float(x-N) for x in frac_counts]
    return frac_counts, N

def count(aligns, frac_counts=None, uniform=False):
    countDict = defaultdict(lambda: defaultdict(float))
    for i,line in enumerate(aligns):
        for x in line:
            for e in x:
                if uniform:
                    countDict[e][x[e]] = 1
                else:
                    countDict[e][x[e]] += float(2**-frac_counts[i])
    return countDict

def normalize(d):
    for e in d:
        vals = d[e].values()
        N = sum(vals)
        for i, j in enumerate(d[e]):
                d[e][j] = min(1,float(d[e][j]/N))
    return d
            
def printdict(d):
    vals = [v for dv in d.values() for v in dv.values() if v >= 0.01]
    for e in d:
        ferr.write('\n' + e + '|->')
        for j in d[e]:
            if d[e][j] >= 0.01:
                ferr.write('  ' + j + ': ' + '{:0.3f}'.format(d[e][j])+'')
    ferr.write('\nnonzeros: '+str(len(vals))+'\n')

def init_probs(ewords,jwords):
    countDict = defaultdict(lambda: defaultdict(float))
    for x in range(len(ewords)):
        for e, ephon in enumerate(ewords[x]):
                for j in range(len(jwords[x])):
                    for k in range(1,min(len(jwords[x])-j,3)+1):
                        jnum = j+k
                        jphon = ''.join([b+' ' for b in jwords[x][j:jnum]]).strip()
                        countDict[ephon][jphon] = 1
    return normalize(countDict)

##### Start EM

# initialize uniform weights
pDict = init_probs(ewords,jwords)

for i in range(iters):

    # e step
    countDict = defaultdict(lambda: defaultdict(float))
    cprob = 0

    for x in range(len(ewords)):
        alignments = get_alignments(ewords[x:x+1],jwords[x:x+1],pDict)
        if len(alignments) == 0:
            continue
        fracs, exprob = get_fracs(alignments,pDict)
        newcDict = count(alignments, fracs)
        for e in newcDict:
            for j in newcDict[e]:
                countDict[e][j] += newcDict[e][j]
        cprob += exprob

    # m step
    pDict = normalize(countDict)

    if cprob > 220:
        cstr = '2^ '+str(-round(cprob,3))
    else:
        cstr = str(2**-cprob)

    ferr.write('\n\niteration '+str(i)+'  ---- corpus prob=  '+cstr)
    printdict(pDict)
    
    if 2**-cprob >= 1:
        break

# print final model to file
for e in sorted(pDict.keys()):
    for j in sorted(pDict[e]):
        if pDict[e][j] >=0.0000000001:
            fout.write(e + ' : ' + j + ' # ' + '{0:.8f}'.format(pDict[e][j]) + '\n')


