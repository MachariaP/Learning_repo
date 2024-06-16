#!/usr/bin/python3

class Agent():

    def __init__(self, name, health, car):
        self.name = name
        self.health = health
        self.car = car

    def player_info(self):

        print("Welcome ", self.name)
        print("Your health: ", self.health)
        print("Car choice: ", self.car)

spy = Agent("James Bond", 100, "Jaguar")
villian = Agent("Ethan Hunt", 60, "Ferrari")

spy.player_info()
villian.player_info()
