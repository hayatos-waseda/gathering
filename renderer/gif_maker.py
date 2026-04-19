# renderer/simple_gif_maker.py

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle, Rectangle
from collections import defaultdict


TEAM_COLORS = {
    "A": "red",
    "B": "blue"
}


class GIFMaker:
    def __init__(self, grid):
        self.grid_size = len(grid)
        self.map = grid
        self.frames = []
        self.fig, self.ax = plt.subplots(figsize=(5, 5))

    def update(self, step, scores, event, positions, actions, teams, attack_ranges):
        artists = []

        # ===== 軸固定（超重要） =====
        self.ax.set_xlim(-0.5, self.grid_size - 0.5)
        self.ax.set_ylim(-0.5, self.grid_size - 0.5)
        self.ax.set_aspect("equal")
        self.ax.set_autoscale_on(False)

        # ===== 背景 =====
        grid = np.zeros((self.grid_size, self.grid_size))
        im = self.ax.imshow(grid, cmap="Greys", vmin=0, vmax=1)
        artists.append(im)

        # ===== グリッド線 =====
        self.ax.set_xticks(np.arange(0, self.grid_size, 1))
        self.ax.set_yticks(np.arange(0, self.grid_size, 1))
        self.ax.tick_params(which='major', length=0)

        self.ax.set_xticks(np.arange(-0.5, self.grid_size, 1), minor=True)
        self.ax.set_yticks(np.arange(-0.5, self.grid_size, 1), minor=True)
        self.ax.grid(which='minor', color="black", linestyle='-', linewidth=1)

        # ===== 壁 =====
        if self.map is not None:
            for y in range(self.grid_size):
                for x in range(self.grid_size):
                    if self.map[y][x] == "#":
                        artists.append(
                            self.ax.add_patch(
                                Rectangle((x - 0.5, y - 0.5), 1, 1, color="black")
                            )
                        )

        # ===== イベント =====
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if event[x][y] == 1:
                    artists.append(
                        self.ax.text(
                            x, y, "★",
                            ha="center", va="center",
                            fontsize=20, color="orange"
                        )
                    )

        # ===== エージェント =====
        for pos, team in zip(positions, teams):
            if pos[0] < 0:
                continue

            color = TEAM_COLORS.get(team, "green")

            artists.append(
                self.ax.add_patch(
                    Circle((pos[0], pos[1]), 0.3, color=color, zorder=3)
                )
            )

        # ===== 攻撃エフェクト =====
        for pos, action, team, attack_range in zip(positions, actions, teams, attack_ranges):
            color = TEAM_COLORS.get(team, "green")
            artists += self.draw_attack(pos, action, color, attack_range)

        # ===== テキスト =====
        team_score = defaultdict(int)
        for team, score in zip(teams, scores):
            team_score[team] += score

        score_text = " | ".join(
            [f"{team}:{team_score[team]}" for team in sorted(team_score)]
        )

        artists.append(
            self.ax.text(
                0.5, 1.05,
                f"Step:{step}  {score_text}",
                transform=self.ax.transAxes,
                ha="center"
            )
        )

        self.frames.append(artists)

    def draw_attack(self, pos, action, color, attack_range):
        if pos[0] < 0 or action is None or action < 4:
            return []

        x, y = pos
        dx, dy = 0, 0
        if action == 4: dy = 1
        elif action == 5: dx = 1
        elif action == 6: dy = -1
        elif action == 7: dx = -1

        end_x, end_y = x, y

        for _ in range(attack_range):
            nx, ny = end_x + dx, end_y + dy
            
            # マップ外判定
            if not (0 <= nx < self.grid_size and 0 <= ny < self.grid_size):
                break
            
            # 壁判定
            if self.map[ny][nx] == "#":
                break
            
            end_x, end_y = nx, ny

        # 目の前がすぐ壁などで攻撃が1マスも伸びなかった場合
        if end_x == x and end_y == y:
            return []

        return [
            self.ax.plot(
                [x, end_x],
                [y, end_y],
                color=color,
                linewidth=5,
                alpha=0.7
            )[0]
        ]

    def save(self, path="result.gif"):
        ani = animation.ArtistAnimation(
            self.fig,
            self.frames,
            interval=400,
            repeat=False
        )
        ani.save(path, writer="pillow")
        plt.close()