#!/bin/python3

import os
import sys

def simpleArraySum(ar):
    a = len(ar)
    sum=0
    for i in range (0, a):
        sum=sum+ar(i)
    return sum
        
if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')
    ar_count = int(input())
    ar = list(map(int, input().rstrip().split()))
    result = simpleArraySum(ar)
    fptr.write(str(result) + '\n')
    fptr.close()
