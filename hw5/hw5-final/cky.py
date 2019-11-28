from collections import defaultdict
from tree import Tree
from pprint import pprint
import sys, string

fin = sys.stdin
fout = sys.stdout
ferr = sys.stderr

lines = [line.strip().split() for line in fin.readlines()]

trainbool = False
for i, arg in enumerate(sys.argv):
    if 'pcfg.bin' in arg:
        gfile = open(arg,'r')
    if 'train' in arg:
        trainfile = open(arg,'r')
        trainbool = True

if trainbool:
    tdict = {x.strip():'<unk>' for x in trainfile}

pdict = defaultdict(lambda: defaultdict(float))
for i,line in enumerate(gfile):
    line = line.strip()
    if i==0:
        start = line
    elif len(line) > 0:
        line = line.split('->')
        k1 = line[0].strip()
        line = line[1].split('#')
        k2 = line[0].strip().split()
        if len(k2) > 1:
            k2 = tuple(k2)
        else:
            k2 = k2[0]
        p = float(line[1].strip())
        pdict[k1][k2] = p

def print_dict(p,bck=None):
    for x in p:
        for a in p[x]:
            for b in p[x][a]:
                if p[x][a][b] >0:
                    ferr.write(''.join(str(zz)+' ' for zz in [x,a,b,p[x][a][b]])+'\n')
                    if bck is not None:
                        ferr.write(str(bck[x][a][b])+'\n')

def backtrace(back,X, i,j):
    if len(back[X][i][j]) == 1:
        return '('+ X + ' ' + back[X][i][j][0] + ')'
    else:
        YZ = back[X][i][j][0]
        k = back[X][i][j][1]
        if isinstance(YZ,tuple):
            return '('+ X + ' ' + backtrace(back,YZ[0],i,k) +' '+ backtrace(back,YZ[1],k,j) + ')'
        else:
            return '('+ X + ' ' + backtrace(back,YZ,i,j) + ')'


def debinarize(tree):
    if '_' in tree.label:
        subtrees = []
        for subtree in tree.subs:
            debinarized_sub = debinarize(subtree)
            if type(debinarized_sub) == list:
                subtrees += debinarized_sub
            else:
                subtrees += [debinarized_sub]
        # this is a forest
        return subtrees
        # return [debinarize(subtree) for subtree in tree.subs]
    # otherwise the root node is a regular node and returns a tree.
    else:
        # no children
        if tree.subs == None:
            return tree
        # children
        else:
            subtrees = []
            for sub in tree.subs:
                #this is for the non-smoothed version of the grammar
                # if '@' in sub.label:
                if '_' in sub.label:
                    # if the child node is one of the added ones, take its subtrees
                    # and attach them to the root node.
                    for subtree in sub.subs:
                        debinarized_sub = debinarize(subtree)
                        if type(debinarized_sub) == list:
                            subtrees += debinarized_sub
                        else:
                            subtrees.append(debinarized_sub)
                    # subtrees += [debinarize(subtree) for subtree in sub.subs]
                else:
                    debinarized_sub = debinarize(sub)
                    if type(debinarized_sub) == list:
                        subtrees += debinarized_sub
                    else:
                        subtrees += [debinarize(sub)]
                    # subtrees += [debinarize(sub)]
            return Tree(tree.label, tree.span, subs= subtrees)

trees = []
scores = []
for lnum, line in enumerate(lines):
    ferr.write('\n\nLine '+str(lnum)+': '+''.join(zz+' ' for zz in line)+'\n')
    
    score = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
    back = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    for i in range(len(line)):
        word = line[i]
        if trainbool:
            if word not in tdict.keys():
                word = '<unk>'
            else:
                word = string.lower(line[i])
        
        keys = [x for x in pdict.keys() if word in pdict[x].keys()]
        if len(keys) == 0:
            word = '<unk>'
        keys = [x for x in pdict.keys() if word in pdict[x].keys()]
        for X in keys:
            score[X][i][i+1] = pdict[X][word]
            back[X][i][i+1] = [line[i]]

        # Unaries
        changed = True
        while changed:
            changed = False
            for X in pdict:
                unary = [z for z in pdict[X].keys() if z in pdict.keys() and not isinstance(z,tuple)]
                for Y in unary:
                    if score[Y][i][i+1] > 0:
                        sc = 0
                        sc = pdict[X][Y] * score[Y][i][i+1]
                        if sc > score[X][i][i+1]:
                            score[X][i][i+1] = sc
                            back[X][i][i+1] = [Y,i+1]
                            changed = True
                                    
    for d in range(1,len(line)+1):
        for i in range(len(line)-d+1):
            j = i+d
            for k in range(i+1,j+1):
                for X in pdict:
                    unary = [z for z in pdict[X].keys() if z in pdict.keys() and not isinstance(z,tuple)]
                    binary = [z for z in pdict[X].keys() if isinstance(z,tuple)]

                    for YZ in binary:
                        sc = 0
                        if score[YZ[0]][i][k]*score[YZ[1]][k][j] > 0:
                            sc = pdict[X][YZ] * score[YZ[0]][i][k] * score[YZ[1]][k][j]
                            
                        if sc > score[X][i][j]:
                            score[X][i][j] = sc
                            back[X][i][j] = [YZ,k]
                            
            # unaries
            changed = True
            while changed:
                changed = False
                for X in pdict:
                    unary = [z for z in pdict[X].keys() if z in pdict.keys() and not isinstance(z,tuple)]
                    for Y in unary:
                        if score[Y][i][j] > 0:
                            sc = 0
                            sc = pdict[X][Y] * score[Y][i][j]
                            if sc > score[X][i][j]:
                                score[X][i][j] = sc
                                back[X][i][j] = [Y,j]
                                changed = True

##    ferr.write('\n')
##    ferr.write('Dictionary Final'+'\n')
##    print_dict(score,back)

    try:
        trees.append(str(debinarize(Tree.parse(backtrace(back,start,0,len(line)).strip()))))
        scores.append(score[start][0][len(line)])
    except:
        trees.append(None)
        scores.append(None)
    ferr.write(str(trees[-1])+'\n')
    ferr.write(str(scores[-1]))
    
for tree in trees:
    if tree is None:
        fout.write(str(tree)+'\n')
    else:
        fout.write(tree+'\n')
    

