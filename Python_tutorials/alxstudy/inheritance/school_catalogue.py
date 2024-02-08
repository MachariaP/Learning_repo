#!/usr/bin/python3

"""
This script defines classes to represent schools, including a generic School class, a PrimarySchool class, and a HighSchool class
Each class has properties such as name, level, and number of students, as well as getters, setters, and a method to represent the object as a string.
The PrimarySchool class includes an additional property for pickup policy, while the HighSchool class includes a property for sports teams.
Test cases are provided to demonstrate the functionality of the classes.
"""

class School:
    def __init__(self, name, level, number_of_students):
        self.name = name
        self.level = level
        self.number_of_students = number_of_students

    # Create getters
    def get_name(self):
        return self.name

    def get_level(self):
        return self.level

    def get_number_of_students(self):
        return self.number_of_students

    # Create setter
    def set_number_of_students(self, number):
        self.number_of_students = number

    # Create repr()
    def __repr__(self):
        return f"A {self.name} school named {self.level} with {self.number_of_students} students"


class PrimarySchool(School):
    def __init__(self, name, number_of_students, pickup_policy):
        self.pickup_policy = pickup_policy
        super().__init__(name, "Primary", number_of_students)

    def get_pickup_policy(self):
        return self.pickup_policy

    def __repr__(self):
        return super().__repr__() + f" With pickupPolicy: {self.pickup_policy}"


class HighSchool(School):
    def __init__(self, name, number_of_students, sport_teams):
        self.sport_teams = sport_teams
        super().__init__(name, "High School", number_of_students)

    def get_sport_teams(self):
        return self.sport_teams

    def __repr__(self):
        return super().__repr__() + f" with sportTeams: {self.sport_teams}"

# Create a School object
school = School("XYZ School", "High", 7877)

# Test getter method
print("School name is: ", school.get_name())
print("School level is: ", school.get_level())
print("Number of students: ", school.get_number_of_students())

# Test setter method
school.set_number_of_students(150)
print("Updated number of Students is : ", school.get_number_of_students())

# Print the object using __repr__ method
print(school)

# Create a PrimarySchool object
primary_school = PrimarySchool("ABC Primary School", 350, "Pickup after 3pm")

# Test getter method
print("Primary School name is: ", primary_school.get_name())
print("Primary School level is: ", primary_school.get_level())
print("Number of students in Primary School is: ", primary_school.get_number_of_students())
print("Pickup policy for Primary School: ", primary_school.get_pickup_policy())

# Print the Primary School object using __repr__ method
print(primary_school)

# Create a HighSchool object
high_school = HighSchool("EFG High School", 450, ["basketball", "football"])

# Test getter method
print("High School name is: ", high_school.get_name())
print("High School level is: ", high_school.get_level())
print("Number of Students in High School: ", high_school.get_number_of_students())
print("Sport teams for High School: ", high_school.get_sport_teams())

# Print the High School object using __repr__ method
print(high_school)
