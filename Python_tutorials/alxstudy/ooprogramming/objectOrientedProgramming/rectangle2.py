#!/usr/bin/env python3

class Rectangle:
    def __init__(self, height, width):
        self.__height = height
        self.__width = width

    def set_height(self, value):
        self.__height = value

    def get_height(self):
        return self.__height

    def set_width(self, value):
        self.__width = value

    def get_width(self):
        return self.__width

    def area(self):
        return (self.__height * self.__width)

rect1 = Rectangle(10, 20)
rect2 = Rectangle(20, 30)
rect3 = Rectangle(30, 40)
rect4 = Rectangle(40, 50)

print(rect1.area())
print(rect2.area())
print(rect3.area())
print(rect4.area())
