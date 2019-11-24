from pprint import pprint
from tree import Tree
import sys

fin = sys.stdin
ferr = sys.stderr

trees = [line.strip() for line in fin.readlines()][:1]

for i,tree in enumerate(trees):
	trees[i] = Tree.parse(tree.strip())

#for t in trees:
#        pprint(t)

def binarizeTree(tree):
        if tree.word == None:
                for t in tree.subs:
                        binarizeTree(t)
                print('tree here: {} subs: {}'.format(tree, tree.subs))
                if len(tree.subs) > 2:
                        newlabel = tree.label+"'"
                        temptreestr = '('+newlabel + ' '+' '.join([t.dostr() for t in tree.subs[1:]])+')'
                        print('subs: {} new label: {} temptreestr: {}'.format(tree.subs, newlabel, temptreestr))
                        temptree = Tree.parse(temptreestr)
                        binarizeTree(temptree)
##                        tree = '('+tree.label+' '+temptree.dostr()+')'
                        print('new original tree: {}'.format(tree))
                return tree

for tree in trees:
        binarizeTree(tree)
print('---------------------------------------------------------')
for t in trees:
        print(t)
