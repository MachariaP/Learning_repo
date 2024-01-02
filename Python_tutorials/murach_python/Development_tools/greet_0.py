#!/usr/bin/python3

# Backslashes using raw string (r-string)

# greet_0.py

def greet(name="World"):
    r"""Print a greeting.

    Usage examples:
    >>> greet("Pythonista")
    /== Hello, Pythonista! ==\
    \== How have you been? ==/
    """
    print(f"/== Hello, {name}! ==\\")
    print("\\== How have you been? ==/")
