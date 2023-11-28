#!usr/bin/python3

# Using a copy or creating a new list (recommended)
numbers = [1, 2, 3, 4, 5]
new_numbers = [num for num in numbers if num % 2 != 0]

# print(new_numbers)  # This will give the expected result without modifying the original list

# create a sample collection
users = {'Hans': 'active','Eleonore':'inacrive', 'James': 'active'}

# strategy: Iterate over a copy
for user, status in users.copy().items():
    if status == 'inactive':
        del users[user]

# strategy: create a new collection
active_users = {}
for user, status in users.items():
    if status == 'active':
        active_users[user] = status

print(new_numbers)
print(active_users)