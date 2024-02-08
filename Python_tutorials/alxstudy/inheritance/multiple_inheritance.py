#!/usr/bin/python3 

"""
This script defines a hierarchy of classes representing animals. Dog and Wolf are subclasses of Animal, while Hybrid inherits from both Dog and Wolf. Each class has an action method that performs a specific action for the respective type of animal. When an instance of Hybrid is created and its action method is called, it first calls the action method of Dog (its first parent class) using super(), and then calls the action method of Wolf.
"""

class Animal():
    def __init__(self, name):
        self.name = name

class Dog(Animal):
    def action(self):
        print("{} wags tail. Awwww".format(self.name))

class Wolf(Animal):
    def action(self):
        print("{} bites. OUCH!".format(self.name))

class Hybrid(Dog, Wolf):
    def action(self):
        super().action()
        Wolf.action(self)

my_pet = Hybrid("Fluffy")
my_pet.action() 
