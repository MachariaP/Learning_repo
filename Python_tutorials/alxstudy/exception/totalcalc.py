#!/usr/bin/python3
# The Total Calculator program
"""
It handles the ValueError exceptions that can occur 
when the program tries to convert the strings that the user 
enters for price and quantity to float and int values.

"""
def get_price():
    while True:
        try:
            price = float(input("Enter price: "))
            return price
        except ValueError:
            print("Invalid decimal number. Please try again.")

def get_quantity():
    while True:
        try:
            quantity = int(input("Enter quantity: "))
            return quantity
        except ValueError:
            print("Invalid integer. Please try again.")

def main():
    print("The Total Calculator program\n")

    # get the price and quantity
    price = get_price()
    quantity = get_quantity()

    # calculate the total
    total = price * quantity

    # display the results
    print()
    print("PRICE: ", price)
    print("QUANTITY: ", quantity)
    print("TOTAL: ", total)

if __name__ == "__main__":
    main()

