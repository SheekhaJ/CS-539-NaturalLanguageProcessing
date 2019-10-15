from collections import defaultdict
from itertools import product

def getStr(l):
    return ''.join(l)

def trigramWFSA(unigramCount, bigramCount, trigramCount, trigramAll):
    outStr = 'F\n'
    outStr += '(0 (<s> <s>))\n'

    for key, value in trigramCount.items():
        if '<s>'in key:
            destState = key.replace('<s>','')
            prob = float(bigramCount['<s>'+destState[0]])/unigramCount[destState[0]]
            outStr += '(<s> (<s>'+destState[0]+' '+destState[0]+'))\n'
            
            prob = float(trigramCount[key])/bigramCount['<s>'+destState[0]]
            outStr += '(<s>'+destState[0]+' ('+destState+' '+destState[1]+' '+str(prob)+'))\n'
        elif '</s>' in key:
            c = key.replace('</s>','')
            prevState = c[1]+'</s>'
            prob = float(trigramCount[key])/bigramCount[c]
            outStr += '('+c+' (F </s> '+str(prob)+'))\n'
        else:
            prevState = key[:-1]
            c = key[-1]
            prob = float(trigramCount[key])/bigramCount[prevState]
            outStr += '('+prevState+' ('+key[1:]+' '+c+' '+str(prob)+'))\n'

    for key in trigramAll:
        if key not in trigramCount.keys():
            if '<s>'in key:
                if len(key.replace('<s>','')) in [0,1]:
                    continue
                destState = key.replace('<s>','')
                prob = float(bigramCount['<s>'+destState[0]])/unigramCount[destState[0]]
                outStr += '(<s> (<s>'+destState[0]+' '+destState[0]+'))\n'
                
                prob = float(trigramCount[key])/bigramCount['<s>'+destState[0]]
                outStr += '(<s>'+destState[0]+' ('+destState+' '+destState[1]+' '+str(prob)+'))\n'
            elif '</s>' in key:
                if key.find('</s>') in [0,1,4]:
                    continue
                c = key.replace('</s>','')
                prevState = c[1]+'</s>'
                prob = float(trigramCount[key])/bigramCount[c]
                outStr += '('+c+' (F </s> '+str(prob)+'))\n'
            else:
                # if key.find('</s>') in [0,1,4] or key.find('<s>') in [1,2,4]:
                #     continue
                prevState = key[:-1]
                c = key[-1]
                prob = float(trigramCount[key])/bigramCount[prevState]
                outStr += '('+prevState+' ('+key[1:]+' '+c+' '+str(prob)+'))\n'

    return outStr

def bigramWFSA(unigramCount, bigramCount, bigramAll):
    N = sum(unigramCount.values())
    V = 28**2
    outStr = 'F\n'
    outStr += '(0 (<s> <s>))\n'

    for key, value in bigramCount.items():
        if '<s>' in key:
            c = key.replace('<s>','')
            prob = float(bigramCount[key])/(unigramCount['<s>'] + V)
            outStr += '(<s> ('+c+' '+c+' '+str(prob)+'))\n'
        elif '</s>' in key:
            c = key.replace('</s>','')
            prob = float(bigramCount[key])/(unigramCount[c] + V)
            outStr += '('+c+' (F </s> '+str(prob)+'))\n'
        else:
            prob = float(bigramCount[key])/(unigramCount[key[0]] + V)
            outStr += '('+key[0]+' ('+key[1]+' '+key[1]+' '+str(prob)+'))\n'

    for key in bigramAll:
        if key not in bigramCount.keys():
            if '<s>' in key:
                c = key.replace('<s>','')
                prob = float(bigramCount[key])/(unigramCount['<s>'] + V)
                outStr += '(<s> ('+c+' '+c+' '+str(prob)+'))\n'
            elif '</s>' in key:
                c = key.replace('</s>','')
                prob = float(bigramCount[key])/(unigramCount[c] + V)
                outStr += '('+c+' (F </s> '+str(prob)+'))\n'
            elif '<s></s>' in key:
                continue
            else:
                prob = float(bigramCount[key])/(unigramCount[key[0]] + V)
                outStr += '('+key[0]+' ('+key[1]+' '+key[1]+' '+str(prob)+'))\n'
        
    return outStr

