# agent/agent_a.py
from agent.action_b import ActionB

class AgentB:
    def __init__(self, rnd, field, pos):
        self.field = field
        self.pos = pos[:] 
        self.status = "active"
        self.action_b = ActionB(rnd, field, pos)
        self.broken_time = -1
        self.attack_range = 2

    def action(self, a_data, e_data):
        return self.action_b.act(self.pos, a_data, e_data)

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
        
        curr_x, curr_y = self.pos[0], self.pos[1]
        move_dir = act - 4 

        # 射程距離の分だけ1マスずつ判定を進める
        for _ in range(self.attack_range):
            # get_pos_status が 1 なら壁やマップ端がない
            if self.field.get_pos_status(curr_x, curr_y, move_dir) == 1:
                # 座標を1マス進める
                if move_dir == 0: curr_y += 1
                elif move_dir == 1: curr_x += 1
                elif move_dir == 2: curr_y -= 1
                elif move_dir == 3: curr_x -= 1
                
                # 敵がその座標にいればヒット
                if curr_x == e_pos[0] and curr_y == e_pos[1]:
                    hit = 1
                    break
            else:
                break
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