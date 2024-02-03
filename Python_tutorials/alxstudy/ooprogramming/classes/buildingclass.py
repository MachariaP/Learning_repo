# Building a Class
'''
Class allows us to:
    define/create a new class
'''

class ClassName:
    '''
    For every parameter in __init__, you MUST also
    give the same number of ARGUMENTS when you
    CREATE an object
    '''

    '''
    self is always the first parameter; it allows us
    to use properties and methods anywhere within a
    class
    '''

    def __init__(self, parameter):
        self.property = parameter

    def class_details(self):
        print("Show me the details:", self.property)

# Creating an instance of the class.
# The argument is given to the __init__ function

object_instance = ClassName(Argument)

