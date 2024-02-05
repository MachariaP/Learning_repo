# Modules

1. **Python Interpreter:**
   - When you use the Python interpreter, it allows you to run Python commands and see their immediate results.

2. **Definitions Lost on Quitting:**
   - If you define functions or variables in the interpreter and then quit, those definitions are lost.

3. **Using a Text Editor for Longer Programs:**
   - For longer programs, it's better to use a text editor to prepare your code. This way, you can save it as a file.

4. **Creating a Script:**
   - Saving your code in a file and running it is called creating a script. This is useful for longer programs.

5. **Splitting into Several Files:**
   - As your program grows, you might want to split it into multiple files. This makes it easier to manage.

6. **Using Handy Functions:**
   - If you have a function used in multiple programs, you don't want to copy its definition every time.

7. **Introducing Modules:**
   - Python has a solution called modules.
   - A module is a file with Python definitions and statements.
   - The file name is the module name with the `.py` extension.

8. **__name__ Variable:**
   - Within a module, there's a global variable `__name__`.
   - This variable holds the module's name as a string.
   - It helps in identifying if the module is being run standalone or imported into another module.

In simpler terms, using a text file to store your code as a script is more practical for longer programs. Modules are like containers for your code that you can reuse in other programs. The `__name__` variable in a module helps Python understand how the module is being used.

## More on Modules

- **Executable Statements in Modules:**
  - Modules can contain executable statements and function definitions.
  - These statements initialize the module and execute only the first time the module name is encountered in an import statement. They also run if the file is executed as a script.

- **Private Symbol Table:**
  - Each module has its private symbol table.
  - It serves as the global symbol table for all functions defined in the module.
  - Allows the use of global variables in the module without worrying about clashes with a user's global variables.

- **Accessing Module Variables:**
  - The author can use global variables in a module using the notation `modname.itemname`.
  - This ensures that module's global variables do not accidentally clash with user's global variables.

- **Importing Other Modules:**
  - Modules can import other modules.
  - Import statements are typically placed at the beginning of a module.
  - Imported module names are added to the importing module's global symbol table.

- **Importing Specific Names:**
  - Specific names can be imported directly into the importing module's symbol table.
  - Example: `from fibo import fib, fib2`.
  - The module name from which the imports are taken is not introduced into the local symbol table.

- **Importing All Names:**
  - Another variant imports all names defined by a module.
  - Example: `from fibo import *`.
  - Excludes names beginning with an underscore (_).
  - Generally frowned upon due to readability concerns.

- **Efficiency Note:**
  - Each module is imported only once per interpreter session for efficiency.
  - If you change modules, you must restart the interpreter or use `imp.reload()` for interactive testing.

- **Caution about Importing All Names:**
  - Importing all names from a module is discouraged as it can introduce an unknown set of names, potentially hiding previously defined names.
  - Recommended for interactive sessions to save typing.

- **Note on Restarting the Interpreter:**
  - If you change modules, restarting the interpreter or using `imp.reload()` is necessary.
  - Example: `import imp; imp.reload(modulename)`.

### Executing modules as scripts
- **Running a Python Module:**
  - When you run a Python module using `python fibo.py <arguments>`, the module's code is executed.
  - It behaves as if it were imported, but with the `__name__` set to `"__main__"`.

- **Using a Module as a Script:**
  - You can make a module usable as both a script and an importable module by adding the following code at the end:
    ```python
    if __name__ == "__main__":
        import sys
        fib(int(sys.argv[1]))
    ```
  - This allows the file to be executed as a script or imported as a module.

- **Command Line Parsing:**
  - The code that parses the command line (`fib(int(sys.argv[1]))`) runs only if the module is executed as the main file.

- **Example Usage as a Script:**
  - Running the module as a script: `$ python fibo.py 50`
  - Output: `1 1 2 3 5 8 13 21 34`

- **Module Import Behavior:**
  - If the module is imported, the code inside the `if __name__ == "__main__":` block is not run.

- **Common Use Cases:**
  - Often used to provide a convenient user interface to a module.
  - Useful for testing purposes; running the module as a script can execute a test suite.
