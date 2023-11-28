#!usr/bin/python3

# Using a copy or creating a new list (recommended)
numbers = [1, 2, 3, 4, 5]
new_numbers = [num for num in numbers if num % 2 != 0]

print(new_numbers)  # This will give the expected result without modifying the original list
