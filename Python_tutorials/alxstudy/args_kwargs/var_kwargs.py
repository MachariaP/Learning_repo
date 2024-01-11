#!/usr/bin/python3

def greet_me(**kwargs):
    """
    Print key-value pairs from keyword arguments.

    Parameters:
    - **kwargs: Variable keyword arguments.

    Example:
    >>> greet_me(name="yasoob")
    name == yasoob
    """
    if kwargs is not None:
        for key, value in kwargs.items():
            print("%s == %s" % (key, value))

greet_me(name="yasoob")
