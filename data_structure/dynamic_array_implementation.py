#!/usr/bin/python3

class Stack(object):
    def __init__(self, limit=10):
        # Initialize an empty stack and set the limit
        self.stk = limit*[None]
        self.limit = limit

    def isEmpty(self):
        # Check if the stack is empty
        return len(self.stk) <= 0

    def push(self, item):
        # Push an item onto the stack
        if len(self.stk) >= self.limit:
            self.resize()
        self.stk.append(item)
        print('Stack after Push', self.stk)

    def pop(self):
        # Pop an item from the stack
        if len(self.stk) <= 0:
            print('Stack Underflow!')
            return 0
        else:
            return self.stk.pop()

    def peek(self):
        # Peek at the top of the stack
        if len(self.stk) <= 0:
            print('Stack Underflow!')
            return 0
        else:
            return self.stk[-1]

    def size(self):
        # Return the size of the stack
        return len(self.stk)

    def resize(self):
        newStk = list(self.stk)
        self.limit = 2*self.limit
        self.stk = newStk

# Create a stack with a limit of 5
our_stack = Stack(5)

# Perform stack operations
our_stack.push("1")
our_stack.push("21")
our_stack.push("14")
our_stack.push("31")
our_stack.push("19")
our_stack.push("3")
our_stack.push("99")
our_stack.push("9")

print(our_stack.peek())
print(our_stack.pop())
print(our_stack.peek())
print(our_stack.pop())

