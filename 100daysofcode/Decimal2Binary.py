#!/bin/env python -tt

def convert2binary(number):
    binary_number = bin(number).replace("0b", "")
    print(binary_number) 

if __name__ == "__main__":
    number = int(input("Enter number to convert to binary: "))
    convert2binary(number)
