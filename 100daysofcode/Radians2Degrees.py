#!/bin/env python -tt
import math

def convert(number_2_convert):
    # Radian measure × (180°/π)
    pi = float(math.pi)
    degree = float(number_2_convert) * (180 / pi)
    print(f"Radian: " + str(number_2_convert) + "\nDegree: " + str(degree))

if __name__ == "__main__":
    number_2_convert = input("Enter a number to convert to degrees: ") 
    convert(number_2_convert)
