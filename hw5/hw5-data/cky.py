from collections import defaultdict
from tree import Tree
from pprint import pprint
import sys

fin = sys.stdin
fout = sys.stdout
ferr = sys.stderr

lines = [line.strip() for line in fin.readlines()]
##print(lines)

pcfgslines = [line.strip() for line in open(sys.argv[1],'r')][1:]
##print(pcfgslines)

pcfgs = defaultdict(lambda : defaultdict(lambda : defaultdict(lambda : float(0))))
for line in pcfgslines:
        line = line.split('->')
        parent = line[0]
        line = line[1].split('#')
        children, prob = line[0].strip(), line[-1]
        if len(children.split()) > 1:
                child1, child2 = children.split()[0], children.split()[1]
                pcfgs[parent][child1][child2] = prob
        else:
                pcfgs[parent][children] = prob

##for k,v in pcfgs.items():
##        print('{} : {}'.format(k,v))


