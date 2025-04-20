#!/usr/bin/evn python3
"""
Procedure-Oriented Programming
Imagine you are baking a cake.
In a procedure-oriented approach, you would write a step-by-step recipe
"""


def mix_ingredients(flour, sugar, eggs):
    return f"Mixed {flour}, {sugar}, and {eggs}"


def bake_cake(mixture):
    return "Baked cake"


def frost_cake(cake):
    return "Frosted cake"


# Using the functions
mixture = mix_ingredients("2 cups of flour", "1 cup sugar", "2 eggs")
cake = bake_cake(mixture)
final_cake = frost_cake(cake)
print(final_cake)
