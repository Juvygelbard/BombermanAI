from ..Agents.bot import Bot
from .genome import Genome, TERMINALS, NODES
from ..Agents.gp_agent import GP_Agent
from queue import Queue

INIT_TREE_MAX_DEPTH = 3
PLAYER_NAME = 'ALLAHU_AKBAR'
PLAYER_PASS = 'ALLAHU_AKBAR'

def generate_random_pop(n, max_depth):
    ans = []
    for i in range(n):
        ans.append(Genome(max_depth, NODES, TERMINALS))

def start_evolution(pop_size, generations, mutation_prob=0.1, elitism=2):
    pop = generate_random_pop(pop_size, INIT_TREE_MAX_DEPTH)

    print("started")
    for g in range(generations):
        for gen in pop:
            agent = GP_Agent(PLAYER_NAME, gen)
            bot = Bot(PLAYER_NAME, PLAYER_PASS, agent)
            score = bot.connect_and_listen()
            print(str(score))

            # Keep score in data structure after every cenome run
            # At the end of each generation, process the population with mutation and xover
            # and then move to next gen with new population