# agent/action_a.py
from agent.utils.astar import astar
import random

class ActionA:
    def __init__(self, rnd, field_view):
        self.field = field_view
        self.rnd = rnd

    def act(self, pos, status, a_data, e_data):
        # ここの中を編集しよう！

        # 使える変数など
        # pos: 自分の座標 [3, 4]
        # status: 自分のstatus 例) "invinsible" 
        # a_data: 味方の情報リスト 例) [{"pos": [1, 2], "status": "broken"}, ...]
        # e_data: 敵の情報リスト   例) [{"pos": [5, 6], "status": "invincible"}, ...]

        # self.field.get_event(x, y): ★があれば1, なければ0
        # 例) self.field.get_event(3, 4) -> 1
    

        return self.rnd.randint(0, 7)