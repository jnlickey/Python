#!/bin/env python -tt
strSplit = []
strOriginal = input("Please enter sentence you wanted modified: ")
for line in strOriginal.split("."):
    strSplit.append(line)
for item in strSplit:
    after = item.capitalize()

    print(after)

