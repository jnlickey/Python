#!/bin/env python -tt

def fib(how_many):
    a = 0
    b = 1
    if how_many == 1:
        print(a)
    else:
        print(a)
        print(b)
    for number in range(2,how_many):
        c = a + b
        a = b
        b = c
        print(c)

if __name__ == "__main__":
    how_many = int(input("How many Fibonnaci numbers do you want to generate: "))
    fib(how_many) 
