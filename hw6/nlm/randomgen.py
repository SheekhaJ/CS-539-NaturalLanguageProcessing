import sys
import math
from nlm import NLM
from random import choices

fout = sys.stdout

NLM.load('base')
sentences = []
for _ in range(10):
    h = NLM()
    sent = ''
    choicechar = choices(population= [chr(a) for a in range(97,123)]+['_','</s>'], weights= h.next_prob().values())[0]
    i = 0
    while choicechar != '</s>':
        if choicechar != '_':
            sent += choicechar
        else:
            sent += ' '
        h += choicechar
        choicechar = choices(population= [chr(a) for a in range(97,123)]+['_','</s>'], weights= h.next_prob().values())[0]
    sentences.append(sent)

for s in sentences:
    fout.write(s+'\n\n')