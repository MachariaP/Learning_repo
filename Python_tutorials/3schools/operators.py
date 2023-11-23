# Python OPerators.
# Are used to perform operations on variables

# How python divides the operators:

# 1. Arithimetic
""" Used with numeric values to perform mathematical operations:"""
x = 12
y = 4
print(x + y)  # Addition ( + )          returns 16
print(x - y)  # Substruction ( - )      returns 8
print(x * y)  # Multiplication ( * )    returns 48
print(x / y)  # Division ( / )          returns 3.0
print(x % y)  # Modulus ( % )           returns 0
print(x**y)  # Exponentiation ( ** )    returns 20736
print(x // y)  # Floor division         returns 3

# 2. Assignment
"""Used to assign values to variables"""
x = 8  # x = 8
print(x)  # returns 8
x += 3  # x = x + 3
print(x)  # returns 11
x -= 3  # x = x - 3
print(x)  # returns 8
x *= 3  # x = x * 3
print(x)  # returns 24
x /= 3  # x = x/3
print(x)  # returns 8.0
x %= 3  # x = x % 3
print(x)  # returns 2.0
x //= 3  # x = x // 3
print(x)  # returns 0.0
x **= 3  # x = x ** 3
print(x)  # returns 0.0
x = 5
x &= 3  # x = x & 3
print(x)  # returns 1
x |= 3  # x = x | 3
print(x)  # returns 3
x ^= 3  # x = x ^ 3
print(x)  # returns 0
x >>= 3  # x = x >> 3
print(x)  #  returns 0
x <<= 3  # x = x << 3
print(x)  #  returns 0

# 3. Comparison
"""Used to compare two values"""
x = 12
y = 8
print(x == y)  # Equal "=="
print(x != y)  # Not equal  "!="
print(x > y)  # Greater than  ">"
print(x < y)  # Less than  "<"
print(x >= y)  # Greater than or equal to
print(x <= y)  # Less than or equal to

# 4. LOgical
"""Used to combine conditional statements"""
x = 5
print(x < 5 and x < 10)  # "and" Returns true if both statements are true
print(x < 5 or x < 4)  # "or"  REturns true if one of the statements is true
print(not (x < 5 and x < 10))  # "not" Reverse the results, False if the result is true

# 5. identity
"""used to compare the objects"""
"""Not if they are equal"""
"""but if they are actually the same object, with same memory location"""
x = ["Football", "Tennis"]
y = ["Football", "Tennis"]
z = x
print(x is z)  # returns True
print(x is y)  # returns False
print(x == y)  # return True

# 6. Membership
"""Used to test if a sequence is presented in an object"""
x = ["apple", "banana"]
print("banana" in x)

# 7. Bitwise
