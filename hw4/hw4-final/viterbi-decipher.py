from collections import defaultdict
import sys, math, string, operator

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
    if '.probs' in arg:
        cprobs_file = arg


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
        for j in d[e]:
            if d[e][j] >= 0.01:
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

# Build cprobs probability dict
ej = [line for line in open(cprobs_file,'r')]
cprobs = defaultdict(lambda : defaultdict(lambda : defaultdict(float)))


for l in ej:
    x1 = l[0]
    x2 = l[l.find(':')+1:l.find('#')].strip()
    if x2 == '':
        x2 = ' '
    p = l[l.rfind('#')+1:].strip()
    cprobs[x1][x2] = float(p)

##### Start EM

alphabet = [x for x in string.ascii_lowercase]+[' ']
pDict = init_probs()
bigram = init_bigram()

def backtrack(a, e, back):
    if e==0:
        return []
    return backtrack(back[e][a], e-1, back) + [a]

bestaligns = []
for cline in cipher:
    # forward viterbi
    best = defaultdict(lambda: defaultdict(float))
    back = defaultdict(lambda: defaultdict(float))
    best[0][' '] = 1
    for e, char in enumerate(cline):
        for pre in list(best[e].keys()):
            for a in [x for x in alphabet if char in cprobs[x]]:
                score = best[e][pre] * cprobs[a][char] * bigram[pre][a]
                if score > best[e+1][a]:
                    best[e+1][a] = score
                    back[e+1][a] = pre

    laste = len(cline)
    bestj = list(sorted(best[laste].items(), key = operator.itemgetter(1)))
    bestj = bestj[-1][0]
    
    bestaligns.append(backtrack(bestj, laste, back))

##    print('###############3')
for x, b in enumerate(bestaligns):
    fout.write(''.join(b).strip()+'\n')













