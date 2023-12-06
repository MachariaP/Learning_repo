#!/usr/bin/python3

# What is `map()`?
"""
`map()` - is a function in python that takes two arguments:
(i) a function (`func`) and 
(ii) a sequence (like a list).
"""
# How `map()` works?
"""
- `map(func, seq)` applies the function `func` to each element in the sequence `seq`.
- it returns an iterator.
"""
# Example without Lambda 
def fahrenheit(T):
    return ((float(9)/5)*T + 32)

def celsius(T):
    return (float(5)/9)*(T-32)

temperatures = (36.5, 37, 37.5, 38, 39)
F = map(fahrenheit, temperatures)
C = map(celsius, F)

# Convert iterators to lists for printing
temperatures_in_Fahrenheit = list(F)
temperatures_in_Celsius = list(C)

print(temperatures_in_Fahrenheit)
print(temperatures_in_Celsius)

