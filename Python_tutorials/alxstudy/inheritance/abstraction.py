#!/usr/bin/python3

from abc import ABC, abstractmethod

class Animal(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def make_noise(self):
        pass

class Cat(Animal):
    def make_noise(self):
        print("{} says, Meow!".format(self.name))

class Dog(Animal):
    def make_noise(self):
        print("{} says, Woof!".format(self.name))

kitty = Cat("Maisy")
doggy = Dog("Amber")
kitty.make_noise()
doggy.make_noise()
