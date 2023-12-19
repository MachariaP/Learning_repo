#!/usr/bin/python3

class Person:
    """
    A simple class representing a person.

    Attributes:
    - name (str): The name of the person.

    Methods:
    - __init__(self, name): Constructor method to initialize the person's name.
    - say_hi(self): Method to print a greeting message.
    """

    def __init__(self, name):
        """
        Constructor method to initialize the person's name.

        Parameters:
        - name (str): The name of the person.
        """
        self.name = name

    def say_hi(self):
        """
        Method to print a greeting message.
        """
        print('Hello, my name is', self.name)

# Creating an instance of the Person class
p = Person('Swaroop')

# Calling the say_hi method on the instance
p.say_hi()

# The previous 2 lines can also be written as
# Person('Swaroop').say_hi()
