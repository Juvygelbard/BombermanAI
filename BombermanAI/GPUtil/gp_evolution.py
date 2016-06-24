from ..Agents.bot import Bot
from .genome import Genome, TERMINALS, NODES
from ..Agents.gp_agent import GP_Agent
from random import random
from numpy.random import choice
import pickle

INIT_TREE_MAX_DEPTH = 3
GAMES_PER_GENERATION = 3
PLAYER_NAME = 'INDIVIDUAL'
PLAYER_PASS = 'JOHNKOZA'
PICKLE_NAME = 'generation_'

# creates initial population
def generate_random_pop(n, max_depth):
    ans = []
    for i in range(n):
        ans.append(Genome(max_depth, NODES, TERMINALS))
    return ans

# roulette wheel selection
def rank_selection(pop_size):
    total = sum(range(pop_size+1))
    prob = [(1+i)/total for i in range(pop_size)]
    prob.reverse() # lowest index has a better score and gets a higher probability
    parents = choice(pop_size, 2, replace=False, p=prob)
    return parents[0], parents[1]

def start_evolution(pop_size, generations, mutation_prob=0.2, elitism=2):
    pop = generate_random_pop(pop_size, INIT_TREE_MAX_DEPTH)

    for g in range(generations):
        # saving generation
        f = open(PICKLE_NAME + str(g) + ".pickle", "wb")
        pickle.dump(pop, f)
        f.close()
        print("--------[GENERATION " + str(g) + "]--------")
        generation_scores = []
        # run generation games
        for i_num, genome in enumerate(pop):
            my_name = PLAYER_NAME + "_" + str(g) +"_" + str(i_num+1)
            agent = GP_Agent(my_name, genome)
            score = 0
            for game in range(GAMES_PER_GENERATION):
                print(my_name + ": GAME " + str(game+1) + "/" + str(GAMES_PER_GENERATION))
                bot = Bot(my_name, PLAYER_PASS, agent)
                score += bot.connect_and_listen()
                print("END GAME. MY SCORE: " + str(score))
            mean_score = score/GAMES_PER_GENERATION
            generation_scores.append((mean_score, genome))
        generation_scores.sort(reverse=True, key=lambda x: x[0])
        print("MAX FITNESS FOR GENERATION: " + str(generation_scores[0][0]))
        next_gen = []
        # compute offsprings for next generation
        # first elitism
        for i in range(elitism):
            next_gen.append(generation_scores[i][1])
        # perform genetic operators
        for i in range(int(elitism/2), int(pop_size/2)):
            parent1_idx, parent2_idx = rank_selection(pop_size)
            parent1, parent2 = generation_scores[parent1_idx][1], generation_scores[parent2_idx][1]
            child1, child2 = parent1.clone(), parent2.clone()
            if(random() < 1-mutation_prob): # crossover
                child1.crossover(child2)
            else: # mutation
                child1.mutation()
                child2.mutation()
            next_gen += [child1, child2]
        pop = next_gen