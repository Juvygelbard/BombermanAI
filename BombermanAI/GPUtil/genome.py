from .tree import *

TERMINALS = [ConstantNum, RandomNum, CanMove_UP, CanMove_DN, CanMove_LT, CanMove_RT, NearEnemy_CLR_UP, NearEnemy_CLR_DN, NearEnemy_CLR_LT, NearEnemy_CLR_RT,
             NearEnemy_WALL_UP, NearEnemy_WALL_DN, NearEnemy_WALL_LT, NearEnemy_WALL_RT,
             InDanger_UP, InDanger_DN, InDanger_LT, InDanger_RT,
             NearTurn_UP, NearTurn_DN, NearTurn_LT, NearTurn_RT]  # Also Random

NODES = [Add, Sub, Mul, Div, Min, Max, Abs, Neg, If_A_ge_B, Compare]

MUTATION_MAX_DEPTH = 3

class Genome(object):
    def __init__(self, max_depth, nodes, terminals, tree_set=None):
        self.max_depth = max_depth
        self.nodes = nodes
        self.terminals = terminals
        self.tree_set = tree_set

        #  Will hold a tree for each possible action
        if(not self.tree_set):
            self.tree_set = [("NONE", Tree(max_depth, nodes, terminals)),
                             ("BOMB", Tree(max_depth, nodes, terminals)),
                             ("UP", Tree(max_depth, nodes, terminals)),
                             ("DOWN", Tree(max_depth, nodes, terminals)),
                             ("LEFT", Tree(max_depth, nodes, terminals)),
                             ("RIGHT", Tree(max_depth, nodes, terminals))]

    def next_move(self, list_of_measures):
        tree_scores = [(t.evaluate_tree(list_of_measures), s) for (s, t) in self.tree_set]
        #  Gets a list of evaluations of all trees
        tree_scores.sort(reverse=True)
        return [s for (e, s) in tree_scores]  # sorted by score from high to low

    # all trees are going thorough crossover
    def crossover(self, other):
        for (s1, t1), (s2, t2) in zip(self.tree_set, other.tree_set):
            t1.perform_crossover(t2)

    # each tree is going through mutation with [prob] probability
    def mutation(self, prob):
        for s, t in self.tree_set:
            if random() < prob:
                t.perform_mutation(MUTATION_MAX_DEPTH)

    def clone(self):
        new_treeset = [(s, t.clone()) for (s, t) in self.tree_set]
        return Genome(self.max_depth, self.nodes, self.terminals, new_treeset)