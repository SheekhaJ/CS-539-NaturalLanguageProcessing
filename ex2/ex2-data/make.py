from collections import defaultdict

def unigramWFSA(unigramCount):
    with open('/nfs/stak/users/jariwals/Natural Language Processing/ex2/ex2-data/myuni.wfsa','w') as outFile:
        outFile.write('F\n')
        outFile.write('(0 (1 <s>))\n')
        
        totalCharCount = sum(unigramCount.values())

        for letter in unigramCount:
            prob = unigramCount[letter]/totalCharCount
            outFile.write('(1 (1 '+letter+' '+str(prob)+'))\n')
            if letter == '</s>':
                outFile.write('(1 (F </s> '+str(prob)+'))\n')        


def getCount(lines, ngram):
    counter = defaultdict(int)
    for line in lines:
        for word in line.strip().split():
            if '<s>' in word:
                word = word.replace('<s>','')
                counter['<s>'+word[:ngram-1]] += 1
            else:
                if '</s>' in word:
                    word = word.replace('</s>','')
                    if -ngram+1<0:
                        counter['</s>'+word[-ngram+1:]] += 1
                    if -ngram+1==0:
                        counter['</s>'] += 1
            for i in range(len(word)-ngram+1):
                counter[word[i:i+ngram]] += 1
    if '<' in counter: counter.pop('<')
    if '\/' in counter : counter.pop('>')
    if '>' in counter: counter.pop('/')

    return counter

if __name__ == '__main__':
    lines = ['<s>'+line.strip('\n')+'</s>' for line in open('/nfs/stak/users/jariwals/Natural Language Processing/ex2/ex2-data/test.txt','r').readlines()]
    lines = ['_'.join(line.split()) for line in lines]
    
    unigramCount = getCount(lines, 1)
    bigramCount = getCount(lines, 2)
    trigramCount = getCount(lines, 3)

    print(unigramCount)
    print(bigramCount)
    print(trigramCount)

    unigramWFSA(unigramCount)