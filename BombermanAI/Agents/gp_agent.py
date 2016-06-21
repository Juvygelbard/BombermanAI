from .bot import Agent
from queue import Queue

EXPLOSION_RADIUS = 3

class GP_Agent(Agent):
    def __init__(self, name, genome):
        self.name = name
        self.genome = genome

    def init_game(self):
        return True

    def next_move(self, map, players, bombs):
        # get my position and map dimensions
        x_pos = players[self.name].x
        y_pos = players[self.name].y
        height = len(map)
        width = len(map[0])

        # duplicate map, add bombs
        d_map = [[x for x in y] for y in map]
        for y in range(height):
            for x in range(width):
                if bombs[y][x]:
                    d_map[y][x] = 'X'

        # calculating in-danger measures
        in_danger_up = self.in_danger(d_map, x_pos, y_pos, 0, -1)
        in_danger_down = self.in_danger(d_map, x_pos, y_pos, 0, 1)
        in_danger_left = self.in_danger(d_map, x_pos, y_pos, -1, 0)
        in_danger_right = self.in_danger(d_map, x_pos, y_pos, 1, 0)

        # calculating turn measure
        near_turn_up = self.dist_to_turn(d_map, x_pos, y_pos, 0, -1, "vertical")
        near_turn_down = self.dist_to_turn(d_map, x_pos, y_pos, 0, 1, "vertical")
        near_turn_left = self.dist_to_turn(d_map, x_pos, y_pos, -1, 0, "horizontal")
        near_turn_right = self.dist_to_turn(d_map, x_pos, y_pos, 1, 0, "horizontal")

        # add players to map
        marks = ['A', 'B', 'C', 'D', 'E']
        for (m, p) in zip(marks, players.values()):
            d_map[p.y][p.x] = m

        # calculate distance to enemy (no walls) measure
        dist_enemy_c_up = self.bfs(d_map, x_pos, y_pos, 0, -1, [0], marks)
        dist_enemy_c_down = self.bfs(d_map, x_pos, y_pos, 0, 1, [0], marks)
        dist_enemy_c_left = self.bfs(d_map, x_pos, y_pos, -1, 0, [0], marks)
        dist_enemy_c_right = self.bfs(d_map, x_pos, y_pos, 1, 0, [0], marks)

        # calculate distance to enemy (with walls) measure
        dist_enemy_w_up = self.bfs(d_map, x_pos, y_pos, 0, -1, [0, 1], marks)
        dist_enemy_w_down = self.bfs(d_map, x_pos, y_pos, 0, 1, [0, 1], marks)
        dist_enemy_w_left = self.bfs(d_map, x_pos, y_pos, -1, 0, [0, 1], marks)
        dist_enemy_w_right = self.bfs(d_map, x_pos, y_pos, 1, 0, [0, 1], marks)

        # build measures dict
        measures = {"NearEnemy_CLR_UP" : dist_enemy_c_up,
                    "NearEnemy_CLR_DN" : dist_enemy_c_down,
                    "NearEnemy_CLR_LT": dist_enemy_c_left,
                    "NearEnemy_CLR_RT": dist_enemy_c_right,
                    "NearEnemy_WALL_UP": dist_enemy_w_up,
                    "NearEnemy_WALL_DN" : dist_enemy_w_down,
                    "NearEnemy_WALL_LT" : dist_enemy_w_left,
                    "NearEnemy_WALL_RT" : dist_enemy_w_right,
                    "InDanger_UP" : in_danger_up,
                    "InDanger_DN" : in_danger_down,
                    "InDanger_LT" : in_danger_left,
                    "InDanger_RT" : in_danger_right,
                    "NearTurn_UP" : near_turn_up,
                    "NearTurn_DN" : near_turn_down,
                    "NearTurn_LT" : near_turn_left,
                    "NearTurn_RT" : near_turn_right}

        # find next move
        possible_moves = self.around_me(map, x_pos, y_pos, [0]) + ['BOMB', 'NONE']
        best_moves = self.genome.next_move(measures)

        for m in best_moves:
            if m in possible_moves:
                if m == 'NONE':
                    return False
                else:
                    return 'ACTION ' + m

    def in_danger(self, map, x, y, d_x, d_y):
        for i in range(1, EXPLOSION_RADIUS+1):
            if y+d_y*i<0 or y+d_y*i>=len(map) or x+d_x*i<0 or x+d_x*i>=len(map[0]): # end of map
                return 0
            elif map[y+d_y*i][x+d_x*i] in [1, 2]: # wall
                return 0
            elif map[y+d_y*i][x+d_x*i]=='X': # bomb
                return 1
        return 0 # nothing

    def dist_to_turn(self, map, x, y, d_x, d_y, turn):
        max_possible_dist = max(len(map), len(map[0]))
        for i in range(max_possible_dist):
            if 0<=y+d_y*i<len(map) and 0<=x+d_x*i<len(map[0]): # end of map
                return max_possible_dist
            elif map[y+d_y*i][x+d_x*i] in [1, 2]: # hit a wall
                return max_possible_dist
            elif turn=="horizontal":
                if x+d_x*i+1<len(map[0]) and map[y+d_y*i][x+d_x*i+1]==0: # turn right
                    return i
                elif x+d_x*i-1>=0 and map[y+d_y*i][x+d_x*i-1]==0: # turn left
                    return i
            elif turn=="vertical":
                if y+d_y*i+1<len(map) and map[y+d_y*i+1][x+d_x*i]==0: # turn down
                    return i
                elif y+d_y*i-1>=0 and map[y+d_y*i-1][x+d_x*i]==0: # turn up
                    return i
        return max_possible_dist

    def around_me(self, map, x, y, walk):
        ans = []
        if y-1>=0 and map[y-1][x] in walk:
            ans.append('UP')
        if y+1<len(map) and map[y+1][x] in walk:
            ans.append('DOWN')
        if x-1>=0 and map[y][x-1] in walk:
            ans.append('LEFT')
        if x+1<len(map[0]) and map[y][x+1] in walk:
            ans.append('RIGHT')
        return ans

    def bfs(self, map, x, y, d_x, d_y, walk, stop):
        q = Queue()
        # check if direction is legal
        max_possible_val = max(len(map), len(map[0]))
        if y+d_y<0 or y+d_y>=len(map) or x+d_x<0 or x+d_x>=len(map[0]):
            return max_possible_val
        # duplicate map and place me on map
        d_map = [[x for x in y] for y in map]
        d_map[y][x] = 'V'
        # push initial
        q.put((x+d_x, y+d_y, 1))
        # start bfs
        while not q.empty():
            # get next tile
            curr = q.get(block=False)
            curr_x, curr_y, d = curr[0], curr[1], curr[2]

            # found what I was looking for
            if d_map[curr_y][curr_x] in stop:
                return d

            dirs = self.around_me(d_map, curr_x, curr_y, walk)
            if 'UP' in dirs:
                q.put((curr_x, curr_y-1, d+1))
            if 'DOWN' in dirs:
                q.put((curr_x, curr_y+1, d+1))
            if 'LEFT' in dirs:
                q.put((curr_x-1, curr_y, d+1))
            if 'RIGHT' in dirs:
                q.put((curr_x+1, curr_y, d+1))

            # mark curr as visited
            d_map[curr_y][curr_x] = 'V'

        return max_possible_val

    def end_game(self, players):
        return players[self.name].score