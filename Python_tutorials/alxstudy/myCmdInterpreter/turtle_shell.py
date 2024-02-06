#!/usr/bin/env python3

import cmd,sys
from turtle import *

class TurtleShell(cmd.Cmd):
    # Intro message displayed when the shell starts
    intro = 'Welcome to the turtle shell. Type help or ? to list commands. \n'
    # Prompt displayed for user input
    prompt = '(turtle)'
    file = None  # File object for recording commands

    # ----- basic turtle commands -----


    # Move the turtle forward by the specified distance
    def do_forward(self, arg):
        'Move the turtle forward by the specified distance:  FORWARD 10'
        forward(*parse(arg))

    # Turn turtle right by given number of degrees
    def do_right(self, arg):
        'Turn  turtle right by given number of degrees:  RIGHT 20'
        right(*parse(arg))

    # Turn turtle left by given number of degrees
    def do_left(self, arg):
        'Turn turtle left by given number of degrees:  LEFT 90'
        left(*parse(arg))

    # Move turtle to an absolute position without changing orientation
    def do_goto(self, arg):
        'Move turtle to an absolute position with changing orientation.  GOTO 100 200'
        goto(*parse(arg))

    # Return turtle to the home position
    def do_home(self, arg):
        'Return turtle to the home position:  HOME'
        home()

    # Draw circle with given radius and options
    def do_circle(self, arg):
        'Draw circle with given radius an options extent and steps:  CIRCLE 50'
        circle(*parse(arg))

    # Print the current turtle position
    def do_position(self, arg):
        'Print the current turtle position:  POSITION'
        print('Current position is %d %d\n' % position())

    # Print the current turtle heading in degrees
    def do_heading(self, arg):
        'Print the current turtle heading in degrees:  HEADING'
        print('Current heading is %d\n' % (heading(),))

    # Set the color
    def do_color(self, arg):
        'Set the color:  COLOR BLUE'
        color(arg.lower())

    # Undo the last turtle action(s)
    def do_undo(self, arg):
        'Undo (repeatedly) the last turtle action(s):  UNDO'

    # Clear the screen and return turtle to center
    def do_reset(self, arg):
        'Clear the screen and return turtle to center:  RESET'
        reset()

    # Stop recording, close the turtle window, and exit
    def do_bye(self, arg):
        'Stop recording, close the turtle window, and exit:  BYE'
        print('Thanks for using Turtle')
        self.close()
        bye()
        return True

    
    # ----- record and playback -----

    # Save future commands to a file
    def do_record(self, arg):
        'Save future commands to filename:  RECORD rose.cmd'
        self.file = open(arg, 'w')

    # Playback commands from a file
    def do_playback(self, arg):
        'Playback commands from a file:  PLAYBACK rose.cmd'
        self.close()
        with open(arg) as f:
            self.cmdqueue.extend(f.read().splitlines())

    # Pre-command hook to record commands to a file
    def precmd(self, line):
        line = line.lower()
        if self.file and 'playback' not in line:
            print(line, file=self.file)
        return line

    # Close the file when the shell is closed
    def close(self):
        if self.file:
            self.file.close()
            self.file = None

# Convert a series of zero or more numbers to an argument tuple
def parse(arg):
    'Convert a series of zero or more numbers to an argument tuple'
    return tuple(map(int, arg.split()))


if __name__ == '__main__':
    # Start the turtle shell command loop
    TurtleShell().cmdloop()
