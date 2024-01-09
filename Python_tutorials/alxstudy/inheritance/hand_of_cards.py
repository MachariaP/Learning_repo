#!/usr/bin/python3

class Hand(Deck):
    def __init__(self, name=" "):
        self.cards = []
        self.name = name

    """
    list append method adds new cards to the end of the list cards

    """

    def add(self, card):
        self.cards.append(card)
