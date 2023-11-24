# dates.py

#To work with date, you need to import date module:

from datetime import date
date.today()
print(date.today())

# data type conversion
"""
To use the + operator two combine two data types i.e
(a string and a date),
convert date to string using the function str() 
"""

print("Today's date is: " + str(date.today()))