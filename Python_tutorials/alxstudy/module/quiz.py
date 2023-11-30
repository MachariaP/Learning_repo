#!/usr/bin/python3

def my_function(counter=89):
    print("counter: {}".format(counter))

my_function()


def my_function(counter=89):
    print("counter: {}".format(counter))

my_function(12)


def my_function(counter=89):
    return counter + 1

print(my_function())


def my_function(counter=89):
    print("In my function")

my_function()



def my_function(counter):
    print("counter: {}".format(counter))

my_function(12)



def my_function():
    print("In my function")

my_function