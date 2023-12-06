#!/usr/bin/python3

# Define a function that multiplies a number by 2
def mult_by_2(num):
    return num * 2

# Assign the function to a variable
times_two = mult_by_2

# Call the function with an argument and print the result
print("4 * 2 =", times_two(4))

# Call the function with a different argument and print the result
print(times_two(7))

# Define a function that applies another function to a number
def do_math(func, num):
    return func(num)

# Call the do_math function with mult_by_2 and an argument, then print the result
print("8 * 2=", do_math(mult_by_2, 8))

# creating a dynamic function
# How to return a function from a function
def get_func_mult_by_num(num):
    # Define a nested function that multiplies a given value by the provided 'num'
    def mult_by(value):
        return num * value
    
    # Return the nested function as the result of get_func_mult_by_num
    return mult_by

# Call get_func_mult_by_num with an argument '5' and assign the result to 'generated_func'
generated_func = get_func_mult_by_num(5)

# Call the generated function with an argument '10' and print the result
print("5 * 10 =", generated_func(10))

# working with two functions combined
listofFuncs = [times_two, generated_func]

print("5 * 9=", listofFuncs[1](9))
