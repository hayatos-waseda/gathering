# renderer/simple_gif_maker.py

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle, Rectangle

class GIFMaker:
    def __init__(self, grid):
        self.grid_size = len(grid)
        self.map = grid
        self.frames = []
        self.fig, self.ax = plt.subplots(figsize=(5,5))

    def update(self, step, score1, score2, event, pos1, pos2, action1, action2):
        artists = []

        self.ax.set_xlim(-0.5, self.grid_size - 0.5)
        self.ax.set_ylim(-0.5, self.grid_size - 0.5)

        # ===== 背景 =====
        grid = np.zeros((self.grid_size, self.grid_size))
        im = self.ax.imshow(grid, cmap="Greys", vmin=0, vmax=1)
        artists.append(im)

        # ===== グリッド線 =====
        self.ax.set_xticks(np.arange(-0.5, self.grid_size, 1))
        self.ax.set_yticks(np.arange(-0.5, self.grid_size, 1))
        self.ax.grid(color="black", linestyle='-', linewidth=1)

        # 軸消す（見やすく）
        self.ax.set_xticklabels([])
        self.ax.set_yticklabels([])

        # ===== 壁描画 =====
        if self.map is not None:
            for x in range(self.grid_size):
                for y in range(self.grid_size):
                    if self.map[y][x] == "#":
                        artists.append(
                            self.ax.add_patch(
                                Rectangle(
                                    (x-0.5, y-0.5),
                                    1, 1,
                                    color="black"
                                )
                            )
                        )

        # ===== イベント =====
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if event[x][y] == 1:
                    artists.append(
                        self.ax.text(x, y, "★",
                                    ha="center", va="center",
                                    fontsize=20, color="orange")
                    )

        # ===== エージェント =====
        if pos1[0] >= 0:
            artists.append(
                self.ax.add_patch(
                    Circle((pos1[0], pos1[1]), 0.3, color="red", zorder=3)
                )
            )

        if pos2[0] >= 0:
            artists.append(
                self.ax.add_patch(
                    Circle((pos2[0], pos2[1]), 0.3, color="blue", zorder=3)
                )
            )
        
        artists += self.draw_attack(pos1, action1, "red")
        artists += self.draw_attack(pos2, action2, "blue")

        # ===== テキスト =====
        artists.append(
            self.ax.text(
                0.5, 1.05,
                f"Step:{step}  P1:{score1}  P2:{score2}",
                transform=self.ax.transAxes,
                ha="center"
            )
        )

        self.frames.append(artists)
    
    def draw_attack(self, pos, action, color):
        if pos[0] < 0:
            return []

        x, y = pos
        effects = []

        if action < 4 or action is None:
            return effects

        dx, dy = 0, 0

        if action == 4:   # 上
            dy = 1
        elif action == 5: # 右
            dx = 1
        elif action == 6: # 下
            dy = -1
        elif action == 7: # 左
            dx = -1

        # 線で表現
        effects.append(
            self.ax.plot(
                [x, x + dx],
                [y, y + dy],
                color=color,
                linewidth=3,
                alpha=0.7
            )[0]
        )

        return effects

    def save(self, path="result.gif"):
        ani = animation.ArtistAnimation(self.fig, self.frames, interval=250, repeat=False)
        ani.save(path, writer="pillow")
        plt.close()