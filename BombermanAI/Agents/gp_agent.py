from .bot import Agent
from queue import Queue

EXPLOSION_RADIUS = 3

class GP_Agent(Agent):
    def __init__(self, name, genome):
        self.name = name
        self.genome = genome
        self.in_game = False
        self.marks = ['A', 'B', 'C', 'D', 'E']

    def init_game(self):
        self.in_game = True
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

        # calculating can move measures
        can_move_up = self.can_move(d_map, x_pos, y_pos, 0, -1)
        can_move_down = self.can_move(d_map, x_pos, y_pos, 0, 1)
        can_move_left = self.can_move(d_map, x_pos, y_pos, -1, 0)
        can_move_right = self.can_move(d_map, x_pos, y_pos, 1, 0)

        # calculating in-danger measures
        in_danger_up = self.in_danger(d_map, x_pos, y_pos, 0, -1)
        in_danger_down = self.in_danger(d_map, x_pos, y_pos, 0, 1)
        in_danger_left = self.in_danger(d_map, x_pos, y_pos, -1, 0)
        in_danger_right = self.in_danger(d_map, x_pos, y_pos, 1, 0)

        # calculating turn measure
        near_turn_up = self.dist_to_turn(d_map, x_pos, y_pos, 0, -1, "horizontal")
        near_turn_down = self.dist_to_turn(d_map, x_pos, y_pos, 0, 1, "horizontal")
        near_turn_left = self.dist_to_turn(d_map, x_pos, y_pos, -1, 0, "vertical")
        near_turn_right = self.dist_to_turn(d_map, x_pos, y_pos, 1, 0, "vertical")

        # add players to map
        for (m, p) in zip(self.marks, players.values()):
            d_map[p.y][p.x] = m

        # calculate distance to enemy measure
        dist_enemy_up = self.nearest_enemy(d_map, x_pos, y_pos, 0, -1)
        dist_enemy_down = self.nearest_enemy(d_map, x_pos, y_pos, 0, 1)
        dist_enemy_left = self.nearest_enemy(d_map, x_pos, y_pos, -1, 0)
        dist_enemy_right = self.nearest_enemy(d_map, x_pos, y_pos, 1, 0)

        # find if enemy in range measure
        enemy_in_range = self.enemy_in_range(d_map, x_pos, y_pos)

        # build measures dict
        measures = {"CanMove_UP" : can_move_up,
                    "CanMove_DN" : can_move_down,
                    "CanMove_LT" : can_move_left,
                    "CanMove_RT" : can_move_right,
                    "EnemyDist_UP" : dist_enemy_up,
                    "EnemyDist_DN" : dist_enemy_down,
                    "EnemyDist_LT" : dist_enemy_left,
                    "EnemyDist_RT" : dist_enemy_right,
                    "EnemyInRange" : enemy_in_range,
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
                    # print (self.name + " NOT MOVING")
                    return False
                else:
                    return 'ACTION ' + m

    def can_move(self, map, x, y, d_x, d_y):
        if 0<=y+d_y<len(map) and 0<=x+d_x<len(map[0]) and map[y+d_y][x+d_x]==0:
            return 1
        else:
            return 0

    def in_danger(self, map, x, y, d_x, d_y):
        for i in range(1, EXPLOSION_RADIUS+1):
            if y+d_y*i<0 or y+d_y*i>=len(map) or x+d_x*i<0 or x+d_x*i>=len(map[0]): # end of map
                return 0
            elif map[y+d_y*i][x+d_x*i] in [1, 2]: # wall
                return 0
            elif map[y+d_y*i][x+d_x*i]=='X': # bomb
                return 1
        return 0 # nothing

    def enemy_in_range(self, map, x, y):
        up, down , left, right = True, True, True, True
        stop = [1, 2] + self.marks
        for i in range(1, EXPLOSION_RADIUS+1):
            if down:
                if y+i>=len(map) or map[y+i][x] in stop:
                    down = False
                elif map[y+i][x] in self.marks:
                    return 1
            if up:
                if y-i<0 or map[y-i][x] in stop:
                    up = False
                elif map[y-i][x] in self.marks:
                    return 1
            if right:
                if x+i<0 or map[y][x+i] in stop:
                    left = False
                elif map[y][x+i] in self.marks:
                    return 1
            if left:
                if x-i<0 or map[y][x-i] in stop:
                    left = False
                elif map[y][x-i] in self.marks:
                    return 1
        return 0 # nothing

    def dist_to_turn(self, map, x, y, d_x, d_y, turn):
        max_possible_dist = max(len(map), len(map[0]))
        for i in range(1, max_possible_dist):
            if y+d_y*i<0 or y+d_y*i >= len(map) or x+d_x*i<0 or x+d_x*i >= len(map[0]): # end of map
                return max_possible_dist
            elif map[y+d_y*i][x+d_x*i] in [1, 2]: # hit a wall
                return max_possible_dist
            elif turn=="horizontal":
                if x+1<len(map[0]) and map[y+d_y*i][x+1]==0: # turn right
                    return i
                elif x-1>=0 and map[y+d_y*i][x-1]==0: # turn left
                    return i
            elif turn=="vertical":
                if y+1<len(map) and map[y+1][x+d_x*i]==0: # turn down
                    return i
                elif y-1>=0 and map[y-1][x+d_x*i]==0: # turn up
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
        if y+d_y<0 or y+d_y>=len(map) or x+d_x<0 or x+d_x>=len(map[0]):
            return False

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

            dirs = self.around_me(d_map, curr_x, curr_y, walk+stop)
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

        return False

    def get_accessible_walls(self, map, x, y):
        ans = []

        # duplicate map
        d_map = [[xv for xv in y] for y in map]

        # init queue and start walls dfs
        q = Queue()
        q.put((x, y))
        while not q.empty():
            curr = q.get(block=False)
            curr_x, curr_y = curr[0], curr[1]

            # found a wall
            if d_map[curr_y][curr_x]==1:
                ans.append(curr)
            else:
                # find next step
                dirs = self.around_me(d_map, curr_x, curr_y, [0, 1] + self.marks)
                if 'UP' in dirs:
                    q.put((curr_x, curr_y-1))
                if 'DOWN' in dirs:
                    q.put((curr_x, curr_y+1))
                if 'LEFT' in dirs:
                    q.put((curr_x-1, curr_y))
                if 'RIGHT' in dirs:
                    q.put((curr_x+1, curr_y))

            # mark curr as visited
            d_map[curr_y][curr_x] = 'V'
        return ans

    def nearest_enemy(self, map, x, y, d_x, d_y):
        # duplicate map and init
        d_map = [[vx for vx in vy] for vy in map]
        dist = False

        while not dist:
            # find enemy
            dist = self.bfs(d_map, x, y, d_x, d_y, [0]+self.marks, self.marks)
            # didn't found? remove one layer of walls
            if not dist:
                walls = self.get_accessible_walls(d_map, x, y)
                for (w_x, w_y) in walls:
                    d_map[w_y][w_x] = 0
        return dist

    def end_game(self, players):
        if(self.in_game):
            if(len(players)>1):
                self.in_game = False
                return players[self.name].score / (len(players)-1) # normalize score