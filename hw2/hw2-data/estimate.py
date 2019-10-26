#!user/bin/python3

import sys, string
import numpy as np

f = sys.stdin
fout = sys.stdout

w0 = 0
thresh = 0.01

flines = [line.strip().split(' ') for line in f]
epron = flines[0::3]
jpron = flines[1::3]
ej = flines[2::3]

# get phoneme names from data
enames = []
jnames = []
for lnum, line in enumerate(epron):
    for enum, echar in enumerate(line):
        if echar not in enames:
            enames.append(echar)
            
        jchar = ''
        k = 0
        for i, e in enumerate(ej[lnum]):
            e = int(e)-1
            if e == enum:
                k+=1
                if k > 3:
                    continue
                jchar += ' '+jpron[lnum][i]
        jchar = jchar.strip()
        if jchar not in jnames:
            jnames.append(jchar)

# build dictionary for counting transitions
cdict = {x: {c: float(w0) for c in jnames} for x in enames}

# count transitions in data
for lnum, line in enumerate(epron):
    for enum, echar in enumerate(line):
        jchar = ''
        k = 0
        for i, e in enumerate(ej[lnum]):
            e = int(e)-1
            if e == enum:
                k+=1
                if k > 3:
                    continue
                jchar += ' '+jpron[lnum][i]
        jchar = jchar.strip()
        
        cdict[echar][jchar] += 1
    
# calculate probabilities from counts
norm_dict = {x: {c: float(cdict[x][c]/sum(cdict[x].values())) for c in cdict[x]} for x in cdict}

# remove probabilities less than thresh
for x in norm_dict:
    for c in norm_dict[x]:
        if norm_dict[x][c] < thresh:
            norm_dict[x][c] = float(0)

# re-normalize probabilties
norm_dict = {x: {c: float(norm_dict[x][c]/sum(norm_dict[x].values())) for c in norm_dict[x]} for x in norm_dict}

# write transition probabilities to fout
for x in sorted(norm_dict.keys()):
    for c in sorted(norm_dict[x].keys()):
        if norm_dict[x][c] > 0:
            fout.write(x + ' : ' + c + ' # '+str(norm_dict[x][c])+'\n')


