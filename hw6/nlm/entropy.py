import sys
import math
from nlm import NLM

fin = sys.stdin
fout = sys.stdout

lines = [line.strip() for line in fin.readlines()]

NLM.load('base')
entropy, seqlen = 0, 0
for line in lines:
    h = NLM()
    for c in line:
        c = c if c != ' ' else '_'
        # entropy += -(h.next_prob(c) * math.log(h.next_prob(c),2))
        entropy += -math.log(h.next_prob(c),2)
        h += c
    # entropy += -(h.next_prob('</s>') * math.log(h.next_prob('</s>'),2))
    entropy += -math.log(h.next_prob('</s>'),2)
    h += '</s>'
    # print(h,end='\n\n')
    seqlen += len(line)+1
print('p: {}'.format(entropy/seqlen))