-   [Program Frameworks](https://docs.python.org/3.8/library/frameworks.html)

# [`cmd`](https://docs.python.org/3.8/library/cmd.html#module-cmd "cmd: Build line-oriented command interpreters.")


1. **What is Cmd Class?**
   - The `Cmd` class is a part of Python that helps in creating simple command interpreters. These interpreters are useful for various tasks like testing, administrative tools, and creating initial versions of programs that will later have more advanced interfaces.

2. **How to Use Cmd Class:**
   - To use the `Cmd` class, you don't create an instance directly but instead create a new class that inherits from `Cmd`. Your new class will then act as an interpreter, inheriting useful methods from `Cmd` to handle commands.

3. **Key Concepts:**
   - `completekey`: An optional setting that defines the key to trigger command completion. By default, it's set to Tab, and if the system supports it (like in command line interfaces), it enables automatic completion of commands.
   - `stdin` and `stdout`: These are optional settings to specify where the interpreter reads input from (`stdin`) and writes output to (`stdout`). If not provided, the interpreter will use the default input and output (keyboard and screen).
   - `use_rawinput`: A setting to indicate whether the interpreter should use a raw form of input. If set to False, the interpreter will consider the specified `stdin` for input.

4. **Example Usage:**
   - If you want to create a command interpreter, you would typically create a new class, inherit from `Cmd`, and define methods to handle different commands.

5. **Example Code:**
   ```python
   import cmd

   class MyCmdInterpreter(cmd.Cmd):
       def do_hello(self, line):
           print("Hello,", line)

   if __name__ == "__main__":
       my_interpreter = MyCmdInterpreter()
       my_interpreter.cmdloop()
   ```
   In this example, the interpreter understands a command `hello` that takes an argument, and it responds with a greeting.

6. **Summary:**
   - `Cmd` class simplifies the creation of command interpreters.
   - It's used as a superclass for a custom interpreter class.
   - Allows customization of completion keys, input, and output settings.



### Cmd Objects in Python

1. **What is a Cmd Object?**
   - A `Cmd` object in Python provides a framework for creating command-line interpreters.
   - It's useful for building tools like test harnesses, administrative utilities, or interactive prototypes.

2. **Key Methods of a Cmd Object:**

   - **`cmdloop(intro=None)`:**
     - This method starts a loop where the interpreter repeatedly prompts the user for input.
     - It accepts input, parses it, and dispatches it to appropriate action methods.
     - You can provide an optional intro message to display before the first prompt.

   - **`onecmd(str)`:**
     - Interprets the argument as if it were typed in response to the prompt.
     - Returns a flag indicating whether command interpretation should stop.

   - **`emptyline()`:**
     - Called when the user enters an empty line in response to the prompt.
     - If not overridden, it repeats the last nonempty command entered.

   - **`default(line)`:**
     - Called when the command prefix is not recognized.
     - If not overridden, it prints an error message.

   - **`completedefault(text, line, begidx, endidx)`:**
     - Called to complete an input line when no command-specific completion method is available.

3. **Hooks and Control Methods:**

   - **`precmd(line)`:**
     - Executed just before the command line is interpreted.
     - It can rewrite the command or return it unchanged.

   - **`postcmd(stop, line)`:**
     - Executed just after a command dispatch is finished.
     - It returns a flag indicating whether interpretation should continue.

   - **`preloop()` and `postloop()`:**
     - Executed once when `cmdloop()` is called and about to return, respectively.
     - They exist to be overridden by subclasses for any necessary setup or teardown.

4. **Public Instance Variables:**

   - **`prompt`**: The prompt issued to solicit input.
   - **`identchars`**: Characters accepted for the command prefix.
   - **`lastcmd`**: Last nonempty command prefix seen.
   - **`cmdqueue`**: A list of queued input lines.
   - **`intro`**: A string to issue as an intro or banner.
   - **`doc_header`, `misc_header`, `undoc_header`**: Headers for different sections of help output.
   - **`ruler`**: Character used to draw separator lines in help messages.
   - **`use_rawinput`**: Flag indicating whether `cmdloop()` uses `input()` for input prompts.

5. **Usage Example:**
   - You can create a custom interpreter by subclassing `Cmd` and implementing action methods for specific commands.

6. **Benefits:**
   - Provides a structured way to build command-line interfaces.
   - Offers features like command completion, history navigation, and input validation.
   - Helps organize code for interactive applications and utilities.

