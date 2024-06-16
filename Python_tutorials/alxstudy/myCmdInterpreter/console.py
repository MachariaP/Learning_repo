#!/usr/bin/env python3

import cmd
import sys

class MyConsole(cmd.Cmd):
    """Simple console example."""

    prompt = "(hbnb) "

    def do_help(self, arg):
        """Display help."""
        print("\nDocumented commands (type help <topic>):")
        print("=" * 40)
        print("EOF  help  quit")

    def do_EOF(self, arg):
        """Exit on EOF."""
        return True

    def do_quit(self, arg):
        """Quit the console."""
        return True

    # Override emptyline method to do nothing on empty input
    def emptyline(self):
        pass

def interactive_mode():
    """Run the console in interactive mode."""
    console = MyConsole()
    console.cmdloop()

def non_interactive_mode(commands):
    """Run the console in non-interactive mode."""
    console = MyConsole()
    for command in commands:
        console.onecmd(command)

if __name__ == "__main__":
    # Check if input is from stdin
    if sys.stdin.isatty():  # Interactive mode
        interactive_mode()
    else:  # Non-interactive mode
        input_commands = sys.stdin.readlines()
        non_interactive_mode(input_commands)
