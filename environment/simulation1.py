# simulation/simulation1.py

from environment.map_loader import MapLoader
from environment.field2 import Field
from agent.agent_a import AgentA
from agent.agent_b import AgentB
from renderer.gif_maker import GIFMaker

import yaml
import random


class Simulation1:

    @staticmethod
    def start(config_path="config/simulation.yaml"):

        # ===== config読み込み =====
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)

        max_step = config["max_step"]
        seed_num = config["seed"]

        rnd = random.Random(seed_num)

        # ===== 環境 =====
        grid = MapLoader.load_map(config["environment"]["map_path"])
        f1 = Field(rnd, grid, config["environment"])

        # ===== Agentクラス対応表 =====
        AGENT_MAP = {
            "AgentA": AgentA,
            "AgentB": AgentB,
        }

        # ===== エージェント生成 =====
        agents = []
        for conf in config["agents"]:
            cls = AGENT_MAP[conf["type"]]

            agent = cls(
                rnd,
                f1,
                conf["start_pos"]
            )

            agents.append({
                "name": conf["name"],
                "team": conf["team"],
                "obj": agent,
                "score": 0
            })

        # ===== renderer =====
        render_mode = config["render"]["mode"]

        if render_mode == "gif":
            gif = GIFMaker(grid)

        # ===== メインループ =====
        for time in range(max_step):

            # --- イベント発生 ---
            f1.happen_event(rnd)

            # ===== 行動決定 =====
            actions = []

            for a in agents:
                agent = a["obj"]

                if agent.can_act(time, rnd):

                    # 敵の位置リスト
                    enemy_positions = [
                        b["obj"].get_pos()
                        for b in agents
                        if b["team"] != a["team"]
                    ]

                    action = agent.action(enemy_positions)

                else:
                    action = 8  # 何もしない

                actions.append(action)

            # ===== 移動 =====
            for i, a in enumerate(agents):
                if actions[i] < 4:
                    a["obj"].move(actions[i])

            # ===== 攻撃 =====
            hits = [0] * len(agents)

            for i, a in enumerate(agents):
                if actions[i] >= 4 and actions[i] < 8:
                    for j, b in enumerate(agents):

                        # 敵のみ対象
                        if a["team"] != b["team"]:
                            hit = a["obj"].attack(
                                actions[i],
                                b["obj"].get_pos()
                            )

                            if hit:
                                b["obj"].broken(time)
                                hits[i] = 1

            # ===== 位置取得 =====
            positions = [a["obj"].get_pos() for a in agents]

            # ===== 報酬処理 =====
            for i, a in enumerate(agents):
                pos = positions[i]

                # 無効位置
                if pos[0] == -1:
                    continue

                # 同マス判定
                same_cell = sum(1 for p in positions if p == pos) > 1

                if same_cell:
                    f1.acquire_event(pos[0], pos[1])
                else:
                    if a["obj"].get_status() != "broken":
                        a["score"] += f1.acquire_event(pos[0], pos[1])

            # ===== 描画 =====
            if render_mode == "gif" and time <= 100:
                gif.update(
                    step=time,
                    scores=[a["score"] for a in agents],
                    event=f1.event,
                    positions=positions,
                    actions=actions,
                    teams=[a["team"] for a in agents]
                )

        # ===== 保存 =====
        if render_mode == "gif":
            gif.save(config["render"]["output"])

        # ===== 確率表示 =====
        print("=== Reward Table ===")
        f1.show_p()

        # ===== 結果出力 =====
        print("=== RESULT ===")
        for a in agents:
            print(f'{a["name"]} (Team {a["team"]}): {a["score"]}')