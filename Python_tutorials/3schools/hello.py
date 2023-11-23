# PYTHON STRINGS
# Python check string
txt = "The best thing in life are free!"
if "free" in txt:
    print("Yes, 'free' is present." )

# Python check if NOT
txt = "The best things in life are free!"
print("expensive" not in txt)

#use it in an if statement
txt = "The best things in life are free!"
if "expensive" not in txt:
    print("No, 'expensive' is NOT present.")

#Python - Slicing Strings
b = "Hello World!"
print(b[2:5])

#Slice From the Start
#Give the characters from the start to position 5(not included):
b = "Hello, World!"
print(b[:5])

#Slice To the End
#Give the characters from position 2, and all the way to the end:
b = "Hello, World!"
print(b[2:])

#Negative Indexing
#Use negative indexes to start the slice from the end of the string:
b = "Hello, World!"
print(b[-5: -2])

# Python Modify Strings
    # 1. Upper Case
#The upper() method returns the string in upper case:
a = "Hello, World!"
print(a.upper())

    # 2. Lower Case
#The lower() method returns the string in lower case:
a = "Hello, World!"
print(a.lower())

    # 3. Remove Whitespace
#Whitespace is the space before and/or after the actual text, and very often you want to remove this space.
#The strip() method removes any whitespace from the beginning or the end:
a = " Hello, World! "
print(a.strip()) #returns "Hello, World!"

    # 4. Replace String
#The replace() method replaces a string with another string:
a = "Hello, World!"
print(a.replace("H", "J"))

    # 5. Split String
#The split() method returns a list where the text between the specified separator becomes the list items.
#The split() method splits the string into substrings if it finds instances of the separator:
a = "Hello, World!"
print(a.split(","))