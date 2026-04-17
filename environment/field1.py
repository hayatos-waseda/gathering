# environment/field1.py

import random
from environment.map_loader import MapLoader

class Field1:
    def __init__(self, rnd, grid, config):

        self.grid = grid
        self.field = MapLoader.build_field_from_map(grid)
        self.grid_size = len(grid)

        self.event = [[0]*5 for _ in range(5)]
        self.p = [[0.0]*5 for _ in range(5)]

        # 確率リスト生成
        p_set = config["event"]["p_set"]
        p_prob = config["event"]["p_distribution"]

        for y in range(self.grid_size):
            for x in range(self.grid_size):

                if grid[y][x] == "#":
                    self.p[x][y] = 0.0
                    continue

                self.p[x][y] = rnd.choices(p_set, weights=p_prob, k=1)[0]

    # イベント発生
    def happen_event(self, rnd):
        for i in range(5):
            for j in range(5):
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