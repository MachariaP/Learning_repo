"""
Demonstrating the use of the = specifier in f-strings.

The = specifier is used to expand an expression to the text of the expression, 
an equal sign, and then the representation of the evaluated expression.

- bugs: Represents the type of bugs, initialized to 'roaches'.
- count: Represents the count of bugs, initialized to 13.
- area: Represents the area where bugs are found, initialized to 'living room'.

Prints a debug statement using f-string with the = specifier to display the 
variables along with their values in a formatted manner.
"""

bugs = 'roaches'
count = 13
area = 'living room'
print(f'Debugging {bugs=} {count=} {area=}')
