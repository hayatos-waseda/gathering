# agent/action_b.py

import random

class RandomAct:
    def __init__(self, rnd, field_view):
        self.field = field_view
        self.rnd = rnd

    def act(self, pos, a_data, e_data):
        return self.rnd.randint(0, 7)