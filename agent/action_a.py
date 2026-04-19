# agent/action_a.py

import random

class ActionA:
    def __init__(self, rnd, field, pos):
        self.field = field
        self.rnd = rnd

    def act(self, pos, a_pos, e_pos):
        return self.rnd.randint(0, 7)