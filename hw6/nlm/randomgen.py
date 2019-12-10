import sys
import math
from nlm import NLM
from random import choices
import random

fout = sys.stdout

NLM.load('large')
sentences = []
for _ in range(10):
    h = NLM()
    sent = ''
    choicekeys = list(h.next_prob().keys())
    choicechar = choices(population = choicekeys, weights = h.next_prob().values())[0]
    while choicechar != '</s>':
        if choicechar != '_':
            sent += choicechar
        else:
            sent += ' '
        h += choicechar
        choicekeys = list(h.next_prob().keys())
        choicechar = choices(population = choicekeys, weights = h.next_prob().values())[0]
    sentences.append(sent)

for s in sentences:
    fout.write(s+'\n\n')