#!/bin/env python -tt

def sort_list(num_list, param):
    if param == "asc":
        print(sorted(num_list, reverse=False))
    elif param == "desc":
        print(sorted(num_list, reverse=True))
    else:
        print(num_list)        


num_list = []
if __name__ == "__main__":
    numbers = input("Enter a string of numbers seperated by space's: ")
    param = input("Enter how to order the list, Ascending (asc), Descending (desc), or none: ")   
    for num in numbers:
        num_list.append(num)
    while(" " in num_list):
        num_list.remove(" ")
    sort_list(num_list, param)
