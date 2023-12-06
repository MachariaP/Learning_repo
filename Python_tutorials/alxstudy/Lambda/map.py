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

# Example with Lambda
"""
We will use a lambda function instead of explicitly defining `fahrenheit()`
Lamba function is like a quick, throwaway function for a specific task.
"""
C = [39.2, 36.5, 37.3, 38, 37.8] 
F = list(map(lambda x: (float(9)/5)*x + 32, C))

print(F)

# Working with Multiple LIsts
# The lambda function is applied to each set of elements at the same index in the list `a`, `b`, and `c`.

a = [1, 2, 3, 4]
b = [17, 12, 11, 10]
c = [-1, -4, 5, 9]

result = list(map(lambda x, y, z: x + y + z, a, b, c))
print(result)

