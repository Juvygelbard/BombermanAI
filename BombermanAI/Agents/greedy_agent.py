from .bot import Agent, EXPLOSION_RADIUS
from queue import Queue
from random import sample

class GreedyAgent(Agent):
    def __init__(self, name):
        self.name = name

    def init_game(self):
        pass

    def end_game(self, players):
        pass

    def next_move(self, map, players, bombs):
        # get my pos
        x_pos = players[self.name].x
        y_pos = players[self.name].y

        # get board size
        h = len(map)
        w = len(map[0])

        # define marks for other players
        marks = ['A', 'B', 'C', 'D', 'E', 'G']

        # deep copy
        map_plus = [[x for x in y] for y in map]

        # add bombs to map
        for y in range(h):
            for x in range(w):
                if bombs[y][x]:
                    map_plus[y][x] = 'X'

        # look for nearby bombs
        if self.in_danger(map_plus, x_pos, y_pos):
            # if in range, look for a safe place
            dist, path = self.bfs(map_plus, x_pos, y_pos, lambda map, x, y: not self.in_danger(map, x, y),
                                  lambda map, x, y: map[y][x]==0,
                                  limit=5)
            if path:
                dir = sample(path, 1)[0]
                return "ACTION " + dir

        # find empty space around me
        dirs = self.find_around_me(map_plus, lambda map, x, y: map[y][x]==0, x_pos, y_pos)

        # add players to map
        for (player, mark) in zip(players.values(), marks):
            if player.status == 'ALIVE':
                x, y = player.x, player.y
                map_plus[y][x] = mark

        # find nearest player and a safe root
        # higher priority - clear path
        dist, path = self.bfs(map_plus, x_pos, y_pos, lambda map, x, y: map[y][x] in marks,
                              lambda map, x, y: map[y][x] in marks + [0] and not self.in_danger(map, x, y))
        if dist and dist==1:
            return "ACTION BOMB"
        path.intersection_update(dirs)
        if path:
            dir = sample(path, 1)[0]
            return "ACTION " + dir

        # lower priority - blocked path
        dist, path = self.bfs(map_plus, x_pos, y_pos, lambda map, x, y: map[y][x] in marks,
                              lambda map, x, y: map[y][x] in marks + [0, 1] and not self.in_danger(map, x, y))
        path.intersection_update(dirs)
        if path:
            dir = sample(path, 1)[0]
            return "ACTION " + dir

        # way is blocked- drop a bomb only if you have somewhere to run
        dist, path = self.bfs(map_plus, x_pos, y_pos, lambda map, x, y: not self.in_danger(map, x, y),
                                  lambda map, x, y: map[y][x] in [0] + marks and not self.in_danger(map, x, y),
                                  limit=5)
        if path:
            return "ACTION BOMB"

        # nothing to else do
        return False

    def find_around_me(self, map, allowed, x, y):
        # get board size
        h = len(map)
        w = len(map[0])

        # find optional moves
        dir = set()
        if y-1>=0 and allowed(map, x, y-1):
            dir.update({'UP'})
        if y+1<h and allowed(map, x, y+1):
            dir.update({'DOWN'})
        if x-1>=0 and allowed(map, x-1, y):
            dir.update({'LEFT'})
        if x+1<w and allowed(map, x+1, y):
            dir.update({'RIGHT'})

        return dir

    def bfs(self, map, x, y, stop, allowed, limit=False):
        # init ans
        ans = set()
        # copy_map
        map_w = [[x for x in y] for y in map]

        # build initial queue
        q = Queue()
        init_dirs = self.find_around_me(map_w, allowed, x, y)
        if 'LEFT' in init_dirs:
            q.put((x-1, y, 1, 'LEFT'))
        if 'RIGHT' in init_dirs:
            q.put((x+1, y, 1, 'RIGHT'))
        if 'UP' in init_dirs:
            q.put((x, y-1, 1, 'UP'))
        if 'DOWN' in init_dirs:
            q.put((x, y+1, 1, 'DOWN'))
        map_w[y][x] = 'v'

        # begin bfs
        while(not q.empty()):
            # get next node to inspect
            curr = q.get(block=False)
            n_x = curr[0]
            n_y = curr[1]
            d =  curr[2]
            i_dir = curr[3]
            # stop if reached limit
            if limit and d>limit:
                return limit-1, ans
            # found what I'm looking for
            if stop(map_w, n_x, n_y):
                ans.update({i_dir})
                limit = d+1
            # mark curr as visited
            map_w[n_y][n_x] = 'v'
            # keep looking around
            dirs = self.find_around_me(map_w, allowed, n_x, n_y)
            if 'LEFT' in dirs:
                q.put((n_x-1, n_y, d+1, i_dir))
            if 'RIGHT' in dirs:
                q.put((n_x+1, n_y, d+1, i_dir))
            if 'UP' in dirs:
                q.put((n_x, n_y-1, d+1, i_dir))
            if 'DOWN' in dirs:
                q.put((n_x, n_y+1, d+1, i_dir))

        # finished looking, didn't find
        return False, ans

    # expects to get a map with bombs and with no players
    # looks for bombs near-by
    def in_danger(self, map, x, y):
        # check if I'm standing on a bomb
        if map[y][x]=='X':
            return True

        # calculate map height an width
        h = len(map)
        w = len(map[0])

        # check other locations
        UP, DOWN, LEFT, RIGHT = True, True, True, True
        for d in range(1, EXPLOSION_RADIUS+1):
            if UP and y-d>=0:
                if map[y-d][x]=='X':
                    return True
                if map[y-d][x] not in [0, 'v']:
                    UP = False
            if DOWN and y+d<h:
                if map[y+d][x]=='X':
                    return True
                if map[y+d][x] not in [0, 'v']:
                    DOWN = False
            if LEFT and x-d>=0:
                if map[y][x-d]=='X':
                    return True
                if map[y][x-d] not in [0, 'v']:
                    LEFT = False
            if RIGHT and x+d<w:
                if map[y][x+d]=='X':
                    return True
                if map[y][x+d] not in [0, 'v']:
                    RIGHT = False
        # no bomb found
        return False