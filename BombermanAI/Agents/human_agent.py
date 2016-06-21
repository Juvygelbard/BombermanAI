from .bot import Agent
from msvcrt import getch
from queue import Queue
from threading import Thread

class HumanAgent(Agent):
    def __init__(self):
        self.key_to_command = {bytes('w', encoding='UTF-8'):'UP',
                               bytes('s', encoding='UTF-8'):'DOWN',
                               bytes('a', encoding='UTF-8'):'LEFT',
                               bytes('d', encoding='UTF-8'):'RIGHT',
                               bytes(' ', encoding='UTF-8'):'BOMB'}
        self.key_q = Queue()
        self.t = Thread(target=self.key_listener)
        self.t.start()

    def init_game(self):
        self.key_q = Queue()
        return True

    def end_game(self, players):
        pass

    def next_move(self, map, players, bombs):
        # get a move frm queue
        if(not self.key_q.empty()):
            n_move = self.key_q.get(block=False)
            return "ACTION " + n_move
        else:
            return False

    def key_listener(self):
        while(True):
            key = getch()
            self.key_q.put(self.key_to_command[key])