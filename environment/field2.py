# environment/field1.py

import random
import numpy as np
from environment.map_loader import MapLoader

class Field1:
    def __init__(self, rnd, grid):

        self.field = MapLoader.build_field_from_map(grid)
        self.grid_size = len(grid)

        self.event = np.zeros((self.grid_size, self.grid_size), dtype=int)
        self.p = np.zeros((self.grid_size, self.grid_size))

        # 確率リスト生成
        p_set = [0.05, 0.01, 0.001]
        p_rate = [0.1, 0.5, 0.4]

        num_p = []
        p_list = []

        for i in range(3):
            app = int(round(self.grid_size * self.grid_size * p_rate[i]))
            num_p.append(app)
            for _ in range(num_p[i]):
                p_list.append(p_set[i])

        rnd.shuffle(p_list)

        # 配置
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.event[i][j] = 0
                self.p[i][j] = p_list[i*5 + j]

    # イベント発生
    def happen_event(self, rnd):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if rnd.random() < self.p[i][j]:
                    self.event[i][j] = 1

    # 行動可能か
    def get_pos_status(self, x, y, act=None):
        if act is None:
            return self.field[x][y]
        return self.field[x][y][act]

    def get_field(self):
        return self.field

    # イベント取得
    def acquire_event(self, x, y):
        result = self.event[x][y]
        self.event[x][y] = 0
        return result

    def get_event(self, x, y):
        return self.event[x][y]

    def get_p(self, x, y):
        return self.p[x][y]
    
    def show_p(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                print(self.get_p(j, i), end=", ")
            print()