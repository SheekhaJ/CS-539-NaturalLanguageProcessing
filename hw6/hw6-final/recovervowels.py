import math
from nlm import NLM
import sys

fin = sys.stdin
fout = sys.stdout

lines = [line.strip() for line in fin.readlines()]
newlines = []
vowels = ['a','e','i','o','u']
bw = 40

NLM.load('base')
for k,line in enumerate(lines):
    newline = ''.join([c for c in line if c not in vowels])
    newline = [c if c!=' ' else '_' for c in newline]
    h = NLM()
    prevbeam = [(0,h)]
    for i,c in enumerate(newline+['</s>']):
        currbeam = []
        for prob, h in prevbeam:
            currbeam.append((prob-math.log(h.next_prob(c)), h+c))
            for v1 in vowels:
                currbeam.append((prob-math.log((h+v1).next_prob(c))-math.log(h.next_prob(v1)), h+v1+c))
                for v2 in vowels:
                    currbeam.append((prob-math.log((h+v1+v2).next_prob(c))-math.log((h+v1).next_prob(v2))-math.log(h.next_prob(v1)), h+v1+v2+c))
        if len(currbeam) > bw:
            currbeam = sorted(currbeam)[:bw]
        prevbeam = currbeam
    print('{}: {}'.format(k,''.join(prevbeam[0][1].history[1:][:-1]).replace("_", " ")))
