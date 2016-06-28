from .GPUtil.gp_evolution import start_evolution
from threading import Thread
from .Agents.bot import *
from .Agents.greedy_agent import GreedyAgent
from threading import Thread

POPULATION_SIZE = 30
NUM_OF_GENERATIONS = 71

server_list = [('localhost', 8037),
               ('localhost', 8038),
               ('localhost', 8039),
               ('localhost', 8040),
               ('localhost', 8041),
               ('localhost', 8042)]

players = [('GAL', '3', GreedyAgent('GAL'), 'localhost', 8037),
           ('DINA', '2', GreedyAgent('DINA'), 'localhost', 8037),
           ('GAL', '3', GreedyAgent('GAL'), 'localhost', 8038),
           ('DINA', '2', GreedyAgent('DINA'), 'localhost', 8038),
           ('GAL', '3', GreedyAgent('GAL'), 'localhost', 8039),
           ('DINA', '2', GreedyAgent('DINA'), 'localhost', 8039),
           ('DINA', '2', GreedyAgent('DINA'), 'localhost', 8040),
           ('GAL', '3', GreedyAgent('GAL'), 'localhost', 8041)]

# 8037 : has all 3
# 8038 : has all 3
# 8039 : has all 3
# 8040 : has one greedy and one outsider
# 8041 : has one greedy and one outsider
# 8042 : has one outsider

def start_player(user, password, agent, host, port):
    b = Bot(user, password, agent)
    b.connect_and_listen(host, port)

for (user, password, agent, host, port) in players:
    t = Thread(target=start_player, args=[user, password, agent, host, port])
    t.start()

# start evolution thread
e = Thread(target=start_evolution, args=[server_list, POPULATION_SIZE, NUM_OF_GENERATIONS, "generation_29.pickle"])
e.start()