def unigramWFSA(unigramCount, smoothing=False):
    outStr = 'F\n'
    outStr += '(0 (1 <s>))\n'
    totalCharCount = float(sum(unigramCount.values())-unigramCount['<s>'])

    for key, value in unigramCount.items():
        if key in ['<s>','</s>']:
            continue
        prob = value/totalCharCount
        outStr += '(1 (1 '+key+' '+str(prob)+'))\n'
    outStr += '(1 (F </s> '+str(unigramCount['</s>']/totalCharCount)+'))\n'
    
    return outStr

def getCount(lines, ngram):
    counter = defaultdict(lambda:1)

    for line in lines:
        for i in range(len(line)-ngram):
            counter[''.join(line[i:i+ngram])] += 1
        counter[''.join(line[-ngram:])] += 1

    return counter

def generator(l):
    res = []
    seq = list(map(chr, range(97,123)))+['<s>','</s>','_']
    for comb in product(seq, repeat=l):
        res.append(''.join(comb))
    
    return res


if __name__ == '__main__':
    lines = [line.strip('\n') for line in open('/nfs/stak/users/jariwals/Natural Language Processing/ex2/ex2-data/train.txt','r').readlines()]
    # lines = ['_'.join(map(lambda s : s.replace(' ',''), line.split())) for line in lines]
    lines = ['_'.join(line.split()) for line in lines]
    lines = [['<s>']+[l for l in line]+['</s>'] for line in lines]
    
    unigramCount = getCount(lines,1)
    bigramCount = getCount(lines,2)
    trigramCount = getCount(lines,3)

    unigramAll = generator(1)
    bigramAll = generator(2)
    trigramAll = generator(3)

    for key in trigramAll:
        if key.find('</s>') in [0,1,4] or key.find('<s>') in [1,2,4]:
            trigramAll.remove(key)

    # print(len(unigramAll))
    # print(len(bigramAll))
    # print(len(trigramAll))

    # print(unigramCount)
    # print(bigramCount)
    # print(trigramCount)

    # print(len(unigramCount))
    # print(len(bigramCount))
    # print(len(trigramCount))

    # with open('/nfs/stak/users/jariwals/Natural Language Processing/ex2/ex2-data/myuni.wfsa','w') as outFile:
    #     outFile.write(unigramWFSA(unigramCount))

    # with open('/nfs/stak/users/jariwals/Natural Language Processing/ex2/ex2-data/mybi.wfsa','w') as outFile:
    #     outFile.write(bigramWFSA(unigramCount, bigramCount, bigramAll))

    # with open('/nfs/stak/users/jariwals/Natural Language Processing/ex2/ex2-data/mytri.wfsa','w') as outFile:
    #     outFile.write(trigramWFSA(unigramCount, bigramCount, trigramCount))

    # print(unigramWFSA(unigramCount))
    # print(bigramWFSA(unigramCount, bigramCount))
    # print(trigramWFSA(unigramCount, bigramCount, trigramCount))

    with open('/nfs/stak/users/jariwals/Natural Language Processing/ex2/ex2-data/unigram.wfsa','w') as outFile:
        outFile.write(unigramWFSA(unigramCount))

    # with open('/nfs/stak/users/jariwals/Natural Language Processing/ex2/ex2-data/bigram.wfsa','w') as outFile:
    #     outFile.write(bigramWFSA(unigramCount, bigramCount, bigramAll))

    # with open('/nfs/stak/users/jariwals/Natural Language Processing/ex2/ex2-data/trigram.wfsa','w') as outFile:
    #     outFile.write(trigramWFSA(unigramCount, bigramCount, trigramCount, trigramAll))