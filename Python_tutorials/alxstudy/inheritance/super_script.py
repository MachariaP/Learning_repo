#!/usr/bin/python3

"""
This script defines two classes: Animal and Cat. Cat is a subclass of Animal, inheriting its attributes and methods. The make_noise() method prints the sound the cat makes. When an instance of Cat is created with the name "Rachel", it makes the noise "Meow!" when make_noise() is called.
"""


class Animal():
    def __init__(self, name, sound="Grrr"):
        self.name = name
        self.sound = sound

    def make_noise(self):
        print("{} says, {}".format(self.name, self.sound))

class Cat(Animal):
    def __init__(self, name):
        super().__init__(name, "Meow!")

pet_cat = Cat("Rachel")
pet_cat.make_noise()
