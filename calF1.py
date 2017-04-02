import sys
import os
import codecs
import re



ft = open('nlpcc-iccpol-2016.kbqa.testing-data','r',encoding='utf8')

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

faList = []

faAList = []

while True:
    print('Please input result file name:')
    path = input()
    if path == 'exit()':
            exit()
    if os.path.exists(path) != True:
        print('File not exist! Input again or use \'exit()\' to exit')
        continue
        
    fa = open(path,'r',encoding='utf8')

    faList = []

    faAList = []

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
                faList.append(tripleTmp)
                continue
            assert(' === ' not in line)
            lineTmp = line.replace(' ||| ', ' === ', 1)
            lineTmp = lineTmp[:lineTmp.index(' |||')+4].replace(' === ',' ||| ',1)
            lineTmp, n = p.subn('',lineTmp)
            tripleTmp.add(lineTmp.lower())
            faList.append(tripleTmp)

        if line[1] == 'a':
            answerTmp = line[line.index('\t')+1:].strip('\n').lower()
            answerSet = set()
            if answerTmp.find(' ||| ') != -1:
                faAList.append(answerSet)
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
            faAList.append(answerSet)

    F1 = 0
    for i in range(len(ftList)):
        if ftList[i] == faList[i]:
            F1 += 1

        else:
            intersectionLen = len(ftList[i] & faList[i])
            lenCi = len(faList[i])
            lenAi = len(ftList[i])
            if intersectionLen == 0:
                F1 += 0
            else:
                F1 += 2*intersectionLen*intersectionLen/(lenCi * lenAi)/(intersectionLen/lenCi+intersectionLen/lenAi)

            
    print('Triple F1:\t' + str(F1/ len(ftAList)))

    F1 = 0
    for i in range(len(ftAList)):
        if ftAList[i] == faAList[i]:
            F1 += 1

        else:
            intersectionLen = len(ftAList[i] & faAList[i])
            lenCi = len(faAList[i])
            lenAi = len(ftAList[i])
            if intersectionLen == 0:
                F1 += 0
            else:
                F1 += 2*intersectionLen*intersectionLen/(lenCi * lenAi)/(intersectionLen/lenCi+intersectionLen/lenAi)

            
    print('Answer F1:\t' + str(F1/ len(ftAList)))


                



