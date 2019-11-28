from collections import defaultdict
from tree import Tree
from pprint import pprint
import sys

fin = sys.stdin
fout = sys.stdout
ferr = sys.stderr

trees = [Tree.parse(line.strip()) for line in fin.readlines()]

def binarize(tree):
        # no children
        if tree.subs == None:
            return tree
        
        if len(tree.subs) <= 2:
            newsubs = []
            for subtree in tree.subs:
                newsubs.append(binarize(subtree))

            return Tree(tree.label, tree.span, subs=newsubs)
        else:
            subs = [tree.subs[0]]
            newsubs = tree.subs[1:]
            newspan = [subs[0].span[1],tree.span[0]]
            
            if '_' in tree.label:
                newlabel = tree.label
            else:
                newlabel = tree.label+'_'

            newtree = Tree(label=newlabel,span=newspan,subs=newsubs)
            subs.append(newtree)
            
            return binarize(Tree(tree.label, tree.span, subs= subs))



for tree in trees:
    fout.write(str(binarize(tree))+'\n')
