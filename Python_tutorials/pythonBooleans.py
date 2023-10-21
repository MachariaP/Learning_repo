# Python Booleans
# Booleans represents one of two values:  True  or  False
print(10 > 9)
print(10 == 9)
print(10 < 9)

# Running a condition in an if statement, Python returns True or False:
a = 200
b = 33

if b > a:
    print("b is greater than a")
else:
    print("b is not greater than a")

# Evaluate Values and Variables
# The bool() function allows you to evaluate any value, and give you True or False in return.
# Evaluate a string and a number
print(bool("Hello"))
print(bool(15))

# Evaluate two variables
x = "Hello"
y = 15

print(bool(x))
print(bool(y))
