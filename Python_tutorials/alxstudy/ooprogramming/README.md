#  Python - More Classes and Objects


### 1. Why Python programming is awesome:

Python's simplicity and readability make it an excellent language for both beginners and experienced developers. Its extensive standard library, active community, and support for multiple programming paradigms contribute to its awesomeness.

### 2. What is OOP (Object-Oriented Programming):

Object-Oriented Programming is a programming paradigm that uses objects, which encapsulate data and behavior. Key principles include:
- **Encapsulation:** Bundling data and methods that operate on the data.
- **Inheritance:** Creating new classes based on existing ones.
- **Polymorphism:** The ability of a function to take different forms.

### 3. "First-class everything":

In Python, everything is an object, and objects can be assigned to variables, passed as arguments, and returned from functions. This includes functions, which are first-class citizens.

Example:
```python
def greet(name):
    return f"Hello, {name}!"

greeting_function = greet
print(greeting_function("John"))
```

### 4. What is a class:

A class is a blueprint for creating objects. It defines attributes (data) and methods (functions) that will be common to all instances of objects created from that class.

Example:
```python
class Dog:
    def __init__(self, name):
        self.name = name

    def bark(self):
        return f"{self.name} says Woof!"

my_dog = Dog("Buddy")
print(my_dog.bark())
```

### 5. What is an object and an instance:

An object is an instance of a class. When a class is defined, no memory is allocated until an object of that class is created. The object is an instance of the class.

Example:
```python
another_dog = Dog("Charlie")
print(another_dog.bark())
```

### 6. Difference between a class and an object or instance:

A class is a blueprint, and an object is an instance of that blueprint. An object represents a real-world entity, and a class defines its properties and behaviors.

### 7. What is an attribute:

An attribute is a characteristic or property of an object. It can be a data member (variable) or a method.

Example:
```python
print(my_dog.name)  # Accessing the 'name' attribute of the Dog object
```

### 8. Public, protected, and private attributes:

In Python, attributes can be public, protected, or private. Public attributes are accessible from outside the class, protected attributes have a single leading underscore, and private attributes have a double leading underscore.

Example:
```python
class Circle:
    def __init__(self, radius):
        self.radius = radius        # Public attribute
        self._diameter = radius * 2  # Protected attribute
        self.__area = 3.14 * radius**2  # Private attribute

my_circle = Circle(5)
print(my_circle.radius)
print(my_circle._diameter)
# Accessing a private attribute directly would result in an AttributeError
```

### 9. What is `self`:

`self` is a convention in Python that represents the instance of the class. It is the first parameter in the definition of a method and refers to the instance itself.

Example:
```python
class Person:
    def __init__(self, name):
        self.name = name

    def introduce(self):
        return f"Hello, my name is {self.name}"

person = Person("Alice")
print(person.introduce())
```

### 10. What is a method:

A method is a function associated with a class. It defines the behaviors of the objects created from the class.

Example:
```python
class Calculator:
    def add(self, x, y):
        return x + y

calculator = Calculator()
result = calculator.add(3, 5)
print(result)
```

### 11. Special `__init__` method:

`__init__` is a special method in Python classes that is called when an object is created. It initializes the object's attributes.

Example:
```python
class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author

book = Book("The Pythonic Way", "John Python")
print(book.title)
```

### 12. Data Abstraction, Data Encapsulation, and Information Hiding:

- **Abstraction:** Simplifying complex systems by modeling classes appropriate to the problem.
- **Encapsulation:** Bundling the data and the methods that operate on the data into a single unit (class).
- **Information Hiding:** Restricting access to some of an object's components.

Example:
```python
class BankAccount:
    def __init__(self, balance):
        self._balance = balance  # Protected attribute

    def get_balance(self):
        # Information hiding: The actual balance is hidden from external code.
        return f"Your balance is ${self._balance}"

account = BankAccount(1000)
print(account.get_balance())
```

### 13. What is a property:

A property is a special kind of attribute that can be accessed using the dot notation. It allows

 the implementation of getters and setters.

