#!/usr/bin/env python3

import cmd

class HelloWorld(cmd.Cmd):
    """Simple command processor example"""

    # List of friends
    FRIENDS = [ 'Alice', 'Adam', 'Barbara', 'Bob' ]


    def do_greet(self, person):
        "Greet the person"
        # Check if the person is specified and if it's in the FRIENDS list
        if person and person in self.FRIENDS:
            greeting = 'hi, %s!' % person
        # If person is specified but not in the FRIENDS list
        elif person:
            greeting = "hello, " + person
        # If no person is specified
        else:
            greeting = 'hello'
        # Print the greeting
        print(greeting)

    def complete_greet(self, text, line, begidx, endidx):
        # Auto-completion for the greet command
        if not text:
            completions = [ f
                    for f in self.FRIENDS
                    if f.startswith(text)
                    ]
        return completions

    def do_EOF(self, line):
        # Handle end-of-line (ctrl+D) to exit the program
        return true

if __name__ == '__main__':
    # Instantiate and run the Helloworld command processor
    HelloWorld().cmdloop()
