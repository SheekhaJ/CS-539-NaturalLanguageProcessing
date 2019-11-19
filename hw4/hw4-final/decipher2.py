from collections import defaultdict
import sys, math, string

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
    if 'train.txt' in arg:
        train_file = arg

train = [line.strip() for line in open(train_file, 'r')]
cipher = [line.strip() for line in fin]

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
        t=0
        for j in d[e]:
            if d[e][j] >= 0.01:
                t=0
                ferr.write('  ' + j + ': ' + '{:0.3f}'.format(d[e][j])+'')
    ferr.write('\nnonzeros: '+str(len(vals))+'\n')

def init_bigram():
    alphabet = [x for x in string.ascii_lowercase]+[' ']
    bigram = {c1 : {c2 : float(0) for c2 in alphabet} for c1 in alphabet}

    for line in train:
        for i, char in enumerate(line):
            if i == 0:
                bigram[' '][char] += 1
            else:
                bigram[line[i-1]][char] += 1
    return normalize(bigram)

def init_probs():
    alphabet = [x for x in string.ascii_lowercase]+[' ']
    countDict = {c1 : {c2 : float(1/len(alphabet)) for c2 in alphabet} for c1 in alphabet}
    return countDict

##### Start EM

alphabet = [x for x in string.ascii_lowercase]+[' ']
pDict = init_probs()
bigram = init_bigram()

for i in range(iters):
    # e step
    countDict = defaultdict(lambda: defaultdict(float))
    cprob = 0
    
    for cline in cipher:
        # forward viterbi
        fwd = defaultdict(lambda: defaultdict(float))
        ftrace = defaultdict(lambda: defaultdict(str))
        fwd[0][' '] = 1
        for e, char in enumerate(cline):
            for pre in list(fwd[e].keys()):
                for a in [x for x in alphabet if char in pDict[x]]:
                    score = fwd[e][pre] * pDict[a][char] * bigram[pre][a]
                    fwd[e+1][a] += score

        FTprob = sum(fwd[len(cline)].values()) # total probability for forward run

        # back viterbi
        bck = defaultdict(lambda: defaultdict(float))
        btrace = defaultdict(lambda: defaultdict(str))
        bck[len(cline)][' '] = 1   
        for e in reversed(range(1,len(cline)+1)):
            e = e-1
            char = cline[e]
            for post in list(bck[e+1].keys()):
                for a in [x for x in alphabet if char in pDict[x]]:
                    score = bck[e+1][post] * pDict[a][char] * bigram[a][post]
                    bck[e][a] += score

        
        # get fractional counts
        for e, ciph in enumerate(cline):
            for pre in list(fwd[e].keys()):
                for a in list(fwd[e+1].keys()):
                    countDict[a][ciph] += fwd[e][pre]* bigram[pre][a] * bck[e][a] / FTprob


        cprob += -math.log(FTprob,2)

    # m step
    pDict = normalize(countDict)

    if cprob > 120:
        cstr = '2^'+str(-round(cprob,2))
    else:
        cstr = str(2**-cprob)

    N = sum([len(x) for x in cipher])
    ent = round(1/N*cprob,3)
    
    vals = [v for dv in pDict.values() for v in dv.values() if v >= 0.01]
    ferr.write('epoch '+str(i+1)+' -- corpus=  ' + cstr
               + ' -- nonzeros: '+str(len(vals))
               + ' -- entropy= ' + str(ent)+'\n')

##    printdict(pDict)
    
    if 10**-cprob >= 1:
        break

# print final model to file
for e in sorted(pDict.keys()):
    for j in sorted(pDict[e]):
        if pDict[e][j] >=0.001:
            fout.write(e + ' : ' + j + ' # ' + '{0:.8f}'.format(pDict[e][j]) + '\n')


