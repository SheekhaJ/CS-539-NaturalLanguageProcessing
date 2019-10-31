import sys
from collections import defaultdict

fin = sys.stdin

sents = ['<s> '+line.strip()+' </s>' for line in fin]
words = [word for sent in sents for word in sent.split()]
tags, ptag, pword = defaultdict(list), defaultdict(lambda : defaultdict(float)), defaultdict(lambda : defaultdict(float))

for line in open('lexicon.wfst','r').readlines()[1:]:
    line = line.strip()
    word = line.split()[2]
    tag = line.split()[3]
    prob = line.split()[4].replace('))','')
    tags[word].append(tag)
    pword[tag][word] = float(prob)

tags['<s>'].append('<s>')
tags['</s>'].append('</s>')
pword['</s>']['</s>']=1

for line in open('bigram.wfsa','r').readlines()[1:]:
    line = line.strip()
    tag1, tag2, prob = line.split()[0].replace('(','').replace('0','<s>'), line.split()[1].replace('(','').replace('1','</s>'), line.split()[3].replace('))','')
    ptag[tag1][tag2] = float(prob)
    
best = defaultdict(lambda : defaultdict(float))
best[0]['<s>']=1
back = defaultdict(lambda : defaultdict(str))

for i, word in enumerate(words[1:],1):
    for tag in tags[word]:
        for prev in best[i-1]:
            if tag in ptag[prev]:
                score = best[i-1][prev] * ptag[prev][tag] * pword[tag][word]
                if score>best[i][tag]:
                    best[i][tag] = score
                    back[i][tag] = prev

def backtrack(i, tag):
    if i==0:
        return []
    return backtrack(i-1, back[i][tag]) + [(words[i], tag)]

print(backtrack(len(words)-1, "</s>")[:-1])