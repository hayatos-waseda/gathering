class MapLoader:
    @staticmethod
    def load_map(path):
        grid = []
        with open(path, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    grid.append(list(line))
        return grid

    @staticmethod
    def build_field_from_map(grid):
        h = len(grid)
        w = len(grid[0])

        field = [[[0,0,0,0] for _ in range(h)] for _ in range(w)]

        for x in range(w):
            for y in range(h):

                if grid[y][x] == "#":
                    continue

                if y+1 < h and grid[y+1][x] != "#":
                    field[x][y][0] = 1
                if x+1 < w and grid[y][x+1] != "#":
                    field[x][y][1] = 1
                if y-1 >= 0 and grid[y-1][x] != "#":
                    field[x][y][2] = 1
                if x-1 >= 0 and grid[y][x-1] != "#":
                    field[x][y][3] = 1

        return field