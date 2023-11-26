#commandlinearg.py

"""
Buy using the sys module, you can retrive the command-line argument
and use them in your program.

sys.argv - is an array or a dT structure that contains many items.
"""
import sys

print(sys.argv)
print(sys.argv[0])   # program name
print(sys.argv[1])   # first arg
print(sys.argv[2])   # second arg
#run [python3 commandlinearg.py 2023-26-11 Sunday] to see results
