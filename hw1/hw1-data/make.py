from collections import defaultdict
import sys

class TrieNode:
    def __init__(self):
        self.dict = defaultdict(TrieNode)
        self.end = False

def insert(root,word):
    outStr = ''
    word = ''.join(word.split())
    node = root
    prevState, destState = str(0), ''
    for i,c in enumerate(word):
        if c in node.dict.keys():
            prevState = word[:i+1]
            node = node.dict[c]
            continue
        destState = word[:i+1].strip()
        outStr += '('+prevState+' ('+destState+' '+c+'))\n'
        prevState, destState = destState, prevState+c
        node = node.dict[c]
    outStr += '('+prevState+' (1 *e*))\n'

    return outStr


if __name__ == '__main__':
    # inFile = sys.argv[1]
    # outFile = sys.argv[2]
    prefixTree = TrieNode()
    inStr = ''
    outStr = '1\n'
    # print(sys.stdin.readlines())
    # for line in sys.stdin.readlines():
    #     for word in line:

    for word in sys.stdin.readlines():
    # for word in "A T _ A N _ A G E".strip().split('_'):
        word = word.strip()
        root = prefixTree
        outStr += insert(root,word)
    outStr += '(1 (0 _))'
    print(outStr)
    # print('hello world')
    
    # with open(outFile,'w') as outFile:
    #     outFile.write(outStr)