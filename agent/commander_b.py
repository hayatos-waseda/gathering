# agent/commander_b.py

class CommanderB:
    def __init__(self, rnd, field_view):
        self.field = field_view
        self.rnd = rnd

    def decide(self, team_data, enemy_data):
        #ランダムに行動決定
        actions = []
        for agent in team_data:
            actions.append(self.rnd.randint(0, 7))
        return actions