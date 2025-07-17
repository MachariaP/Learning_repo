#!/usr/bin/env python3

class Car:
    def __init__(self, make="", model="", year=0, color=""):
        self.__make = make
        self.__model = model
        self.__year = year
        self.__color = color

    @property
    def make(self):
        return self.__make

    @make.setter
    def make(self, value):
        if not isinstance(value, str):
            raise TypeError("Make must be a string")
        self.__make = value


    @property
    def model(self):
        return self.__Model


    @property
    def year(self):
        return self.__year


    @property
    def color(self):
        return self.__color
