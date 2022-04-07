#!/bin/env python -tt
try:
    #print(1/0)
    #print(1 + "something")
    print('Hello World')
except ZeroDivisionError as z:
    print(z)
except TypeError as t:
    print(t)
else:
    print("Completed Successfully")
