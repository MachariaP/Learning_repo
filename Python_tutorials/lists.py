# PYTHON LISTS
# List

mylist = ["apple", "banana", "cherry"]

"""Lists are used to store multiple items in a single variable"""

thislist = ["apple", "banana", "cherry"]
print(thislist)
print(mylist)

# List Items
"""List items are: (i)ordered
                   (ii)changeable
                   (iii)allow duplicate values
The first item has index [0], the second has index [1], the third has index [2] etc."""

# Ordered
# - Have a defined order
# - The order will not change
# - Whenever new items are added to the list, new items are placed at the end of the list.

# Changeable
# - meaning we can change, add, remove items from an existing list.

# Allow Duplicates
#   - list can have items with the same value

"""Example"""
# Lists allow duplicate values:

thislist = ["apple", "banana", "cherry", "apple", "cherry"]
print(thislist)

"""List Length"""
# use the len() function:
# print the number of items in the list:
thislist = ["apple", "banana", "cherry"]
print(len(thislist))
