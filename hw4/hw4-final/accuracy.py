import sys

fin = sys.stdin

def getAccuracy(files):
    for i,fs in enumerate(files):
        plain, deciphered = fs[0], fs[1]
        with open(plain) as p, open(deciphered) as d:
            pStr, dStr = '', ''
            pStr, dStr = [pStr+ps for ps in p.readlines()], [dStr+ds for ds in d.readlines()]
            hits = sum([1 for x,y in zip(pStr, dStr) for a,b in zip(x,y) if a==b])
            totals = sum([len(y) for x,y in zip(pStr,dStr)])
            accuracy = round(float(hits/totals)*100,2)
            print(fs, accuracy)
    return None

if __name__ == "__main__":
    files = [line.strip() for line in fin.readlines()]
    files = [(file.split()[0],file.split()[1]) for file in files]
    getAccuracy(files)