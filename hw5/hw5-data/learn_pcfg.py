from collections import defaultdict
from tree import Tree
from pprint import pprint
import sys

fin = sys.stdin
fout = sys.stdout
ferr = sys.stderr

trees = [line.strip() for line in fin.readlines()]

for i,tree in enumerate(trees):
	trees[i] = Tree.parse(tree.strip())

gcounts = defaultdict(lambda : defaultdict(lambda : list))

def getcfgcounts(tree, gcounts):
        if tree.word == None:
                for t in tree.subs:
                        getcfgcounts(t,gcounts)
                if len(tree.subs) == 2:
                        children = ''
                        for t in tree.subs:
                                children += ' '+t.label
                        children = children.strip()
                        if children not in gcounts[tree.label]:
                                gcounts[tree.label][children] = 1
                        else:
                                gcounts[tree.label][children] += 1
                elif len(tree.subs)==1:
                        if tree.subs[0].label not in gcounts[tree.label]:
                                gcounts[tree.label][tree.subs[0].label] = 1
                        else:
                                gcounts[tree.label][tree.subs[0].label] += 1
                else:
                        print('something odd here! tree: {} gcounts:{}'.format(tree, gcounts))
        else:
                if tree.label not in gcounts[tree.label]:
                        gcounts[tree.label][tree.word] = 1
                else:
                        gcounts[tree.label][tree.word] += 1

for tree in trees:
        getcfgcounts(tree, gcounts)

##print('gcounts: '.format(gcounts))
##for k,v in gcounts.items():
##        print('{} : {}'.format(k,v))

pcfgs = {x : {c : float(gcounts[x][c])/sum(gcounts[x].values()) for c in gcounts[x]} for x in gcounts}
##for k,v in pcfgs.items():
##        print('{} : {}'.format(k,v))

fout.write('TOP\n')
for key,val in pcfgs.items():
        for k,v in pcfgs[key].items():
                fout.write('{} -> {} # {:0.4f}\n'.format(key,k,pcfgs[key][k]))
