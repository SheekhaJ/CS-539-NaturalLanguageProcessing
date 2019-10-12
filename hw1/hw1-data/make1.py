from collections import defaultdict
import sys

class TrieNode:
    def __init__(self):
        self.dict = defaultdict(TrieNode)
        self.count = 0

def insertWord(root, word):
    word = ''.join(word.split())
    node = root
    for i,c in enumerate(word):
        node.count += 1
        node = node.dict[c]
    
def printToFSA(root,word,wordsLen):
    outStr = ''
    word = ''.join(word.split())
    node = root
    prevState, destState = str(0), ''
    for i,c in enumerate(word):
        destState = word[:i+1].strip()
        prob = float(node.count)/wordsLen
        outStr += '('+prevState+' ('+destState+' '+c+' '+str(prob)+'))\n'
        prevState, destState = destState, prevState+c
        node = node.dict[c]
    
    node.end = True
    outStr += '('+prevState+' (1 *e* 1))\n'

    return outStr


if __name__ == '__main__':
    prefixTree = TrieNode()
    inStr = ''
    outStr = '1\n'
    countDict = defaultdict(int)

    # for word in sys.stdin.readlines():
    # for word in open('vocab', 'r').readlines():
    with open('strings','r') as f:
        mStr = f.readlines()
    
    words = mStr[0].strip('\n').split('_')
    for line in mStr:
        words.extend(line.strip('\n').split('_'))
    
    for word in words:
        word = word.strip()
        root = prefixTree
        insertWord(root, word)
    
    visited = defaultdict(bool)

    # for word in sys.stdin.readlines():
    # for word in "A T _ A N _ A G E".strip().split('_'):
    # for word in open('vocab', 'r').readlines():
    for word in words:
        word = word.strip()
        root = prefixTree
        outStr += printToFSA(root,word,len(words))
    outStr += '(1 (0 _ 1))'
    print(outStr)