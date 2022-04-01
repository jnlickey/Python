#!/bin/env python -tt

row1=["☐'","☐'","☐'"]
row2=["☐'","☐'","☐'"]
row3=["☐'","☐'","☐'"]

number = input("Enter a number to place an X: ")
map=[row1,row2,row3]
print("",row1,"\n",row2,"\n",row3)
# Enter your code below this line

horizontal = int(number[0]) 
vertical = int(number[1])
map[horizontal - 1][vertical - 1] = "X"

# Enter your code above this line
print()
print("",row1,"\n",row2,"\n",row3)
