#!/usr/bin/env python3

from polygon import Polygon
from shape import Shape
from sides import Sides

class Triangle(Polygon, Shape, Sides):
    def area(self):
        return self.get_width() * self.get_height() / 2
