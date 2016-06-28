from .node import *
from random import randint, random

class Tree(object):
    def __init__(self, init_depth, max_depth, nodes, terminals, root=None):
        self.const_nodes = nodes
        self.const_terminals = terminals
        self.init_depth = init_depth
        self.max_depth = max_depth
        self.root = root
        if not self.root:
            self.root = self.gen_tree(init_depth, nodes, terminals)

    def grow_tree(self, tree, init_depth, nodes, terminals):
        if init_depth == 1:
            tree.generate_subtree([], terminals)
        elif init_depth > 1:
            tree.generate_subtree(nodes, terminals)
            for subtree in tree.children:
                self.grow_tree(subtree, init_depth-1, nodes, terminals)

    def gen_tree(self, init_depth, nodes, terminals):
        if init_depth == 0:
            return terminals[randint(0, len(terminals)-1)]()  # Constructs a random node
        else:
            if random() <= TERMINAL_RATIO:
                tree = terminals[randint(0, len(terminals)-1)]()
            else:
                tree = nodes[randint(0, len(nodes)-1)]()
            self.grow_tree(tree, init_depth, nodes, terminals)
            return tree

    def print_as_tree(self):
        print(self.root.to_str_tree())

    def print_as_code(self):
        print(self.root.to_str_code())

    def get_random_child_for_crossover(self):
        nodes = self.root.get_non_terminal_list()
        if not nodes:
            return False, False
        parent = nodes[randint(0, len(nodes)-1)]  # Chooses random non terminal node
        child_idx = randint(0, len(parent.children)-1)  # Chooses a random child from the chosen node
        return parent, child_idx

    def perform_mutation(self, n):
        nodes = self.root.get_non_terminal_list()
        part_num = randint(0, len(nodes))  # Chooses random non terminal node
        if part_num == len(nodes):  # 1/tree_size probability for the root to change
            self.root = self.gen_tree(min(n, self.max_depth) , self.const_nodes, self.const_terminals)
        else:
            parent = nodes[part_num]
            child_idx = randint(0, len(parent.children)-1)  # Chooses a random child from the chosen node TODO: inspect
            parent.children[child_idx] = self.gen_tree(min(n, self.max_depth-(parent.depth+1)) , self.const_nodes, self.const_terminals) # grow a tree that dosn't exceed the given max depth
            parent.children[child_idx].update_depth(parent.depth+1) # update the child's depth

    def perform_crossover(self, other):
        # get random nodes for crossover := (parent, child_index)
        p1, c1 = self.get_random_child_for_crossover()
        p2, c2 = other.get_random_child_for_crossover()

        # make sure crossover is possible
        # one of the trees is just a node := don't preform crossover
        if not p1 or not p2:
            return

        # check max_depth is not exceeded; if it does, get a new node
        while(p1.depth + p2.children[c2].get_height()-1 >= self.max_depth or
              p2.depth + p1.children[c1].get_height()-1 >= other.max_depth):
            p2, c2 = other.get_random_child_for_crossover()

        # update nodes depths
        p1.children[c1].update_depth(p2.depth+1)
        p2.children[c2].update_depth(p1.depth+1)

        # preform crossover
        tmp = p1.children[c1]
        p1.children[c1] = p2.children[c2]
        p2.children[c2] = tmp


    def evaluate_tree(self, measures):
        return self.root.evaluate(measures)

    def clone(self):
        new_root = self.root.clone()
        return Tree(self.init_depth, self.max_depth, self.const_nodes, self.const_terminals, new_root)