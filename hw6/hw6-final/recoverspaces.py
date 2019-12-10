import sys
import math
from nlm import NLM

# sents = ['therestcanbeatotalmessandyoucanstillreaditwithoutaproblem', 'thisisbecausethehumanminddoesnotreadeveryletterbyitselfbutthewordasawhole']
fin = sys.stdin
fout = sys.stdout

sents = [line.strip() for line in fin.readlines()]
sents = [sent.replace(' ','') for sent in sents]

bw = 20

NLM.load('base')
for sent in sents:
    h = NLM()
    prevbeam = [(0, h)]
    for i,c in enumerate(list(sent)+["</s>"]):
        currbeam = []
        for prob, h in prevbeam:
            currbeam.append((prob-math.log(h.next_prob(c)), h+c))
            currbeam.append((prob-math.log(h.next_prob(c))-math.log((h+c).next_prob('_')), h+c+'_'))
            # print(currbeam)
        if len(currbeam) > bw:
            # print(currbeam)
            currbeam = sorted(currbeam)[:bw]
            # print(currbeam)
            # exit()
        prevbeam = currbeam
        # print(prevbeam)
    
    print(''.join(prevbeam[0][1].history[1:][:-1]).replace("_", " "))