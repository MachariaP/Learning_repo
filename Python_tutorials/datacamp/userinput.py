#userinput.py
"""
To get information from the user, use the input() function
Example below:
"""

Greetings = "Welcome to the greeter program "
name = input("Enter your name: ")

print(Greetings  + name)

# Working with numbers
"""
The input function stores a result as a string
"""
print("calculator program")
first_number = input("first number: ")
second_number = input("second number: ")

print(first_number + second_number)

"""
first_number and second_number are strings.
To be able to perform calculations, convert strings into numbers using 
the int() function.
"""
print(int(first_number) + int(second_number))