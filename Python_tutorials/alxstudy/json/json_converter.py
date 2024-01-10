"""JSON Converter

Converts a Python dictionary to a JSON string using the json module.

Attributes:
    x (dict): A Python dictionary to be converted.
    y (str): The resulting JSON string.

Example:
    To convert a Python dictionary to a JSON string:

    >>> x = {
    ...   "name": "John",
    ...   "age": 30,
    ...   "city": "New York"
    ... }
    >>> y = json.dumps(x)
    >>> print(y)
    '{"name": "John", "age": 30, "city": "New York"}'
"""
import json

# a Python object (dict):
x = {
  "name": "John",
  "age": 30,
  "city": "New York"
}

# convert into JSON:
y = json.dumps(x)

# the result is a JSON string:
print(y)
