#!/usr/bin/python3

import cmd

class MyCmdInterpreter(cmd.Cmd):
    def do_hello(self, line):
        print("Hello,", line)


if __name__ == "__main__":
    my_interpreter = MyCmdInterpreter()
    my_interpreter.cmdloop()
