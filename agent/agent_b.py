# agent/agent_a.py
from agent.action_b import ActionB

class AgentB:
    def __init__(self, rnd, field, pos):
        self.field = field
        self.pos = pos[:]  # コピー重要
        self.status = "active"
        self.action_a = ActionB(rnd, field, pos)
        self.broken_time = -10**9  # Integer.MIN_VALUE相当

    def action(self, e_pos):
        return self.action_a.act(self.pos, e_pos)

    def move(self, act):
        x, y = self.pos

        if act == 0:  # 上
            if self.field.get_pos_status(x, y, act) == 1:
                self.pos[1] += 1
        elif act == 1:  # 右
            if self.field.get_pos_status(x, y, act) == 1:
                self.pos[0] += 1
        elif act == 2:  # 下
            if self.field.get_pos_status(x, y, act) == 1:
                self.pos[1] -= 1
        elif act == 3:  # 左
            if self.field.get_pos_status(x, y, act) == 1:
                self.pos[0] -= 1

    def attack(self, act, e_pos):
        hit = 0
        #攻撃範囲はここで設定できそう

        if act == 4:  # 上攻撃
            if self.pos[0] == e_pos[0] and self.pos[1] == e_pos[1] - 1:
                hit = 1
        elif act == 5:  # 右攻撃
            if self.pos[1] == e_pos[1] and self.pos[0] == e_pos[0] - 1:
                hit = 1
        elif act == 6:  # 下攻撃
            if self.pos[0] == e_pos[0] and self.pos[1] == e_pos[1] + 1:
                hit = 1
        elif act == 7:  # 左攻撃
            if self.pos[1] == e_pos[1] and self.pos[0] == e_pos[0] + 1:
                hit = 1

        return hit

    def respawn(self, rnd, field):
        while True:
            x = rnd.randrange(field.grid_size)
            y = rnd.randrange(field.grid_size)

            # 壁じゃない
            if field.grid[y][x] == "#":
                continue

            self.pos = [x, y]
            break

    def can_act(self, time, rnd):
        if self.status != "broken":
            return True

        if time - self.broken_time < 6:
            return False

        self.status = "active"
        self.respawn(rnd, self.field)
        return True

    def get_pos(self):
        return self.pos

    def get_status(self):
        return self.status

    def broken(self, time):
        self.status = "broken"
        self.broken_time = time
        self.pos[0] = -1
        self.pos[1] = -1