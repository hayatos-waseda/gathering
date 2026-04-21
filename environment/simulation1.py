# simulation/simulation1.py

from environment.map_loader import MapLoader
from environment.field1 import Field1 as Field
from environment.field_view import FieldView
from renderer.gif_maker import GIFMaker

import yaml
import random


class Simulation:

    @staticmethod
    def start(config_path, agent_a, agent_b):
        config_path="config/simulation.yaml"
        AgentA = agent_a
        AgentB = agent_b

        # ===== config読み込み =====
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)

        max_step = config["max_step"]
        seed_num = config["seed"]

        rnd = random.Random(seed_num)

        # ===== 環境 =====
        field = Field(rnd, config["environment"])
        field_view = FieldView(field)
        grid = field.grid

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
                field_view,
                conf["start_pos"],
            )

            agents.append({
                "name": conf["name"],
                "team": conf["team"],
                "obj": agent,
                "score": 0,
                "attack_count": 0,
                "broken_count": 0
            })

        # ===== renderer =====
        render_mode = config["render"]["mode"]

        if render_mode == "gif":
            gif = GIFMaker(grid)

        # ===== メインループ =====
        for time in range(max_step):

            # --- イベント発生 ---
            field.happen_event(rnd)

            # ===== 行動決定 =====
            actions = []

            for a in agents:
                agent = a["obj"]

                if agent.can_act(time, rnd):

                    ally_data = [
                        {"pos": b["obj"].get_pos(), "status": b["obj"].get_status()}
                        for b in agents
                        if b["team"] == a["team"] and b["name"] != a["name"]
                    ]
                    enemy_data = [
                        {"pos": b["obj"].get_pos(), "status": b["obj"].get_status()}
                        for b in agents if b["team"] != a["team"]
                    ]

                    action = agent.action(ally_data,enemy_data)

                else:
                    action = 8  # 何もしない

                actions.append(action)

            # ===== 攻撃 =====
            broken_flags = [False]*len(agents)

            for i, a in enumerate(agents):
                if actions[i] >= 4 and actions[i] < 8:
                    for j, b in enumerate(agents):
                        if i != j:
                            hit = a["obj"].attack(
                                actions[i],
                                b["obj"].get_pos()
                            )

                            if hit:
                                broken_flags[j] = True
                                a["attack_count"] += 1

            for j, b in enumerate(agents):
                if broken_flags[j]:
                    b["obj"].broken(time)
                    b["broken_count"] += 1
            
            # ===== 移動 =====
            for i, a in enumerate(agents):
                if actions[i] < 4 and a["obj"].get_status() == "active":
                    a["obj"].move(actions[i])


            # ===== 位置取得 =====
            positions = [a["obj"].get_pos() for a in agents]

            # ===== 報酬処理 =====
            for i, a in enumerate(agents):
                pos = positions[i]

                # 無効位置
                if a["obj"].get_status() == "broken":
                    continue

                # 同マス判定
                same_cell = positions.count(pos) > 1

                if same_cell:
                    field.acquire_event(pos[0], pos[1])
                else:
                    a["score"] += field.acquire_event(pos[0], pos[1])

            # ===== 描画 =====
            if render_mode == "gif" and time <= 100:
                gif.update(
                    step=time,
                    scores=[a["score"] for a in agents],
                    event=field.event,
                    positions=positions,
                    actions=actions,
                    teams=[a["team"] for a in agents],
                    attack_ranges =[a["obj"].attack_range for a in agents]
                )

        # ===== 保存 =====
        if render_mode == "gif":
            gif.save(config["render"]["output"])

        # ===== 確率表示 =====
        print("=== Reward Table ===")
        field.show_p()

        # ===== 結果出力 =====
        print("=== RESULT ===")
        for a in agents:
            print(f'{a["name"]} (Team {a["team"]}):')
            print(f'  {"Score:":<15} {a["score"]:>5}')
            print(f'  {"Attack Success:":<15} {a["attack_count"]:>5}')
            print(f'  {"Broken:":<15} {a["broken_count"]:>5}')
