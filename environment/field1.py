# environment/field1.py

import random
import numpy as np
from environment.map_loader import MapLoader

class Field:
    def __init__(self, rnd, env_config):
        
        self.grid = MapLoader.load_map(env_config["map_path"])
        self.field = MapLoader.build_field_from_map(self.grid)
        self.grid_size = len(self.grid)

        self.event = np.zeros((self.grid_size, self.grid_size), dtype=int)
        self.p = np.zeros((self.grid_size, self.grid_size))

        # 確率リスト生成
        p_set = env_config["event"]["p_set"]
        p_prob = env_config["event"]["p_distribution"]

        for y in range(self.grid_size):
            for x in range(self.grid_size):

                if self.grid[y][x] == "#":
                    self.p[x][y] = 0.0
                    continue

                self.p[x][y] = rnd.choices(p_set, weights=p_prob, k=1)[0]


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
    
    def is_path(self, x, y):
        return self.grid[y][x] != "#"

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
