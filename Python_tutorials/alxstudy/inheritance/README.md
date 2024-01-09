# Python - Inheritance

### Why Python programming is awesome
Python is considered awesome for several reasons:
- **Readability:** Python has a clear and readable syntax, making it easy to write and understand code.
- **Versatility:** Python is a versatile language used in various domains such as web development, data science, machine learning, artificial intelligence, scripting, and more.
- **Community and Documentation:** Python has a large and active community, contributing to a wealth of libraries and frameworks. Additionally, there's extensive documentation available.
- **Ease of Learning:** Python's syntax is simple and easy to learn, making it an excellent choice for beginners.

### What is a superclass, base class, or parent class
In object-oriented programming (OOP), a superclass, base class, or parent class is a class that is extended or inherited by one or more other classes called subclasses or derived classes. The superclass provides common attributes and methods that the subclasses share.

Example:
```python
class Animal:
    def speak(self):
        print("Animal speaks")

class Dog(Animal):
    def bark(self):
        print("Dog barks")

# Here, Animal is the superclass, and Dog is the subclass inheriting from Animal.
```

### What is a subclass
A subclass, also known as a derived class, is a class that inherits attributes and methods from a superclass or base class. It can also have its own additional attributes and methods.

Example:
```python
class Vehicle:
    def start_engine(self):
        print("Engine started")

class Car(Vehicle):
    def drive(self):
        print("Car is moving")

# Car is a subclass of Vehicle.
```

### How to list all attributes and methods of a class or instance
You can use the `dir()` function to list all attributes and methods of a class or instance.

Example:
```python
class MyClass:
    x = 10
    def my_method(self):
        pass

obj = MyClass()

# List all attributes and methods of the class
print(dir(MyClass))

# List all attributes and methods of the instance
print(dir(obj))
```

### When can an instance have new attributes
An instance can have new attributes at any time, either during the initialization (in the `__init__` method) or later in the program.

Example:
```python
class MyClass:
    def __init__(self, initial_value):
        self.value = initial_value

obj = MyClass(42)
print(obj.value)  # Output: 42

# Adding a new attribute later
obj.new_attribute = "Hello"
print(obj.new_attribute)  # Output: Hello
```

### How to inherit class from another
Inheritance in Python is achieved by placing the name of the superclass in parentheses after the class name of the subclass.

Example:
```python
class Animal:
    def speak(self):
        print("Animal speaks")

class Dog(Animal):
    def bark(self):
        print("Dog barks")
```

### How to define a class with multiple base classes
A class can inherit from multiple base classes by separating them with commas.

Example:
```python
class A:
    pass

class B:
    pass

class C(A, B):
    pass
```

### What is the default class every class inherits from
In Python, the default class every class inherits from is the `object` class.

Example:
```python
class MyClass:
    pass

# Equivalent to:
# class MyClass(object):
#     pass
```

### How to override a method or attribute inherited from the base class
Method or attribute overriding is done by redefining the method or attribute in the subclass.

Example:
```python
class Animal:
    def speak(self):
        print("Animal speaks")

class Dog(Animal):
    def speak(self):  # Method overridden
        print("Dog barks")
```

### Which attributes or methods are available by heritage to subclasses
Subclasses inherit all attributes and methods from their superclass, including public and protected ones. Private attributes or methods (those starting with double underscores) are not directly inherited.

### What is the purpose of inheritance
The purpose of inheritance in OOP is to promote code reusability and structure. It allows the creation of a general class (superclass) with common attributes and methods, and more specialized classes (subclasses) can inherit and extend the functionality of the superclass.

### What are, when and how to use isinstance, issubclass, type, and super built-in functions
- **isinstance(object, class):** Checks if an object is an instance of a class or a tuple of classes.
  ```python
  obj = Dog()
  print(isinstance(obj, Animal))  # True
  ```

- **issubclass(class, classinfo):** Checks if a class is a subclass of another class or a tuple of classes.
  ```python
  print(issubclass(Dog, Animal))  # True
  ```

- **type(object):** Returns the type of an object. It can also be used to check the type.
  ```python
  obj = Animal()
  print(type(obj))  # <class '__main__.Animal'>
  ```

- **super():** Returns a temporary object of the superclass, allowing you to call its methods.
  ```python
  class Dog(Animal):
      def speak(self):
          super().speak()
          print("Dog barks")
  ```

These functions are useful for checking types and relationships between classes in a program.
