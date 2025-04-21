#!/usr/bin/env python3

class Rectangle:
    pass

rect1 = Rectangle()
rect2 = Rectangle()

rect1.height = 20
rect2.height = 30

rect1.width = 30
rect2.width = 40

print(rect1.height * rect1.width)
print(rect2.height * rect2.width)
