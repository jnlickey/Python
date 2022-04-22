#!/bin/env python -tt

def count_vowels(string):
    a_count = 0
    e_count = 0
    i_count = 0
    o_count = 0
    u_count = 0

    string2chk = string.lower()

    for letter in string2chk:
        if letter == 'a':
            a_count += 1
        elif letter == 'e':
            e_count +=1
        elif letter == 'i':
            i_count +=1
        elif letter == 'o':
            o_count +=1
        elif letter == 'u':
            u_count +=1
    print(f"Number of A's: {a_count}")
    print(f"Number of E's: {e_count}")
    print(f"Number of I's: {i_count}")
    print(f"Number of O's: {o_count}")
    print(f"Number of U's: {u_count}")
    total_vowels = int(a_count) + int(e_count) + int(i_count) + int(o_count) + int(u_count)
    print(f"Total Number of vowels: {total_vowels}")

if __name__ == "__main__":
    string = str(input("Enter a string of characters to count the vowels: "))
    count_vowels(string)
