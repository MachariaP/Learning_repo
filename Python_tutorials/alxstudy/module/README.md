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
