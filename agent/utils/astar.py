# agent/utils/astar.py

import heapq


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def Astar(field_view, start, goal):

    start = tuple(start)
    goal = tuple(goal)

    if start == goal:
        return [list(start)]

    # (f, g, pos)
    open_set = []
    heapq.heappush(open_set, (0, 0, start))

    came_from = {}
    g_score = {start: 0}

    directions = [
        (0,  1),   # 0: 上
        (1,  0),   # 1: 右
        (0, -1),   # 2: 下
        (-1, 0),   # 3: 左
    ]

    while open_set:
        _, g, current = heapq.heappop(open_set)
        if g > g_score.get(current, float('inf')):
            continue

        if current == goal:
            path = []
            while current in came_from:
                path.append(list(current))
                current = came_from[current]
            path.append(list(start))
            path.reverse()
            return path

        for act, (dx, dy) in enumerate(directions):
            if field_view.get_pos_status(current[0], current[1], act) != 1:
                continue

            neighbor = (current[0] + dx, current[1] + dy)
            new_g = g + 1

            if neighbor not in g_score or new_g < g_score[neighbor]:
                g_score[neighbor] = new_g
                f = new_g + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f, new_g, neighbor))
                came_from[neighbor] = current

    return []  # 経路なし
