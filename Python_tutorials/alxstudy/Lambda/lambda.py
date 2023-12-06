#!/usr/bin/python3

""" 
Lambda - a small anonymous function
- can take any number of arguments, but can only have one expression.

"""
"""
Syntax :
lambda arguments : expression

"""

# Example 1
# Add 20 to argument a, and return the result :

x = lambda a : a + 20
print(x(5))
# Expected output : 25

# Example 2
# Lambda functions can take any number of arguments
# Multiply argument a with argument b and return the result:

x = lambda a, b : a * b
print(x(5, 6))
# Expected output : 30

# Example 3
# Summarize argument a, b, and c and return the result:

x = lambda a, b, c : a + b + c
print(x(5, 6, 2))
# Expected output : 13