Example:
```python
class Temperature:
    def __init__(self, celsius):
        self._celsius = celsius

    @property
    def fahrenheit(self):
        return (self._celsius * 9/5) + 32

    @fahrenheit.setter
    def fahrenheit(self, value):
        self._celsius = (value - 32) * 5/9

temp = Temperature(25)
print(temp.fahrenheit)  # Accessing the property
temp.fahrenheit = 77   # Modifying the property using the setter
print(temp.fahrenheit)
```

### 14. Difference between an attribute and a property in Python:

An attribute is a data member, while a property is an attribute with getter and setter methods.

### 15. Pythonic way to write getters and setters:

The `@property` decorator is used for getter methods, and the `@<attribute>.setter` decorator is used for setter methods.

Example:
```python
class Rectangle:
    def __init__(self, width, height):
        self._width = width
        self._height = height

    @property
    def area(self):
        return self._width * self._height

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        if value < 0:
            raise ValueError("Width must be non-negative")
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        if value < 0:
            raise ValueError("Height must be non-negative")
        self._height = value

rectangle = Rectangle(5, 8)
print(rectangle.area)
rectangle.width = 6
print(rectangle.area)
```

### 16. Special `__str__` and `__repr__` methods:

`__str__` returns the "informal" or nicely printable string representation of an object, and `__repr__` returns the "formal" or unambiguous string representation.

Example:
```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Point({self.x}, {self.y})"

    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"

point = Point(3, 4)
print(str(point))   # Calls __str__
print(repr(point))  # Calls __repr__
```

### 17. Difference between `__str__` and `__repr__`:

`__str__` is used for the end user, while `__repr__` is used for developers and should be unambiguous.

### 18. Class attribute:

A class attribute is a variable that belongs to a class rather than an instance. It is shared among all instances of the class.

Example:
```python
class Car:
    num_wheels = 4  # Class attribute

    def __init__(self, make, model):
        self.make = make
        self.model = model

car1 = Car("Toyota", "Camry")
car2 = Car("Honda", "Accord")
print(car1.num_wheels)  # Accessing the class attribute
print(car2.num_wheels)
```

### 19. Difference between an object attribute and a class attribute:

An object attribute is specific to an instance, while a class attribute is shared among all instances.

### 20. Class method:

A class method is a method bound to the class and not the instance of the class. It takes the class itself as its first argument.

Example:
```python
class Employee:
    num_employees = 0  # Class attribute

    def __init__(self, name):
        self.name = name
        Employee.num_employees += 1  # Modifying the class attribute

    @classmethod
    def get_num_employees(cls):
        return cls.num_employees

print(Employee.get_num_employees())
employee1 = Employee("Alice")
print(Employee.get_num_employees())
```

### 21. Static method:

A static method is a method bound to the class and not the instance. It doesn't have access to the instance or class itself.

Example:
```python
class MathOperations:
    @staticmethod
    def add(x, y):
        return x + y

result = MathOperations.add(3, 5)
print(result)
```

### 22. Dynamically create arbitrary new attributes:

You can dynamically create attributes using the `setattr` function.

Example:
```python
class Student:
    pass

student = Student()
setattr(student, "name", "John")
print(student.name)
```

### 23. Bind attributes to object and classes:

Attributes can be bound to an instance using `self` and to a class using the class name.

Example:
```python
class Language:
    spoken = True  # Class attribute

    def __init__(self, name):
        self.name = name  # Object attribute

python = Language("Python")
print(python.spoken)  # Accessing class attribute
print(python.name)    # Accessing object attribute
```

### 24. `__dict__` of a class and an instance:

`__dict__` is a dictionary containing a class or an instance's namespace.

Example:
```python
class Example:
    class_attr = 42

    def __init__(self, instance_attr):
        self.instance_attr = instance_attr

obj = Example(99)
print(Example.__dict__)  # Class's namespace
print(obj.__dict__)      # Instance's namespace
```

### 25. How Python finds the attributes:

Python looks for attributes first in the instance's namespace, then in the class's namespace, and finally in the parent classes' namespaces (following the method resolution order).

### 26. How to use the `getattr` function:

`getattr` is used to get the value of an attribute of an object. It takes the object and the attribute name as arguments.

Example:
```python
class City:
    def __init__(self, name, population):
        self.name = name
        self.population = population

city = City("San Francisco", 884363)
attr_name = "population"
population = getattr(city, attr_name)
print(f"The population of {city.name} is {population}")
```

