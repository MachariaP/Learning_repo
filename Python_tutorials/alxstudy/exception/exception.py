#!/usr/bin/python3

# code that can cause a ValueError exception
number = int(input("Enter an integer: "))
print("You entered a valid integer of " + str(number) + ".")
print("Thanks!")

"""
Two functions that can cause a ValueError exception
int(data) - can't convert data to an int value.
float(data) - can't convert data to a float value.
"""
