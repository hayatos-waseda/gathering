# renderer/gif_maker.py

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

        # ===== 静的要素はinitで一度だけ設定 =====
        self.ax.set_xlim(-0.5, self.grid_size - 0.5)
        self.ax.set_ylim(-0.5, self.grid_size - 0.5)
        self.ax.set_aspect("equal")
        self.ax.set_autoscale_on(False)

        self.ax.set_xticks(np.arange(0, self.grid_size, 1))
        self.ax.set_yticks(np.arange(0, self.grid_size, 1))
        self.ax.tick_params(which='major', length=0)
        self.ax.set_xticks(np.arange(-0.5, self.grid_size, 1), minor=True)
        self.ax.set_yticks(np.arange(-0.5, self.grid_size, 1), minor=True)
        self.ax.grid(which='minor', color="black", linestyle='-', linewidth=1)

        # ===== 壁パッチも使い回す =====
        self.static_artists = []
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                if self.map[y][x] == "#":
                    self.static_artists.append(
                        self.ax.add_patch(
                            Rectangle((x - 0.5, y - 0.5), 1, 1, color="black")
                        )
                    )

    def update(self, step, scores, event, teams, attack_ranges, prev_positions, positions, statuses, actions, broken_positions):
        """
        Simulation.py の引数順序に合わせて受け取り
        """
        artists = list(self.static_artists)

        # ===== イベント (★) =====
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

        # ===== 攻撃エフェクト (移動前座標 prev_positions を起点) =====
        for pos_before, action, team, attack_range in zip(prev_positions, actions, teams, attack_ranges):
            color = TEAM_COLORS.get(team, "green")
            artists += self.draw_attack(pos_before, action, color, attack_range)

        # ===== やられエフェクト（✖を表示） =====
        # broken_positions は [None, [x, y], None, ...] のような形式
        for pos in broken_positions:
            if pos is not None and pos[0] >= 0:
                artists.append(
                    self.ax.text(
                        pos[0], pos[1], "✖",
                        ha="center", va="center",
                        fontsize=25, color="black",
                        fontweight="bold", zorder=5
                    )
                )

        # ===== エージェントの描画（無敵エフェクト付き） =====
        cell_groups = defaultdict(list)
        for pos, team in zip(positions, teams):
            if pos[0] >= 0:
                cell_groups[tuple(pos)].append(team)

        cell_count = defaultdict(int)
        for i, (pos, team, status) in enumerate(zip(positions, teams, statuses)):
            if pos[0] < 0:
                continue
            
            key = tuple(pos)
            n = len(cell_groups[key])
            idx = cell_count[key]
            cell_count[key] += 1
            
            offset = (idx - (n - 1) / 2) * 0.25
            color = TEAM_COLORS.get(team, "green")
            
            # ===== 無敵状態なら金色の太枠を表示 =====
            edge_color = "none"
            line_width = 0
            if status == "invincible":
                edge_color = "gold"
                line_width = 3

            artists.append(
                self.ax.add_patch(
                    Circle(
                        (pos[0] + offset, pos[1]),
                        0.25,
                        color=color,
                        ec=edge_color,
                        lw=line_width,
                        zorder=4
                    )
                )
            )

        # ===== スコア表示 =====
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
        if pos[0] < 0 or action is None or action < 4 or action > 7:
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
            if not (0 <= nx < self.grid_size and 0 <= ny < self.grid_size):
                break
            if self.map[ny][nx] == "#":
                break
            end_x, end_y = nx, ny

        if end_x == x and end_y == y:
            return []

        return [
            self.ax.plot(
                [x, end_x], [y, end_y],
                color=color, linewidth=4, alpha=0.6, zorder=2
            )[0]
        ]

    def save(self, path="result.gif"):
        ani = animation.ArtistAnimation(
            self.fig, self.frames, interval=400, repeat=False
        )
        ani.save(path, writer="pillow")
        plt.close()