#!/usr/bin/python3

# Regular strings that escape the backslash by doubling it

# greet_1.py

def greet(name="World"):
    """Print a greeting.

    Usage examples:
    >>> greet("Pythonista")
    /== Hello, Pythonista! ==\\
    \\== How have you been? ==/
    """
    print(f"/== Hello, {name}! ==\\")
    print("\\== How have you been? ==/")
