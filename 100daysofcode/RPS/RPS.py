#!/bin/env python -tt

import random

# Rock Paper Scissors ASCII Art

def Rock():
    # Rock
    print("""
        _______
    ---'   ____)
          (_____)
          (_____)
          (____)
    ---.__(___)
    """)
    print("ROCK\n")

def Paper():
    # Paper
    print("""
         _______
    ---'    ____)____
               ______)
              _______)
             _______)
    ---.__________)
    """)
    print("PAPER\n")

def Scissors():
    # Scissors
    print("""
        _______
    ---'   ____)____
              ______)
              _______)
          (____)
    ---.__(___)
    """)
    print("SCISSORS\n")
    

def start():
    print("Welcome to Rock, Paper, Scissors!")
    user_choice = input("Which do you choose, Rock (R|r), Paper (P|p). or Scissors (S|s): ")
    uchoice = 0
    cchoice = 0
    print("You chose:")
    if user_choice == "R" or user_choice == "r":
        Rock()
        uchoice = "r"
    elif user_choice == "P" or user_choice == "p":
        Paper()
        uchoice = "p"
    elif user_choice == "S" or user_choice == "s":
        Scissors()
        uchoice = "s"

    auto_choice = random.randint(1,3)
    print("Computer chose:")
    if auto_choice == 1:
        Rock()
        cchoice = "r"
    elif auto_choice == 2:
        Paper()
        cchoice = "p"
    elif auto_choice == 3:
        Scissors()
        cchoice = "s"

    if cchoice == "r" and uchoice == "s" or cchoice == "s" and uchoice == "p" or cchoice == "p" and uchoice == "r":
        print("You lose.")
    elif cchoice == uchoice:
        print("It's a draw.")
    else:
        print("You WIN!")

    ans = input("Do you want to play again (Y|N): ")
    if ans == "Y" or ans == "y" or ans == "YES" or ans == "Yes" or ans == "yes":
        start()
    else:
        exit()
    
start()
