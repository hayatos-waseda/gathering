# agent/commander_a.py
from agent.utils.astar import astar

class CommanderA:
    def __init__(self, rnd, field_view):
        self.field = field_view
        self.rnd = rnd

    def decide(self, team_data, enemy_data):
        """
        引数:
            team_data  : 味方エージェントの情報リスト
                         [{"pos": [x, y], "status": "active"}, ...]
            enemy_data : 敵エージェントの情報リスト
                         [{"pos": [x, y], "status": "active"}, ...]

        返り値:
            各エージェントへの行動リスト（team_data と同じ順序）
            例) [1, 3]  -> playerA1 は右移動、playerA2 は左移動

        行動番号:
            0: 上移動  1: 右移動  2: 下移動  3: 左移動
            4: 上攻撃  5: 右攻撃  6: 下攻撃  7: 左攻撃  8: 何もしない
        """

        # ここを実装しよう！
        # team_data の順番と返り値リストの順番は対応しています。
        # 例: return [action_for_agent0, action_for_agent1]

        actions = []
        for agent in team_data:
            actions.append(self.rnd.randint(0, 7))
        return actions