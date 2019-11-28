# from pprint import pprint
from tree import Tree
import sys

fin = sys.stdin
ferr = sys.stderr

trees = [line.strip() for line in fin.readlines()]
#print(trees)

for i,tree in enumerate(trees):
	trees[i] = Tree.parse(tree.strip())

words = {}
def getCount(tree):
        if tree.word != None:
                if tree.word not in words:
                        words[tree.word] = 1
                else:
                        words[tree.word] += 1
        else:
             for t in tree.subs:
                     getCount(t)

for tree in trees:
        getCount(tree)

def replaceOneCounts(tree,words):
        if tree.word != None:
                if words[tree.word] == 1:
                        tree.word = "<unk>"
        else:
                for t in tree.subs:
                        replaceOneCounts(t,words)

for tree in trees:
        replaceOneCounts(tree, words)

for tree in trees:
        print(tree)

for word,val in words.items():
        if val>1:
                ferr.write(word+'\n')
