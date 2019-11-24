from collections import defaultdict
from tree import Tree
from pprint import pprint
import sys

fin = sys.stdin
ferr = sys.stderr

trees = [line.strip() for line in fin.readlines()]

for i,tree in enumerate(trees):
	trees[i] = Tree.parse(tree.strip())

gcounts = defaultdict(lambda : defaultdict(lambda : list))

def getpcfgs(tree, gcounts):
##        print('tree in method: {}'.format(type(tree)))
        if tree.word == None:
                for t in tree.subs:
                        getpcfgs(t,gcounts)
                if len(tree.subs) == 2:
##                        print('tree: {} label: {}'.format(tree, tree.label))
                        children = ''
                        for t in tree.subs:
                                children += ' '+t.label
                        children = children.strip()
                        if children not in gcounts[tree.label]:
                                gcounts[tree.label][children] = 1
                        else:
                                gcounts[tree.label][children] += 1
                elif len(tree.subs)==1:
##                        print('unary case: {} child: {}'.format(tree, tree.subs[0].label))
                        if tree.subs[0].label not in gcounts[tree.label]:
                                gcounts[tree.label][tree.subs[0].label] = 1
                        else:
                                gcounts[tree.label][tree.subs[0].label] += 1
                else:
                        print('something odd here! tree: {} gcounts:{}'.format(tree, gcounts))
        else:
##                print('3) tree: {} tree.label: {} tree.word: {}'.format(tree, tree.label, tree.word))
                if tree.label not in gcounts[tree.label]:
                        gcounts[tree.label][tree.word] = 1
                else:
                        gcounts[tree.label][tree.word] += 1
##        print('gcounts: {}'.format(gcounts))

for tree in trees:
##        print('tree type: {}'.format(type(tree)))
        getpcfgs(tree, gcounts)

#pgdict = {label : {} if }

print('gcounts: {}'.format(gcounts))
