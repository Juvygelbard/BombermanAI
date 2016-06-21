from random import seed, randint

DIV_BY_ZERO = 0.0000001


# Class of all classes, oh mighty Node!
class Node(object):
    def __init__(self, data, is_terminal):
        self.data = data
        self.isTerminal = is_terminal
        self.children = []

    def getData(self):
        return self.data

    def generate_subtree(self, set_of_nodes, n):
        seed() # gives the engine a random number from the computer's clock to give as a random value
        classes = []
        for i in range(n):
            classes.append(set_of_nodes[randint(0, len(set_of_nodes)-1)]) # Appends one random child at a time
        self.children = [c() for c in classes]    # Constructs each child with its own Ctor

    def get_children(self):
        return self.children

    def evaluate(self, measures):
        raise NotImplementedError

    def to_str_tree(self):
        raise NotImplementedError

    def to_str_code(self):
        raise NotImplementedError

    def get_non_terminal_list(self):
        list_of_nodes = []
        if not self.isTerminal:
            list_of_nodes.append(self)
        for child in self.get_children():
            if not child.isTerminal:
                list_of_nodes += child.get_non_terminal_list()
        return list_of_nodes


####################### Terminal Node Classes #######################

class ConstantNum(Node):
    def __init__(self):
        super().__init__(randint(0, 9), True)   # Numbers get random values

    def generate_subtree(self, set_of_nodes):
        pass

    def evaluate(self, measures):
        return self.data

    def to_str_tree(self, level=0):
        return "    " * level + str(self.data) + "\n"

    def to_str_code(self):
        return str(self.data)


class RandomNum(Node):
    def __init__(self):
        super().__init__("random", True)   # Numbers get random values

    def generate_subtree(self, set_of_nodes):
        pass

    def evaluate(self, measures):
        return randint(0, 9)

    def to_str_tree(self, level=0):
        return "    " * level + self.data + "\n"

    def to_str_code(self):
        return self.data

####################### Arithmetic Node Classes #######################

class Add(Node):
    def __init__(self):
        super().__init__("+", False)

    def generate_subtree(self, set_of_nodes):
        super().generate_subtree(set_of_nodes, 2)

    def evaluate(self, measures):
        return self.children[0].evaluate(measures) + self.children[1].evaluate(measures)

    def to_str_tree(self, level=0):
        return "    " * level + self.data + "\n" + \
               self.children[0].to_str_tree(level+1) + \
               self.children[1].to_str_tree(level+1)

    def to_str_code(self):
        return "(" + self.children[0].to_str_code() + \
                self.data + \
                self.children[1].to_str_code() + ")"


class Sub(Node):
    def __init__(self):
        super().__init__("-", False)

    def generate_subtree(self, set_of_nodes):
        super().generate_subtree(set_of_nodes, 2)

    def evaluate(self, measures):
        return self.children[0].evaluate(measures) - self.children[1].evaluate(measures)

    def to_str_tree(self, level=0):
        return "    " * level + self.data + "\n" + \
               self.children[0].to_str_tree(level+1) + \
               self.children[1].to_str_tree(level+1)

    def to_str_code(self):
        return "(" + self.children[0].to_str_code() + \
                self.data + \
                self.children[1].to_str_code() + ")"


class Mul(Node):
    def __init__(self):
        super().__init__("*", False)

    def generate_subtree(self, set_of_nodes):
        super().generate_subtree(set_of_nodes, 2)

    def evaluate(self, measures):
        return self.children[0].evaluate(measures) * self.children[1].evaluate(measures)

    def to_str_tree(self, level=0):
        return "    " * level + self.data + "\n" + \
               self.children[0].to_str_tree(level+1) + \
               self.children[1].to_str_tree(level+1)

    def to_str_code(self):
        return "(" + self.children[0].to_str_code() + \
                self.data + \
                self.children[1].to_str_code() + ")"


