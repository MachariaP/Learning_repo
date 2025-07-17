#!/usr/bin/env python3

class Salary:
    def __init__(self, name, amount):
        self.name = name
        self.amount = amount

account1 = Salary("James", 54000)
account2 = Salary("Jane", 45000)

print(account1.name, account1.amount)
print(account2.name, account2.amount)
