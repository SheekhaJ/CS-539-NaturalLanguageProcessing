from collections import defaultdict

def getStr(l):
    return ''.join(l)

def trigramWFSA(unigramCount, bigramCount, trigramCount):
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

    return outStr

def bigramWFSA(unigramCount, bigramCount):
    outStr = 'F\n'
    outStr += '(0 (<s> <s>))\n'

    for key, value in bigramCount.items():
        if '<s>' in key:
            c = key.replace('<s>','')
            prob = float(bigramCount[key])/unigramCount['<s>']
            outStr += '(<s> ('+c+' '+c+' '+str(prob)+'))\n'
        elif '</s>' in key:
            c = key.replace('</s>','')
            prob = float(bigramCount[key])/unigramCount[c]
            outStr += '('+c+' (F </s> '+str(prob)+'))\n'
        else:
            prob = float(bigramCount[key])/unigramCount[key[0]]
            outStr += '('+key[0]+' ('+key[1]+' '+key[1]+' '+str(prob)+'))\n'
        
    return outStr

def unigramWFSA(unigramCount):
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
    counter = defaultdict(int)

    for line in lines:
        for i in range(len(line)-ngram):
            counter[''.join(line[i:i+ngram])] += 1
        counter[''.join(line[-ngram:])] += 1

    return counter

if __name__ == '__main__':
    lines = [line.strip('\n') for line in open('/nfs/stak/users/jariwals/Natural Language Processing/ex2/ex2-data/train.txt','r').readlines()]
    lines = ['_'.join(line.split()) for line in lines]
    lines = [['<s>']+[l for l in line]+['</s>'] for line in lines]
    
    unigramCount = getCount(lines,1)
    bigramCount = getCount(lines,2)
    trigramCount = getCount(lines,3)

    # print(unigramCount)
    # print(bigramCount)
    # print(trigramCount)

    # print(len(unigramCount))
    # print(len(bigramCount))
    # print(len(trigramCount))

    with open('/nfs/stak/users/jariwals/Natural Language Processing/ex2/ex2-data/myuni.wfsa','w') as outFile:
        outFile.write(unigramWFSA(unigramCount))

    with open('/nfs/stak/users/jariwals/Natural Language Processing/ex2/ex2-data/mybi.wfsa','w') as outFile:
        outFile.write(bigramWFSA(unigramCount, bigramCount))

    with open('/nfs/stak/users/jariwals/Natural Language Processing/ex2/ex2-data/mytri.wfsa','w') as outFile:
        outFile.write(trigramWFSA(unigramCount, bigramCount, trigramCount))

    # print(unigramWFSA(unigramCount))
    # print(bigramWFSA(unigramCount, bigramCount))
    # print(trigramWFSA(unigramCount, bigramCount, trigramCount))
    