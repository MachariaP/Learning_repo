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

# Most Values are True
# Almost any value is evaluated to True if it has some sort of content.

# Any string is True, except empty strings.

# Any number is True, except 0.

# Any list, tuple, set, and dictionary are True, except empty ones.

# The following will return False:
bool(False)
bool(None)
bool(0)
bool("")
bool(())
bool([])
bool({})
# If you have an object that is made from a class with a __len__ function that returns 0 or False, it evaluates to False:


class myclass:
    def _len_(self):
        return 0


myobj = myclass()
print(bool(myobj))

# isinstance()
# is a python builtin function that returns a boolen value
# can be used to determine if any object is of certain data type
x = 200
print(isinstance(x, int))
