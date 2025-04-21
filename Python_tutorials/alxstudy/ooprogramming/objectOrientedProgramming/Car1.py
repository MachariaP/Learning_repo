#!/usr/bin/env python3

class Car:
    def __init__(self, speed, color):
        print("__init__ is being called")
        print(speed)
        print(color)

        self.speed = speed
        self.color = color


ford = Car(120, "Blue")
audi = Car(140, "White")
toyota = Car(90, "Black")

print(ford.speed)
print(ford.color)

print(audi.speed)
print(audi.color)

print(toyota.speed)
print(toyota.color)
