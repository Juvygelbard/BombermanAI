from ..Agents.bot import Bot
from .genome import Genome, TERMINALS, NODES
from ..Agents.gp_agent import GP_Agent
from random import random
from numpy.random import choice
from threading import Thread
from queue import Queue
import pickle

INIT_TREE_MAX_DEPTH = 3
GAMES_PER_GENERATION = 3
PLAYER_NAME = 'INDIVIDUAL'
PLAYER_PASS = 'JOHNKOZARULEZ'
PICKLE_NAME = 'generation_'

# creates initial population
def generate_random_pop(n, max_depth):
    ans = []
    for i in range(n):
        ans.append(Genome(max_depth, NODES, TERMINALS))
    return ans

# preforming rank selection: returns 2
def rank_selection(pop_size):
    total = sum(range(pop_size+1))
    prob = [(1+i)/total for i in range(pop_size)]
    prob.reverse() # lowest index has a better score and gets a higher probability
    parents = choice(pop_size, 2, replace=False, p=prob)
    return parents[0], parents[1]

def play_individual(server, port, genome_q, server_q, result_q):
    curr = genome_q.get(block=True)
    gen, ind, genome = curr[0], curr[1], curr[2]
    name = PLAYER_NAME + "_" + str(gen) +"_" + str(ind)
    password = PLAYER_PASS

    agent = GP_Agent(name, genome)
    score = 0
    for game in range(GAMES_PER_GENERATION):
        print(name + ": GAME " + str(game+1) + "/" + str(GAMES_PER_GENERATION))
        try:
            bot = Bot(name, password, agent)
            score += bot.connect_and_listen(server, port)
        except:
            print("ERROR RUNNING " + name + "; RESTARTING GAME")
            server_q.put((server, port))
            genome_q.put((gen, ind, genome))
            return
        print("END GAME. MY SCORE: " + str(score))
    mean_score = score/GAMES_PER_GENERATION
    # return result and release server
    result_q.put((mean_score, genome))
    server_q.put((server, port))

def start_evolution(server_list, pop_size, generations, filename=None, mutation_prob=0.1, crossover_prob=0.8, elitism=2):
    # either load an existing generation or generate initial population
    if filename:
        f = open(filename, "rb")
        pop = pickle.load(f)
    else:
        pop = generate_random_pop(pop_size, INIT_TREE_MAX_DEPTH)

    # init server queue
    server_q = Queue()
    for server in server_list:
        server_q.put(server)

    # start evolution
    for g in range(generations):
        print("--------[GENERATION " + str(g) + "]--------")
        result_q = Queue()
        generation_scores = []

        # init genome queue
        genome_q = Queue()
        for i, genome in enumerate(pop):
            genome_q.put((g, i+1, genome))

        # run generation games
        while not genome_q.empty():
            current_server = server_q.get(block=True)
            t = Thread(target=play_individual, args=[current_server[0], current_server[1], genome_q, server_q, result_q])
            t.start()

        # get results
        for i_num in range(pop_size):
            generation_scores.append(result_q.get(block=True))

        # compute offsprings for next generation
        generation_scores.sort(reverse=True, key=lambda x: x[0])
        print("MAX FITNESS FOR GENERATION: " + str(generation_scores[0][0]))
        next_gen = []

        # saving generation according to score
        f = open(PICKLE_NAME + str(g) + ".pickle", "wb")
        pickle.dump([g for (s, g) in generation_scores], f)
        f.close()

        # first elitism
        for i in range(elitism):
            next_gen.append(generation_scores[i][1])
        # perform genetic operators
        for i in range(int(elitism/2), int(pop_size/2)):
            parent1_idx, parent2_idx = rank_selection(pop_size)
            parent1, parent2 = generation_scores[parent1_idx][1], generation_scores[parent2_idx][1]
            child1, child2 = parent1.clone(), parent2.clone()
            # crossover
            if(random() < crossover_prob):
                child1.crossover(child2)
            # mutation
            child1.mutation(mutation_prob)
            child2.mutation(mutation_prob)
            next_gen += [child1, child2]
        pop = next_gen