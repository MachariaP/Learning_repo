#!/usr/bin/python3
# How to use a try statement to handle one type of exception

"""
try:
    statements
except [ExceptionName]:
    statements
"""
try:
    number = int(input("Enter an integer: "))
    print("You entered a valid integer of " + str(number) + ".")
except ValueError:
    print("You entered an invalid integer. Please try again.")
print("THanks!")
