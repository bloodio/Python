def swap_case(s):
    strLen = len(s)
    i = 0
    newStr=''
    for i in range (0, strLen):
        if (s[i].isupper()==True):
            newStr = newStr + s[i].lower()
        else:
            newStr = newStr + s[i].capitalize()
    return newStr

if __name__ == '__main__':
    s = input()
    result = swap_case(s)
    print(result)