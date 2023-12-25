#!/usr/bin/python3

# adding whitespace to strings with Tabs or Newlines

'''
    white space refers to any nonprinting characters ie space,
    tabs and end-of-line symbols.
    \t - for adding a tab to a text
    \n - for adding a new line to a string

'''
# adding a tab \t
print("Python")
print("\tPython")

# adding a newline \n
print("Languages:\nPython\nC\nJavascript")

# combining newline and tab together \n\t
print("Languages:\n\tPython\n\tC\n\tJavascript")

# Stripping Whitespace

'''
    Python can detect whitespace on the right or left side of a string.
    To ensure that no whitespace exsists at the right end
    of a string, use the rstrip() method

'''
print()
language = 'Python '
print(language)
print()
print(language.rstrip())
print()
print(language)

'''
    In the previous example the .rstrip only removed the whitespace 
    temporarily
    To remove the whitespace permanently, associate the stripped value with
    the variable name

'''

print()
language = 'Python3 '
language = language.rstrip()
print(language)

'''
    You can also strip whitespace from the left side of a string
    using the lstrip() method.
    Also its possible to from both sides using strip()

'''

print()
language = ' Python '
print(language)
print(language.rstrip())
print(language.lstrip())
language = language.strip()
print(language)
