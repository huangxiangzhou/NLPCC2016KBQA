import sys
import os
import codecs
import re



ft = open('nlpcc-iccpol-2016.kbqa.training-data','r',encoding='utf8')

p = re.compile(r'\s')

ftList = []
ftAList = []
for line in ft:
    if line[1] == 't':
        tripleTmp = set()
        assert(' === ' not in line)
        lineTmp = line.replace(' ||| ', ' === ', 1)
        lineTmp = lineTmp[:lineTmp.index(' |||')+4].replace(' === ',' ||| ',1)
        lineTmp, n = p.subn('',lineTmp)
        tripleTmp.add(lineTmp.lower())
        ftList.append(tripleTmp)
    if line[1] == 'a':
        answerTmp = line[line.index('\t')+1:].strip().lower()
        answerSet = set()
        indexS = answerTmp.find(' | ')
        if indexS == -1:
            answerTmp, n = p.subn('',answerTmp)
            answerSet.add(answerTmp)
        while answerTmp.find(' | ') != -1:
            indexS = answerTmp.index(' | ')
            answerCell = answerTmp[:indexS]
            answerCell, n = p.subn('',answerCell) 
            answerSet.add(answerCell)
            answerTmp = answerTmp[indexS+3:]        
        ftAList.append(answerSet)

faDict = {}

faADict = {}


tripleResult = {}
answerResult = {}

for wi in range(101):
    path = 'answer.Training.wAP100.wP'+str(wi)
    if os.path.exists(path) != True:
        continue
        
    fa = open(path,'r',encoding='utf8')
    keyi = 'w' + str(wi)
    faDict[keyi] = []

    faADict[keyi] = []

    for line in fa:
        if line[1] == 't':
            tripleTmp = set()
            if line.replace('======','',1).find('======') != -1:
                lineCopy = line
                while lineCopy.replace('======','',1).find('======') != -1:
                    line1 = lineCopy[:lineCopy.index(' ====== ')]
                    assert(' === ' not in line1)
                    lineTmp = line1.replace(' ||| ', ' === ', 1)
                    lineTmp = lineTmp[:lineTmp.index(' |||')+4].replace(' === ',' ||| ',1)
                    lineTmp, n = p.subn('',lineTmp)
                    tripleTmp.add(lineTmp.lower())
                    lineCopy = lineCopy[lineCopy.index(' ====== ') + 8:]
                faDict[keyi].append(tripleTmp)
                continue
            assert(' === ' not in line)
            lineTmp = line.replace(' ||| ', ' === ', 1)
            lineTmp = lineTmp[:lineTmp.index(' |||')+4].replace(' === ',' ||| ',1)
            lineTmp, n = p.subn('',lineTmp)
            tripleTmp.add(lineTmp.lower())
            faDict[keyi].append(tripleTmp)

        if line[1] == 'a':
            answerTmp = line[line.index('\t')+1:].strip('\n').lower()
            answerSet = set()
            if answerTmp.find(' ||| ') != -1:
                faADict[keyi].append(answerSet)
                continue
                       
            indexS = answerTmp.find(' | ')

            if indexS == -1:
                answerCell, n = p.subn('',answerTmp)
                answerSet.add(answerCell)

            
            while answerTmp.find(' | ') != -1:
                indexS = answerTmp.index(' | ')
                answerCell = answerTmp[:indexS]
                answerCell, n = p.subn('',answerCell) 
                answerSet.add(answerCell)
                answerTmp = answerTmp[indexS+3:]
            faADict[keyi].append(answerSet)

    F1 = 0
    for i in range(len(ftList)):
        if ftList[i] == faDict[keyi][i]:
            F1 += 1

        else:
            intersectionLen = len(ftList[i] & faDict[keyi][i])
            lenCi = len(faDict[keyi][i])
            lenAi = len(ftList[i])
            if intersectionLen == 0:
                F1 += 0
            else:
                F1 += 2*intersectionLen*intersectionLen/(lenCi * lenAi)/(intersectionLen/lenCi+intersectionLen/lenAi)


    tripleResult[str(wi)] = F1/ len(ftList)    

    F1 = 0
    for i in range(len(ftAList)):
        if ftAList[i] == faADict[keyi][i]:
            F1 += 1

        else:
            intersectionLen = len(ftAList[i] & faADict[keyi][i])
            lenCi = len(faADict[keyi][i])
            lenAi = len(ftAList[i])
            if intersectionLen == 0:
                F1 += 0
            else:
                F1 += 2*intersectionLen*intersectionLen/(lenCi * lenAi)/(intersectionLen/lenCi+intersectionLen/lenAi)


    answerResult[str(wi)] = F1/ len(ftAList)         



for key in tripleResult:
    print('Triple F1 of w'+ str(key) +' :\t' + str(tripleResult[key]))

sortedTriple =sorted(tripleResult.items(), key=lambda d:d[1], reverse=True)
strBest = ''
for res in sortedTriple:
    if res[1] == sortedTriple[0][1]:
        strBest += res[0] + ', '

print(strBest.rstrip(', ')+' is the best predicate weight for triple!')

print('\n')

for key in answerResult:
    print('Answer F1 of w'+ str(key) +' :\t' + str(answerResult[key]))

sortedAnswer =sorted(answerResult.items(), key=lambda d:d[1], reverse=True)
strBest = ''
for res in sortedAnswer:
    if res[1] == sortedAnswer[0][1]:
        strBest += res[0] + ', '

print(strBest.rstrip(', ')+' is the best predicate weight for answer!')



print('\nPress Enter to exit!\n')
input()
