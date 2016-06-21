from tree import *

terminals = [ConstantNum, RandomNum, NearEnemy_CLR_UP, NearEnemy_CLR_DN, NearEnemy_CLR_LT, NearEnemy_CLR_RT,
             NearEnemy_WALL_UP, NearEnemy_WALL_DN, NearEnemy_WALL_LT, NearEnemy_WALL_RT,
             InDanger_UP, InDanger_DN, InDanger_LT, InDanger_RT,
             NearTurn_UP, NearTurn_DN, NearTurn_LT, NearTurn_RT]  # Also Random

nodes = [Add, Sub, Mul, Div, Min, Max, Abs, Neg, If_A_ge_B, Compare]

class Genome(object):
    def __init__(self, max_depth, nodes, terminals):
        #  Will hold a tree for each possible action
        self.tree_set = [("NONE", Tree(max_depth, nodes, terminals)),
                        ("BOMB", Tree(max_depth, nodes, terminals)),
                        ("UP", Tree(max_depth, nodes, terminals)),
                        ("DOWN", Tree(max_depth, nodes, terminals)),
                        ("LEFT", Tree(max_depth, nodes, terminals)),
                        ("RIGHT", Tree(max_depth, nodes, terminals))]

    def next_move(self, list_of_measures):
        tree_scores = [(t.evaluate_tree(list_of_measures), s) for (s, t) in self.tree_set]
        #  Gets a list of evaluations of all trees
        return max(tree_scores)[1]  # The highest score will be in the first index

gen = Genome(10, nodes, terminals)
gen.tree_set[0][1].print_as_code()