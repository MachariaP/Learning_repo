#!/usr/bin/python3
# Define Your Own Types
class Coordinate(object):

    # define attributes here
    def __init__ (self, x, y):
        self.x = x
        self.y = y

    c = Coordinate (3, 4)
    origin = Coordinate (0, 0)
    print(c.x)
    print(origin.x)
