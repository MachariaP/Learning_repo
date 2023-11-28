#!/usr/bin/python3

# Measure the length of some words:
words = ['cat', 'window', 'defenestrate']

# The 'for' loop goes through each word in the 'words' list
# 'w' is a variable that takes on the value of each word in the list, one by one
for w in words:
    # Inside the loop, we do something with each word.
    # In this case, we print the word and its length.
    print(w, len(w))
