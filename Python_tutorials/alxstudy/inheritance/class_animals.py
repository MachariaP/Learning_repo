#!/usr/bin/python3

class Animal():
    def eat(self):
        print("Nom Nom Nom....eating food!")

class Dog(Animal):
    def bark(self):
        print('Bark!')

class Cat(Animal):
    def meow(self):
        print('Meow!')

fluffy = Dog()
zoomie = Cat()

fluffy.eat()
zoomie.eat()