class Div(Node):
    def __init__(self):
        super().__init__("/", False)

    def generate_subtree(self, set_of_nodes):
        super().generate_subtree(set_of_nodes, 2)

    def evaluate(self, measures):
        A = self.children[0].evaluate(measures)
        B =  self.children[1].evaluate(measures)
        if B==0:
            B=DIV_BY_ZERO
        return A / B

    def to_str_tree(self, level=0):
        return "    " * level + self.data + "\n" + \
               self.children[0].to_str_tree(level+1) + \
               self.children[1].to_str_tree(level+1)

    def to_str_code(self):
        return "(" + self.children[0].to_str_code() + \
                self.data + \
                self.children[1].to_str_code() + ")"


class Min(Node):
    def __init__(self):
        super().__init__("min", False)

    def generate_subtree(self, set_of_nodes):
        super().generate_subtree(set_of_nodes, 2)

    def evaluate(self, measures):
        return min([self.children[0].evaluate(measures), self.children[1].evaluate(measures)])

    def to_str_tree(self, level=0):
        return "    " * level + self.data + "\n" + \
               self.children[0].to_str_tree(level+1) + \
               self.children[1].to_str_tree(level+1)

    def to_str_code(self):
        return self.data + \
            "(" + self.children[0].to_str_code() + ", " +\
            self.children[1].to_str_code() + ")"


class Max(Node):
    def __init__(self):
        super().__init__("max", False)

    def generate_subtree(self, set_of_nodes):
        super().generate_subtree(set_of_nodes, 2)

    def evaluate(self, measures):
        return max([self.children[0].evaluate(measures), self.children[1].evaluate(measures)])

    def to_str_tree(self, level=0):
        return "    " * level + self.data + "\n" + \
               self.children[0].to_str_tree(level+1) + \
               self.children[1].to_str_tree(level+1)

    def to_str_code(self):
        return self.data + \
            "(" + self.children[0].to_str_code() + ", " +\
            self.children[1].to_str_code() + ")"


class Abs(Node):
    def __init__(self):
        super().__init__("abs", False)

    def generate_subtree(self, set_of_nodes):
        super().generate_subtree(set_of_nodes, 1)

    def evaluate(self, measures):
        return abs(self.children[0].evaluate(measures))

    def to_str_tree(self, level=0):
        return "    " * level + self.data + "\n" + \
               self.children[0].to_str_tree(level+1)

    def to_str_code(self):
        return self.data + \
            "(" + self.children[0].to_str_code() + ")"


class Neg(Node):
    def __init__(self):
        super().__init__("neg", False)

    def generate_subtree(self, set_of_nodes):
        super().generate_subtree(set_of_nodes, 1)

    def evaluate(self, measures):
        return (-1)*self.children[0].evaluate(measures)

    def to_str_tree(self, level=0):
        return "    " * level + self.data + "\n" + \
               self.children[0].to_str_tree(level+1)

    def to_str_code(self):
        return self.data + \
            "(" + self.children[0].to_str_code() + ")"

####################### Logic Node Classes #######################

class If_A_ge_B(Node):
    def __init__(self):
        super().__init__("if_>=", False)

    def generate_subtree(self, set_of_nodes):
        super().generate_subtree(set_of_nodes, 4)

    def evaluate(self, measures):
        A = self.children[0].evaluate(measures)
        B = self.children[1].evaluate(measures)
        if(A>=B):
            return self.children[2].evaluate(measures)
        else:
            return self.children[3].evaluate(measures)

    def to_str_tree(self, level=0):
        return "    " * level + "if >= (\n" + \
                self.children[0].to_str_tree(level+1) + \
                self.children[1].to_str_tree(level+1) + \
                "    " * level + ") then {\n" + \
                self.children[2].to_str_tree(level+1) + \
                "    " * level + "} else {\n" + \
                self.children[3].to_str_tree(level+1) + "}"

    def to_str_code(self):
        return "(if (" + self.children[0].to_str_code() + \
                ">=" + self.children[1].to_str_code() + \
               ") then " + self.children[2].to_str_code() + \
                " else " + self.children[3].to_str_code() + ")"

####################### Measure Node Classes #######################

class DistanceToClosestEnemy(Node):
    def __init__(self):
        super().__init__("DistanceToEnemy", True)

    def generate_subtree(self, set_of_nodes):
        pass

    def evaluate(self, measures):
        return measures[self.data]

    def to_str_tree(self, level=0):
        return "    " * level + str(self.data) + "\n"

    def to_str_code(self):
        return str(self.data)