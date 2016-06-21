from random import randint, seed
from .bot import Agent

class RandomAgent(Agent):
    def __init__(self):
        seed()

    def init_game(self):
        pass

    def next_move(self, map, players, bombs):
        opt = ["ACTION LEFT",
               "ACTION RIGHT",
               "ACTION UP",
               "ACTION DOWN",
               "ACTION BOMB"]
        return opt[randint(0, 4)]

    def end_game(self, players):
        pass