#!/bin/env python -tt
#########################################################################
#
# This script was created to randomly generate a password, of any length.
#
# Created by: J.Lickey
# 20220302
#
#########################################################################
import random, os, sys, argparse, subprocess

def genpwd(length):
    alpha = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    num = ['1','2','3','4','5','6','7','8','9','0']
    spc = ['`','`','!','@','#','$','%','^','&','*','(',')','_','+','-','=','{','}','|','[',']','\\',';','\'',':','"',',','.','/','<','>','?']
    L = 0
    p = []
    passwd = []

    while L <= length:
        randnum = random.randrange(1, 5)
        if ( randnum == 1):
            p = str(random.choice(alpha)) 
        elif ( randnum == 2):
            p = str(random.choice(num))
        elif ( randnum == 3):
            p = str(random.choice(spc))
        else:
            p = str(random.choice(alpha)).lower()
            #p = p.lower()
        passwd.append(p)
        L = L + 1
    #for i in passwd:
    #    print(i, end="")
    return ''.join(passwd)

if __name__ == "__main__":
    try:
        passwd = ''
        parser = argparse.ArgumentParser()
        parser.add_argument("-n", "--number", help="Enter the length of password", type=int)
        args = parser.parse_args()
        length = int(sys.argv[2])
        print(genpwd(length))
    except Exception as Err:
        cmd = 'python ADgenpasswd.py -h'
        output = subprocess.getoutput(cmd)
        print(output)
