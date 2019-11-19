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

lines = list(filter(lambda x:x!='' ,[w.strip() for w in fin.readlines()]))

ewords, jwords = [], []
for i,line in enumerate(lines):
    if i%3==0:
        ewords.append(line.split())
    else:
        if '1' not in line:
            jwords.append(line.split())

kbest = 1
for i, arg in enumerate(args):
    if 'eword.wfsa' in arg:
        eword_file = arg
    if 'eword-epron' in arg:
        ewep_file = arg
    if 'epron-jpron' in arg:
        ejfile = arg
    
    if '-' == arg[0]:
        kbest = int(arg[1:])
        args.pop(i)

# Build eprons-jprons probability dict
ej = [line.strip().split() for line in open(ejfile,'r')]
ejprobs = defaultdict(lambda : defaultdict(lambda : defaultdict(float)))

for l in ej:
    j = ''
    for i in range(2,len(l)-2):
        j += ' '+l[i]
    ejprobs[l[0]][j.strip()] = float(l[-1])


def backtrack(jnum, e, x, back):
    if e==0:
        return []
    j = back[e][jnum]
    return backtrack(j, e-1, x, back) + [str(e)+' ']*(jnum-j)

bestaligns = []
for x in range(len(ewords)):
    
    # forward viterbi
    best = defaultdict(lambda: defaultdict(float))
    back = defaultdict(lambda: defaultdict(float))
    best[0][0] = 1
    
    for e, ephon in enumerate(ewords[x]):
        for j in best[e]:
            for k in range(1,min(len(jwords[x])-j,3)+1):
                jnum = j+k
                jphon = ''.join([j+' ' for j in jwords[x][j:jnum]]).strip()
                if jphon in ejprobs[ephon] and j >= e-1:
                    score = best[e][j] * ejprobs[ephon][jphon]

                    if score > best[e+1][j+k]:
                        best[e+1][jnum] = score
                        back[e+1][jnum] = j


    
    laste = len(ewords[x])
    bestj = len(jwords[x])
    score = 0
    
    bestaligns.append(backtrack(bestj, laste, x, back))

##    print('###############3')
for x, b in enumerate(bestaligns):
    ewd = [j+' ' for j in ewords[x]]
    jwd = [j+' ' for j in jwords[x]]
    
    
    fout.write(''.join(ewd).strip()+'\n')
    fout.write(''.join(jwd).strip()+'\n')
    fout.write(''.join(b).strip()+'\n')













