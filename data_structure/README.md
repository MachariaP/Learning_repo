

```markdown
# Python Stack Implementation

This is a simple Python implementation of a stack using a class named `Stack`. The stack supports basic operations such as push, pop, peek, check if it's empty, and retrieve its size.

## Usage

### 1. Initialization:

You can initialize a stack with a specified limit (default is 10):

```python
our_stack = Stack(5)
```

### 2. Push:

To push an item onto the stack:

```python
our_stack.push("1")
```

If the stack is full, it will print "Stack Overflow!"

### 3. Pop:

To pop an item from the stack:

```python
popped_item = our_stack.pop()
```

If the stack is empty, it will print "Stack Underflow!" and return 0.

### 4. Peek:

To peek at the top of the stack:

```python
top_item = our_stack.peek()
```

If the stack is empty, it will print "Stack Underflow!" and return 0.

### 5. Check if Empty:

To check if the stack is empty:

```python
is_empty = our_stack.isEmpty()
```

### 6. Get Size:

To get the size of the stack:

```python
stack_size = our_stack.size()
```

## Example

Here's an example of creating a stack, pushing elements, and performing operations:

```python
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
```
