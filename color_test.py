#!/bin/env python -tt

i = 0
color_lst = []
for i in range(0,101):
    for b in range(0,101):
        color_lst.append(f"\033[{i};{b}m color \\033[{i};{b}m \033[0;0m")
for i,entry in enumerate(color_lst):
    print("{}".format(entry), sep='', end="")
    if i%6 == 0:
        print("\n") 
