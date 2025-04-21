#!/usr/bin/env python3

class Car:
    def __init__(self, speed, color):
        self.__speed = speed
        self.__color = color

    def set_speed(self, value):
        self.__speed = value

    def get_speed(self):
        return self.__speed

    def set_color(self, value):
        self.__color = value

    def get_color(self):
        return self.__color

# Objects (Instances of a class)
toyota = Car(80, "black")
honda = Car(100, "white")
audi = Car(120, "blue")

print(toyota.get_color())
print(audi.get_speed())
print(audi.get_speed(), audi.get_color())
