# simulation/simulation1.py

from environment.map_loader import MapLoader
from agent.agent_a import AgentA
from agent.agent_b import AgentB
from environment.field1 import Field1
from renderer.gif_maker import GIFMaker


import yaml
import random


class Simulation1:

    @staticmethod
    def start(config_path="config/simulation.yaml"):

        with open(config_path, "r") as f:
            config = yaml.safe_load(f)

        max_step = config["max_step"]
        seed_num = config["seed"]
        rnd = random.Random(seed_num)

        grid = MapLoader.load_map(config["environment"]["map_path"])

        f1 = Field1(rnd, grid)
        pos1 = config["agents"]["player1"]["start_pos"]
        pos2 = config["agents"]["player2"]["start_pos"]

        player1 = AgentA(rnd, f1, pos1)
        player2 = AgentB(rnd, f1, pos2)


        render_mode = config["render"]["mode"]
        if render_mode == "gif":
            gif = GIFMaker(grid)

        score1 = 0
        score2 = 0

        # ステップループ
        for time in range(max_step):

            # イベント発生
            f1.happen_event(rnd)

            # 行動決定
            action1 = 8
            action2 = 8

            if player1.can_act(time, rnd):
                action1 = player1.action(player2.get_pos())

            if player2.can_act(time, rnd):
                action2 = player2.action(player1.get_pos())

            # 移動
            if action1 < 4:
                player1.move(action1)
            if action2 < 4:
                player2.move(action2)

            # 攻撃
            hit1 = 0
            hit2 = 0

            if action1 >= 4:
                hit1 = player1.attack(action1, player2.get_pos())

            if action2 >= 4:
                hit2 = player2.attack(action2, player1.get_pos())

            # 破壊処理
            if hit1 != 0:
                player2.broken(time)

            if hit2 != 0:
                player1.broken(time)

            pos1 = player1.get_pos()
            pos2 = player2.get_pos()

            # 報酬処理
            if pos1[0] == pos2[0] and pos1[1] == pos2[1] and pos1[0] != -1:
                f1.acquire_event(pos1[0], pos1[1])
            else:
                if player1.get_status() != "broken":
                    score1 += f1.acquire_event(pos1[0], pos1[1])

                if player2.get_status() != "broken":
                    score2 += f1.acquire_event(pos2[0], pos2[1])

            # ログ
            # print(f"action player1: {action1}, player2: {action2}")
            # print(f"position player1: ({player1.get_pos()[0]},{player1.get_pos()[1]}), "
            #     f"player2: ({player2.get_pos()[0]},{player2.get_pos()[1]})")
            # print(f"score player1: {score1}, player2: {score2}")
            # print()

            if render_mode == "gif" and time <= 100:
                gif.update(
                    step=time,
                    score1=score1,
                    score2=score2,
                    event=f1.event,
                    pos1=pos1,
                    pos2=pos2,
                    action1=action1,
                    action2=action2
                )
        
        if render_mode == "gif":
            gif.save("results.gif")
        
        f1.show_p()
        
        