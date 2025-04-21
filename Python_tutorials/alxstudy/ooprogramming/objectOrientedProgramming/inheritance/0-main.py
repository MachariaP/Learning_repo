#!/usr/bin/env python3

# base class
class Vehicle():
    def description(self):
        print("I'm a Vehicle!")


# subclass
class Car(Vehicle):
    pass


# create an object from each class
v = Vehicle()
c = Car()

v.description()
# Prints I'm a Vehicle!
c.description()
# Prints I'm a Vehicle!
