#!/usr/bin/env python3

from triangle import Triangle
from rectangle import Rectangle

rect = Rectangle()
tria = Triangle()

rect.set_values(30, 60)
tria.set_values(30, 60)

rect.set_color("Blue")
tria.set_color("Red")

rect.set_edges(4)
tria.set_edges(3)

print(rect.area())
print(tria.area())

print(rect.get_color())
print(tria.get_color())

print(rect.get_edges())
print(tria.get_edges())
