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




######################## EM ######################

def normalize(d):
    for e in d:
        vals = d[e].values()
        N = sum(vals)
        if N == 0:
            continue
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
        
        # forward viterbi
        fwd = defaultdict(lambda: defaultdict(float))
        ftrace = defaultdict(lambda: defaultdict(str))
        fwd[0][0] = 1
        for e, ephon in enumerate(ewords[x]):
            for j in fwd[e]:
                for k in range(1,min(len(jwords[x])-j,3)+1):
                    jnum = j+k
                    jphon = ''.join([b+' ' for b in jwords[x][j:jnum]]).strip()
                    score = fwd[e][j] * pDict[ephon][jphon]
                    fwd[e+1][j+k] += score

        FTprob = fwd[len(ewords[x])][len(jwords[x])] # total probability for forward run


        # back viterbi
        bck = defaultdict(lambda: defaultdict(float))
        btrace = defaultdict(lambda: defaultdict(str))
        bck[len(ewords[x])][len(jwords[x])] = 1   
        for e in reversed(range(1,len(ewords[x])+1)):
            e = e-1
            ephon = ewords[x][e]
            for j in list(bck[e+1].keys()):
                j = j-1
                for k in range(0,min(j,2)+1):
                    jnum = j-k
                    jphon = ''.join([j+' ' for j in jwords[x][jnum:j+1]]).strip()
                    score = bck[e+1][j+1] * pDict[ephon][jphon]
                    bck[e][j-k] += score

        # get fractional counts
        for e, ephon in enumerate(ewords[x]):
            for j in list(fwd[e].keys()):
                for k in range(1,min(len(jwords[x])-j,3)+1):
                    jnum = j+k
                    jphon = ''.join([j+' ' for j in jwords[x][j:jnum]]).strip()
                    countDict[ephon][jphon] += pDict[ephon][jphon] * fwd[e][j] * bck [e+1][j+k] / FTprob


        cprob += -math.log(FTprob,2)

    # m step
    pDict = normalize(countDict)

    if cprob > 120:
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
        if pDict[e][j] >=0.01:
            fout.write(e + ' : ' + j + ' # ' + '{0:.8f}'.format(pDict[e][j]) + '\n')


