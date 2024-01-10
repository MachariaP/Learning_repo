# JSON Concepts in Python

Welcome to the world of JSON (JavaScript Object Notation) in Python! JSON is a lightweight data interchange format that is easy for humans to read and write and easy for machines to parse and generate. In Python, the `json` module provides functionality to work with JSON data seamlessly.

## Table of Contents

1. [Introduction to JSON](#introduction-to-json)
2. [JSON Basics in Python](#json-basics-in-python)
3. [Working with JSON Data](#working-with-json-data)
4. [Serializing Python Objects to JSON](#serializing-python-objects-to-json)
5. [Deserializing JSON to Python Objects](#deserializing-json-to-python-objects)
6. [JSON File Operations](#json-file-operations)

## Introduction to JSON

JSON is a text format that is completely language-independent but uses conventions that are familiar to programmers of the C family of languages, including C, C++, C#, Java, JavaScript, Perl, Python, and many others.

## JSON Basics in Python

### 1. JSON Syntax

JSON data is represented as key-value pairs, similar to Python dictionaries.

Example:
```json
{
  "name": "John",
  "age": 30,
  "city": "New York"
}
```

### 2. JSON Data Types

- **Number**: Integer or floating-point.
- **String**: A sequence of characters.
- **Boolean**: `true` or `false`.
- **Array**: An ordered list of values.
- **Object**: An unordered collection of key-value pairs.
- **Null**: Represents an empty value.

## Working with JSON Data

### 3. Encoding and Decoding

- **`json.dumps()`**: Serialize Python objects to a JSON formatted string.
  ```python
  import json

  data = {"name": "John", "age": 30, "city": "New York"}
  json_string = json.dumps(data)
  ```

- **`json.loads()`**: Deserialize a JSON string to a Python object.
  ```python
  json_string = '{"name": "John", "age": 30, "city": "New York"}'
  python_object = json.loads(json_string)
  ```

## Serializing Python Objects to JSON

### 4. Serializing Simple Data Types

```python
import json

# Python object
data = {"name": "John", "age": 30, "city": "New York"}

# Serialize to JSON
json_string = json.dumps(data)
print(json_string)
```

### 5. Serializing Custom Objects

```python
import json

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

# Custom object
person = Person("John", 30)

# Serialize to JSON using a custom function
def convert_to_dict(obj):
    return obj.__dict__

json_string = json.dumps(person, default=convert_to_dict)
print(json_string)
```

## Deserializing JSON to Python Objects

### 6. Deserializing Simple Data Types

```python
import json

# JSON string
json_string = '{"name": "John", "age": 30, "city": "New York"}'

# Deserialize to Python object
data = json.loads(json_string)
print(data)
```

### 7. Deserializing Custom Objects

```python
import json

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

# JSON string
json_string = '{"name": "John", "age": 30}'

# Deserialize to a custom object
def convert_to_object(d):
    return Person(d['name'], d['age'])

person_object = json.loads(json_string, object_hook=convert_to_object)
print(person_object.name, person_object.age)
```

## JSON File Operations

### 8. Reading and Writing JSON Files

```python
import json

# Writing to a JSON file
data = {"name": "John", "age": 30, "city": "New York"}
with open('data.json', 'w') as json_file:
    json.dump(data, json_file)

# Reading from a JSON file
with open('data.json', 'r') as json_file:
    loaded_data = json.load(json_file)
    print(loaded_data)
```

Feel free to explore more advanced features of the `json` module to enhance your JSON handling skills in Python!
