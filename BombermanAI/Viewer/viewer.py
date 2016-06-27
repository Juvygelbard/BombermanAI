from queue import Queue
from ..Agents.bot import Agent, EXPLOSION_RADIUS
from .canvas import MainFrame

class Viewer(Agent):
    def __init__(self):
        self.blasts = []

    def next_move(self, map, players, bombs):
        # deep copy map
        map_n = [[x for x in y] for y in map]

        # get map height and width
        height = len(map_n)
        width = len(map_n[0])

        # put players marks on map
        player_marks = ['A', 'B', 'C', 'D', 'E']
        for mark, player in zip(player_marks, players.values()):
            if player.status=='ALIVE':
                map_n[player.y][player.x] = mark

        # display blasts
        for (x, y) in self.blasts:
            map_n[y][x] = '@'
        self.blasts = []

        # place bombs on map
        for y in range(height):
            for x in range(width):
                if bombs[y][x] != 0 and map_n[y][x] == 0:
                    map_n[y][x] = 'X'
                if bombs[y][x] == 1:
                    self.blasts += self.calc_blasts(x, y, map_n)

        # update displayed map
        self.update_map(map_n)
        return False

    def update_map(self, map):
        self.map_queue.put(map)

    def calc_blasts(self, x, y, map):
        ans = [(x, y)]
        up, down, left, right = True, True, True, True
        for d in range(1, EXPLOSION_RADIUS+1):
            if up:
                if y-d < 0:
                    up = False
                elif map[y-d][x] == 2:
                    up = False
                elif map[y-d][x] == 1:
                    ans.append((x, y-d))
                    up = False
                else:
                    ans.append((x, y-d))
            if down:
                if y+d >= len(map):
                    down = False
                elif map[y+d][x] == 2:
                    down = False
                elif map[y+d][x] == 1:
                    ans.append((x, y+d))
                    down = False
                else:
                    ans.append((x, y+d))
            if left:
                if x-d < 0:
                    left = False
                elif map[y][x-d] == 2:
                    left = False
                elif map[y][x-d] == 1:
                    ans.append((x-d, y))
                    left = False
                else:
                    ans.append((x-d, y))
            if right:
                if x+d >= len(map[0]):
                    right = False
                elif map[y][x+d] == 2:
                    right = False
                elif map[y][x+d] == 1:
                    ans.append((x+d, y))
                    right = False
                else:
                    ans.append((x+d, y))
        return ans

    def init_game(self):
        self.blasts = []
        self.map_queue = Queue()

    def end_game(self, players):
        pass