# simulation/simulation1.py

from environment.map_loader import MapLoader
from environment.field1 import Field1 as Field
from environment.field_view import FieldView
from renderer.gif_maker import GIFMaker
from agent.agent_a import AgentA
from agent.agent_b import AgentB

#自由にCommanderを作ってimportしてもよい
from agent.commander_a import CommanderA
from agent.commander_b import CommanderB


import yaml
import random


class Simulation:

    @staticmethod
    def start(config_path):
        config_path="config/simulation.yaml"

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

        # ===== Commander生成 =====
        commanders = {
            "A": CommanderA(rnd, field_view),
            "B": CommanderB(rnd, field_view),
        }
        team_indices = {}
        for i, a in enumerate(agents):
            team_indices.setdefault(a["team"], []).append(i)

        # ===== renderer =====
        render_mode = config["render"]["mode"]

        if render_mode == "gif":
            gif = GIFMaker(grid)

        # ===== メインループ =====
        for time in range(max_step):

            # --- イベント発生 ---
            field.happen_event(rnd)

            prev_positions = [a["obj"].get_pos()[:] for a in agents]

            can_act_flags = [
                agents[i]["obj"].can_act(time, rnd)
                for i in range(len(agents))
            ]

            # ===== 行動決定 =====
            actions = [8] * len(agents)  # デフォルトは停止

            for team, indices in team_indices.items():
                commander = commanders[team]

                team_data = [
                    {
                        "pos": agents[i]["obj"].get_pos(),
                        "status": agents[i]["obj"].get_status(),
                    }
                    for i in indices
                ]

                enemy_data = [
                    {
                        "pos": agents[j]["obj"].get_pos(),
                        "status": agents[j]["obj"].get_status(),
                    }
                    for j in range(len(agents))
                    if agents[j]["team"] != team
                ]

                decided = commander.decide(team_data, enemy_data)

                for k, i in enumerate(indices):
                    if can_act_flags[i]:
                        actions[i] = decided[k] if k < len(decided) else 8

            # ===== 移動 =====
            for i, a in enumerate(agents):
                if actions[i] < 4 and a["obj"].get_status() != "broken":
                    a["obj"].move(actions[i])

            # ===== 攻撃 =====
            hit_flags = [False]*len(agents)
            broken_positions = [None] * len(agents)

            for i, a in enumerate(agents):
                if actions[i] >= 4 and actions[i] < 8:
                    for j, b in enumerate(agents):
                        if i != j:
                            hit = a["obj"].attack(
                                actions[i],
                                b["obj"].get_pos()
                            )

                            if hit:
                                hit_flags[j] = True
                                a["attack_count"] += 1

            for j, b in enumerate(agents):
                if hit_flags[j]:
                    current_pos = b["obj"].get_pos()[:]
                    broken = b["obj"].broken(time)
                    if broken:
                        b["broken_count"] += 1
                        broken_positions[j] = current_pos

            # ===== 位置取得 =====
            positions = [a["obj"].get_pos() for a in agents]

            # ===== 報酬処理 =====
            for i, a in enumerate(agents):
                pos = positions[i]

                if a["obj"].get_status() == "broken":
                    continue

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
                    teams=[a["team"] for a in agents],
                    attack_ranges=[a["obj"].attack_range for a in agents],
                    prev_positions=prev_positions,
                    positions=positions,
                    statuses=[a["obj"].get_status() for a in agents],
                    actions=actions,
                    broken_positions=broken_positions
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