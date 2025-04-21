#!/usr/bin/env python3

from triangle import Triangle
from rectangle import Rectangle

rect = Rectangle()
tria = Triangle()

rect.set_values(30, 60)
tria.set_values(30, 60)

print(rect.area())
print(tria.area())
