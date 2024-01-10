#!/usr/bin/python3
"""Module to convert JSON to Python"""


import json

def parse_json_string(json_string):
    """
    Parse a JSON string and return the resulting Python dictionary.

    Args:
        json_string (str): A valid JSON-formatted string.

    Returns:
        dict: A Python dictionary representing the parsed JSON data.
    """
    parsed_data = json.loads(json_string)
    return parsed_data

# some JSON string
json_data = '{ "name":"John", "age":30, "city":"Kenya"}'

# parse the JSON string
resulting_dict = parse_json_string(json_data)

# Accessing and printing a specific value from the dictionary
print(resulting_dict["age"])
