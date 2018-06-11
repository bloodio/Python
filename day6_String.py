def wordOdd(inputString):
    i = 0
    k = len(inputString)
    strOdd = ""
    for i in range (0, k, 2):
        strOdd = strOdd + inputString[i] 
    return strOdd

def wordEven(inputString):
    j = 1
    k = len(inputString)
    strEven = ""
    for j in range (1, k, 2):
        strEven = strEven + inputString[j]
    return strEven

t = int(input())
n = 0
for n in range (0, t):
    inputString = str(input())
    print(wordOdd(inputString) +' '+ wordEven(inputString))