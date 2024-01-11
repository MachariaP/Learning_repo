#!/usr/bin/python3

def test_var_args(f_arg, *argv):
    """
    Print the first normal argument and any additional arguments passed.

    Parameters:
    - f_arg: The first normal argument.
    - *argv: Additional variable arguments collected into a tuple.

    Example:
    >>> test_var_args('yasoob', 'python', 'eggs', 'test')
    first normal arg: yasoob
    another arg through *argv : python
    another arg through *argv : eggs
    another arg through *argv : test
    """
    print("first normal arg:", f_arg)
    for arg in argv:
        print("another arg through *argv :", arg)

test_var_args('yasoob', 'python', 'eggs', 'test')
