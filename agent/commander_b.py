# agent/commander_b.py

class CommanderB:
    def __init__(self, rnd, field_view):
        self.field = field_view
        self.rnd = rnd

    def decide(self, team_data, enemy_data):
        #ランダムに行動決定
        return [self.rnd.randint(0, 7) for _ in team_data]