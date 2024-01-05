#!/usr/bin/python3
# Lists
"""
List:
    An ordered set of values.
    Each value is identified by an index.

Elements:
    Values that make up a list.
    They can have any type.
"""
# Creating a new list using square brackets [ ]
list1 = [10, 20, 30, 40]
list2 = ["spam", "bungee", "swallow"]

# A list doesn't have to be the same type and can be nested
list3 = ["Hello", 2.0, 5, [10, 20]]

# An empty list is false in a boolean expression
if []:
    print('This is true.')
else:
    print('This is false.')
