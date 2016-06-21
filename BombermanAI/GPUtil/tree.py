from node import *
from random import randint


class Tree(object):
    def __init__(self, max_depth, nodes, terminals):
        self.const_nodes = nodes
        self.const_terminals = terminals
        self.root = self.gen_tree(max_depth, nodes, terminals)

    def grow_tree(self, tree, max_depth, nodes, terminals):
        if max_depth == 1:
            tree.generate_subtree(terminals)
        elif max_depth > 1:
            tree.generate_subtree(nodes + terminals)
            for subtree in tree.get_children():
                self.grow_tree(subtree, max_depth-1, nodes, terminals)

    def gen_tree(self, max_depth, nodes, terminals):
        if max_depth == 0:
            return terminals[randint(0, len(terminals)-1)]()  # Constructs a random node
        else:
            terms_nodes = terminals + nodes
            tree = terms_nodes[randint(0, len(terms_nodes)-1)]()
            self.grow_tree(tree, max_depth, nodes, terminals)
            return tree

    def print_as_tree(self):
        print(self.root.to_str_tree())

    def print_as_code(self):
        print(self.root.to_str_code())

    def get_random_child_for_crossover(self):
        nodes = self.root.get_non_terminal_list()
        if(not nodes):
            return False, False
        parent = nodes[randint(0, len(nodes)-1)]  # Chooses random non terminal node
        children = parent.get_children()
        child_idx = randint(0, len(children)-1)  # Chooses a random child from the chosen node
        return parent, child_idx

    # Will be used as a tool for the mutation and crossover genetic operators
    def replace_node(self, new_genome):
        nodes = self.root.get_non_terminal_list()
        part_num = randint(0, len(nodes))  # Chooses random non terminal node
        if part_num == len(nodes):  # 1/tree_size probability for the root to change
            self.root = new_genome
        else:
            children = nodes[part_num].get_children()
            child_idx = randint(0, len(children)-1)  # Chooses a random child from the chosen node
            children[child_idx] = new_genome

    def perform_mutation(self, n):
        new_genome = self.gen_tree(n, self.const_nodes, self.const_terminals)
        # TODO: DECIDE WHAT DEPTH SHOULD BE USED FOR MUTATION
        self.replace_node(new_genome)

    def perform_crossover(self, other):
        p1, c1 = self.get_random_child_for_crossover()
        p2, c2 = other.get_random_child_for_crossover()
        if (not p1) or (not p2):    # make sure crossover is possible
            return
        tmp = p1.get_children()[c1]
        p1.get_children()[c1] = p2.get_children()[c2]
        p2.get_children()[c2] = tmp

    def evaluate_tree(self, measures):
        return self.root.evaluate(measures)


#  TIME FOR SOME FUCKING TESTS!!!
terminals = [ConstantNum, RandomNum, DistanceToClosestEnemy]  # Also Random
nodes = [Add, Sub, Mul, Div, Min, Max, Abs, Neg, If_A_ge_B]

# tree1 = Tree(2, nodes, terminals)
# print("TREE1")
# tree1.print_as_tree()
#
# tree2 = Tree(2, nodes, terminals)
# print("TREE2")
# tree2.print_as_tree()
#
#
# # testing mutation
# tree1.perform_mutation(1)
# print("TREE1 AFTER MUTATION")
# tree1.print_as_tree()
#
# # testing crossover
# tree1.perform_crossover(tree2)
# print("TREE1 AFTER CROSSOVER WITH TREE2")
# tree1.print_as_tree()
# print("TREE2 AFTER CROSSOVER WITH TREE1")
# tree2.print_as_tree()

measures = {"DistanceToEnemy": 10}

tree = Tree(4, nodes, terminals)
tree.print_as_code()
tree.print_as_tree()
print("Evaluation: " + str(tree.evaluate_tree(measures)))