#!usr/bin/python3

"""
    Define a class named 'Person' with a method 'say_hi'.
    Create an instance(object) of the 'Person' class.
    Call the 'say_hi' method on the object 'p'.

"""
class Person:

    def say_hi(self):
        print('Hello, how are you?')

p = Person()
p.say_hi()

# The prevoius 2 lines can also be written as

# Person().say_hi()
