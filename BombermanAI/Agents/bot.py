import socket

SERVER_IP = 'localhost'
SERVER_PORT = 8037

BOMB_TICKS = 5
EXPLOSION_RADIUS = 3

class Connection:
    def __init__(self, host, port):
        self.s = socket.socket()
        self.s.connect((host, port))

    def send_line(self, line):
        self.s.send(bytes(line, 'utf-8'))

    def get_line(self):
        buffer = ""

        while True:
            c = self.s.recv(1).decode('utf-8')
            if c == '\n' or c == '':
                break
            buffer += c

        return buffer

import numpy

class Player:
    def __init__(self, name, x, y):
        self.name = name
        self.score = 0
        self.x = x
        self.y = y
        self.status = 'ALIVE'

    def move(self, dir, map, bombs):
        height = len(map)
        width = len(map[0])
        n_map = numpy.add(map, bombs)

        if dir=='UP' and self.y>0 and n_map[self.y-1][self.x]==0:
            self.y -= 1
        elif dir=='DOWN' and self.y<height-1 and n_map[self.y+1][self.x]==0:
            self.y += 1
        elif dir=='LEFT' and self.x>0 and n_map[self.y][self.x-1]==0:
            self.x -= 1
        elif dir=='RIGHT' and self.x<width-1 and n_map[self.y][self.x+1]==0:
            self.x +=1

    def kill(self):
        self.status = 'DEAD'

    def set_score(self, score):
        self.score = score

class Bot:
    def __init__(self, user, password, agent):
        self.user = user
        self.password = password
        self.agent = agent
        self.alive = False
        self.players_s = {}
        self.map_s = None
        self.parse_table = {'INIT' :self.init,
                            'MAP' : self.map,
                            'PLAYERS' : self.players,
                            'TICK' : self.tick,
                            'ACTIONS' : self.actions,
                            'DEAD' : self.dead,
                            'END' : self.end,
                            'SCORES' : self.scores,
                            'REGISTERED' : self.registered,
                            'LEFT' : self.conf,
                            'RIGHT' : self.conf,
                            'UP' : self.conf,
                            'DOWN' : self.conf,
                            'BOMB' : self.conf,
                            'E_INVALID_ACTION' : self.error_handling,
                            'E_TOO_MANY_ACTIONS' : self.error_handling,
                            'E_NOT_PLAYING' : self.error_handling,
                            'E_NOT_INIT' : self.error_handling,
                            'E_WRONG_PASS' : self.error_handling}
        self.run_bot = True
        self.ret_val = None

    def error_handling(self, args): # TODO: handle server errors!
        print(self.user + " " + args[0])

    # start connection with server
    def connect_and_listen(self):
            self.conn = Connection(SERVER_IP, SERVER_PORT)
            while self.run_bot:
                msg = self.conn.get_line()
                s_msg = msg.split()
                self.parse_table[s_msg[0]](s_msg)

            return self.ret_val


    # init game := register player
    def init(self, args):
        ready = self.agent.init_game()
        if(ready):
            self.conn.send_line("REGISTER " + self.user + " " + self.password)

    # got confirmation for registration, game starts
    def registered(self, args):
        print("Registered as " + self.user)
        self.alive = True

    # getting a new map from server
    def map(self, args):
        # get map dimensions
        self.height = int(args[1])
        self.width = int(args[2])
        # init bomb and map
        self.bombs = [[0 for x in range(self.width)] for y in range(self.height)]
        self.map_s = []
        for y in range(self.height):
            row = self.conn.get_line().split()
            self.map_s.append([int(x) for x in row])

    # getting players list and initial positions from server
    def players(self, args):
        self.players_s = {}
        for i in range(int(args[1])):
            raw = self.conn.get_line().split()
            self.players_s.update({raw[0]: Player(raw[0], int(raw[2]), int(raw[1]))})

    # play current turns
    def tick(self, args):
        # advance bombs
        self.advance_bombs()

        # preform action
        if(self.alive):
            move = self.agent.next_move(self.map_s, self.players_s, self.bombs)
            if(move):
                self.conn.send_line(move)

    # advance bomb ticks and blow-up on time
    def advance_bombs(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.bombs[y][x] > 0:
                    self.bombs[y][x] -= 1
                    if self.bombs[y][x]==0:
                        # explode if bomb hits 0
                        self.expolsion(x, y)

    # get a list of players actions and update game state
    def actions(self, args):
        for x in range(int(args[1])):
            p_act = self.conn.get_line().split()
            if p_act[1]=='BOMB':
                b_x = self.players_s[p_act[0]].x
                b_y = self.players_s[p_act[0]].y

                # init bomb countdown
                if self.bombs[b_y][b_x]==0:
                    self.bombs[b_y][b_x] = BOMB_TICKS + 1
            else:
                self.players_s[p_act[0]].move(p_act[1], self.map_s, self.bombs)

    # get list of dead players
    def dead(self, args):
        for x in range(int(args[1])):
            player = self.conn.get_line()
            self.players_s[player].kill()
            if(player==self.user):
                self.alive = False

    # end game
    def end(self, args):
        self.alive = False

    # update scores
    def scores(self, args):
        for x in range(int(args[1])):
            score = self.conn.get_line().split()
            self.players_s[score[0]].set_score(int(score[1]))

        # send players with scores to agent
        stop_bot = self.agent.end_game(self.players_s)
        if stop_bot != None:
            self.run_bot = False
            self.ret_val = stop_bot

    # get a confirmation of player's action
    def conf(self, args):
        dic = {'LEFT' : "moved left.",
               'RIGHT' : "moved right",
               'UP' : "moved up",
               'DOWN' : "moved down",
               'BOMB' : "placed a bomb."}

        print(self.user + " " + dic[args[0]])

    # simulate explosion for a given map and x, y coordinates
    def expolsion(self, x, y):
        UP, DOWN, LEFT, RIGHT = True, True, True, True

        # modify map in case of explosion
        for d in range(1, EXPLOSION_RADIUS+1):
            # modify up
            if RIGHT and x+d < self.width and self.map_s[y][x+d]!=0:
                RIGHT = False
                if self.map_s[y][x+d]==1:
                    self.map_s[y][x+d]=0
            # modify down
            if LEFT and x-d >= 0 and self.map_s[y][x-d]!=0:
                LEFT = False
                if self.map_s[y][x-d]==1:
                    self.map_s[y][x-d]=0
            # modify right
            if DOWN and y+d < self.height and self.map_s[y+d][x]!=0:
                DOWN = False
                if self.map_s[y+d][x]==1:
                    self.map_s[y+d][x]=0
            # modify left
            if UP and y-d >= 0 and self.map_s[y-d][x]!=0:
                UP = False
                if self.map_s[y-d][x]==1:
                    self.map_s[y-d][x]=0

# abstract class represents an agent
class Agent:
    def init_game(self):
        raise NotImplementedError("init_game")

    def next_move(self, map, players, bombs):
        raise NotImplementedError("next_move")

    def end_game(self, players):
        raise NotImplementedError("end_game")