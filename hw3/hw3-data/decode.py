import argparse, sys
from collections import defaultdict
from operator import itemgetter

f = sys.stdin
fout = sys.stdout
ferr = sys.stderr
probs = sys.argv[1:]

kbest = 1
for i, arg in enumerate(probs):
    if '-' == arg[0]:
        kbest = int(arg[1:])
        probs.pop(i)



# Get list of input lines with jprons separated
inlines = [['<s>']+b.strip().split()+['</s>'] for l in [x.strip().split('\\n') for x in f] for b in l]

# Build eprons trigram probability dict
ep = [line.split() for line in open(probs[0],'r')]
eprobs = defaultdict(lambda : defaultdict(lambda : defaultdict(lambda : defaultdict(float))))
for l in ep:
        eprobs[l[0]][l[1]][l[3]] = float(l[5])


# Build eprons-jprons probability dict
ej = [line.strip().split() for line in open(probs[1],'r')]
ejprobs = defaultdict(lambda : defaultdict(lambda : defaultdict(float)))

for l in ej:
    j = ''
    for i in range(2,len(l)-2):
        j += ' '+l[i]
    ejprobs[l[0]][j.strip()] = float(l[-1])
    

###### Write viterbi here  ###########
##  'ej' is the eprons-jprons probability dict
##  example: ej[epron][jpron] = float(p)
##
##  'ep' is the eprons trigram probability dict
##  example: ej[e1][e2][e3] = float(p)
##
##  'inlines' is the list of lists of input jprons
##  example: [['P','I','A','N','O'],['N','A','I','T','O']]

def backtrack(jnum, prev, tag):
    if jnum==0:
        return []
    return backtrack(int(back[jnum][prev][tag][1]), back[jnum][prev][tag][0], prev) + [(word[i], tag)]
   


for wnum, word in enumerate(inlines,1):   
    best = defaultdict(lambda : defaultdict(lambda : defaultdict(float)))
    best[0]['<s>']['<s>'] = 1
    back = defaultdict(lambda : defaultdict(lambda : defaultdict(lambda : defaultdict(lambda : defaultdict(str)))))
    for i in range(1,len(word)):
       for k in range(3):
            jnum = i-k
            if jnum < 1:
                continue
            jpron = ''
            for j in word[i-k:i+1]:
                jpron += ' '+j
            jpron = jpron.strip()
            eprons = [epron for epron in ejprobs.keys() if jpron in ejprobs[epron].keys()]
            for epron in eprons:
                for prev2 in best[jnum-1]:
                    for prev1 in best[jnum-1][prev2]:
                        if epron in eprobs[prev2][prev1]:
                            score = best[jnum-1][prev2][prev1] * eprobs[prev2][prev1][epron] * ejprobs[epron][jpron]
                            if score>best[i][prev1][epron]:
                                best[i][prev1][epron] = score
                                back[i][prev1][epron][0] = prev2
                                back[i][prev1][epron][1] = str(jnum-1)


    paths = []
    jnum = len(word)-1
    for prev in best[jnum]:
        for epron in best[jnum][prev]:
            paths.append([jnum,prev,best[jnum][prev][epron]])
    
    paths = sorted(paths, key=itemgetter(2))
    for path in paths:
        print(path)

    win = ''
    for a in word[1:-1]:
        win += ' '+a
    fout.write('\nInput '+str(wnum)+': '+win.strip()+'\n')

    for i in range(kbest):
        bestp = paths[-1-i]
        bt = backtrack(bestp[0], bestp[1],"</s>")[:-1]
        
        wout = ''
        for a in bt:
            wout += ' '+a[1]        
        
        ferr.write(wout.strip()+' # '+str.format('{0:.6e}',best[bestp[0]][bestp[1]]['</s>'])+'\n')
    