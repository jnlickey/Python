#!/usr/bin/env python -tt
#######################################
# Random key generator
# Created by: J.N.Lickey
# 20160229
#######################################
import re, random, datetime, os

def randomnum():
    # Generates a random string of numbers based off of the
    # date and time that the script is being ran.
    now = str(datetime.datetime.now())
    now = int(re.sub('[\W]',"", now))
    num = random.SystemRandom()
    num = num.randint(0,now)
    return num

def randomlet():
    # Grab a random letter from the string of letters listed
    let = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    randomlet = random.choice(let)
    return randomlet
    
def main():
    # Generates the completed key and associated random letters
    key = str(randomnum())
    length = str(len(key))
    #print (key)
    #print (length)
    keylst = {}
    for number in length:
        keylst[0] = key[:4]
        keylst[1] = key[4:8]
        keylst[2] = key[8:12]
        keylst[3] = key[12:16]
        keylst[4] = key[16:]

    number = 0    
    print (keylst[number] + randomlet() + "-" + keylst[(number+1)] + randomlet() + "-" + keylst[(number+2)] + randomlet() + "-" + keylst[(number+3)] + randomlet() + "-" + keylst[(number+4)] + randomlet())

main()

