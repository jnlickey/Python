import os, sys, random

alpha = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
num = ['1','2','3','4','5','6','7','8','9','0']
spc = ['`','~','!','@','#','$','%','^','&','*','(',')','_','+','-','=','[',']','}','{','\\','|',':',';','"','\'','<',',','>','.','?','/']

def passwdgen(alpha, num, spc, length):
    L = 1
    passwd = []
    while L <= length:
        randnum = random.randint(1, 5)
        if ( randnum == 1 ):
            p = str(random.choice(alpha))
        elif ( randnum == 2 ):
            p = str(random.choice(num))
        elif ( randnum == 3 ):
            p = str(random.choice(spc))
        else:
            p = str(random.choice(alpha))
            p = p.lower()
        passwd.append(p)
        L = L + 1
    for i in passwd:
        print (i, end='')

if __name__ == "__main__":
    length = int(input('Enter length of password (numbers only): '))
    passwdgen(alpha, num, spc, length)

