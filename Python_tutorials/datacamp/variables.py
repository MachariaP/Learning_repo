#variable.py

# Calculations with variables
savings = 100

# Create the variables monthly_savings and num_months
monthly_savings = 10
num_months = 4


# Multiply monthly_savings and num_months
new_savings = monthly_savings * num_months

# Add new_savings to your savings
total_savings = new_savings + savings

# Print total_savings
print(total_savings)

#other variables 

# Create a variable half
half = 0.5

# Create a variable intro
intro = "Hello! How are you?"

# Create a variable is_good
is_good = True

# operations with other types

"""
Calculate the product of monthly_savings and num_months. Store the result in year_savings.
What do you think the resulting type will be? Find out by printing out the type of year_savings.
Calculate the sum of intro and intro and store the result in a new variable doubleintro.
Print out doubleintro
"""
monthly_savings = 10
num_months = 12
intro = "Hello! How are you?"

# Calculate year_savings using monthly_savings and num_months
year_savings = monthly_savings * num_months

# Print the type of year_savings
print(type(year_savings))

# Assign sum of intro and intro to doubleintro
doubleintro = intro + intro

# Print out doubleintro
print(doubleintro)


# Type Conversion
"""
Hit Run Code to run the code. Try to understand the error message.
Fix the code such that the printout runs without errors; use the function str() to convert the variables savings and total_savings to strings.
Convert the variable pi_string to a float and store this float as a new variable, pi_float.
"""

# Definition of savings and total_savings
savings = 100
total_savings = 150

# Fix the printout
print("I started with $" + str(savings) + " and now have $" + str(total_savings) + ". Awesome!")

# Definition of pi_string
pi_string = "3.1415926"

# Convert pi_string into float: pi_float
pi_float = float(pi_string)

print(pi_float)