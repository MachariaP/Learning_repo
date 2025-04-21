#!/usr/bin/env python3

class Rectangle:
    def __init__(self, height, width):
        self.height = height
        self.width = width


rect1 = Rectangle(20, 30)
rect2 = Rectangle(30, 40)

print(rect1.height * rect1.width)
print(rect2.height * rect2.width)
