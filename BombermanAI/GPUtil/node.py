from random import seed, randint, random

DIV_BY_ZERO = 0.0000001
TERMINAL_RATIO = 0.2

# Class of all classes, oh mighty Node!
class Node(object):
    def __init__(self, data, is_terminal, depth=0):
        self.data = data
        self.isTerminal = is_terminal
        self.depth = depth
        self.children = []

    def getData(self):
        return self.data

    def generate_subtree(self, nodes, terminals, n):
        seed() # gives the engine a random number from the computer's clock to give as a random value
        classes = []
        for i in range(n):
            if nodes and random() > TERMINAL_RATIO:
                # Appends from nodes or from terminals depending on the ratio between the lists
                classes.append(nodes[randint(0, len(nodes)-1)]) # Appends one random child at a time
            else:
                classes.append(terminals[randint(0, len(terminals)-1)]) # Appends one random child at a time
        self.children = [c(self.depth+1) for c in classes]    # Constructs each child with its own Ctor

    def evaluate(self, measures):
        raise NotImplementedError

    def clone(self):
        clone = type(self)(self.depth) # create an instance of the same class
        clone.data = self.data
        clone.children = [child.clone() for child in self.children]
        return clone

    def to_str_tree(self):
        raise NotImplementedError

    def to_str_code(self):
        raise NotImplementedError

    def get_non_terminal_list(self):
        list_of_nodes = []
        if not self.isTerminal:
            list_of_nodes.append(self)
        for child in self.children:
            if not child.isTerminal:
                list_of_nodes += child.get_non_terminal_list()
        return list_of_nodes

    def get_height(self):
        return 1 + max([c.get_height() for c in self.children] + [0])

    def update_depth(self, d):
        self.depth = d
        for child in self.children:
            child.update_depth(d+1)

####################### Terminal Node Classes #######################

class ConstantNum(Node):
    def __init__(self, depth=0):
        super().__init__(randint(0, 9), True, depth)   # Numbers get random values

    def generate_subtree(self, nodes, terminals):
        pass

    def evaluate(self, measures):
        return self.data

    def to_str_tree(self, level=0):
        return "    " * level + str(self.data) + "\n"

    def to_str_code(self):
        return str(self.data)


class RandomNum(Node):
    def __init__(self, depth=0):
        super().__init__("random", True, depth)   # Numbers get random values

    def generate_subtree(self, nodes, terminals):
        pass

    def evaluate(self, measures):
        return randint(0, 9)

    def to_str_tree(self, level=0):
        return "    " * level + self.data + "\n"

    def to_str_code(self):
        return self.data

####################### Arithmetic Node Classes #######################

class Add(Node):
    def __init__(self, depth=0):
        super().__init__("+", False, depth)

    def generate_subtree(self, nodes, terminals):
        super().generate_subtree(nodes, terminals, 2)

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
    def __init__(self, depth=0):
        super().__init__("-", False, depth)

    def generate_subtree(self, nodes, terminals):
        super().generate_subtree(nodes, terminals, 2)

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
    def __init__(self, depth=0):
        super().__init__("*", False, depth)

    def generate_subtree(self, nodes, terminals):
        super().generate_subtree(nodes, terminals, 2)

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
    def __init__(self, depth=0):
        super().__init__("/", False, depth)

    def generate_subtree(self, nodes, terminals):
        super().generate_subtree(nodes, terminals, 2)

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
    def __init__(self, depth=0):
        super().__init__("min", False, depth)

    def generate_subtree(self, nodes, terminals):
        super().generate_subtree(nodes, terminals, 2)

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
    def __init__(self, depth=0):
        super().__init__("max", False, depth)

    def generate_subtree(self, nodes, terminals):
        super().generate_subtree(nodes, terminals, 2)

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
    def __init__(self, depth=0):
        super().__init__("abs", False, depth)

    def generate_subtree(self, nodes, terminals):
        super().generate_subtree(nodes, terminals, 1)

    def evaluate(self, measures):
        return abs(self.children[0].evaluate(measures))

    def to_str_tree(self, level=0):
        return "    " * level + self.data + "\n" + \
               self.children[0].to_str_tree(level+1)

    def to_str_code(self):
        return self.data + \
            "(" + self.children[0].to_str_code() + ")"


class Neg(Node):
    def __init__(self, depth=0):
        super().__init__("neg", False, depth)

    def generate_subtree(self, nodes, terminals):
        super().generate_subtree(nodes, terminals, 1)

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
    def __init__(self, depth=0):
        super().__init__("if_>=", False, depth)

    def generate_subtree(self, nodes, terminals):
        super().generate_subtree(nodes, terminals, 4)

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


class Compare(Node):
    def __init__(self, depth=0):
        super().__init__("compare", False, depth)

    def generate_subtree(self, nodes, terminals):
        super().generate_subtree(nodes, terminals, 2)

    def evaluate(self, measures):
        A = self.children[0].evaluate(measures)
        B = self.children[1].evaluate(measures)
        if(A > B):
            return 1
        elif(A == B):
            return 0
        else:
            return -1

    def to_str_tree(self, level=0):
        return "    " * level + "compare \n" + \
                self.children[0].to_str_tree(level+1) + \
                self.children[1].to_str_tree(level+1)

    def to_str_code(self):
        return "compare(" + self.children[0].to_str_code() + \
                ", " + self.children[1].to_str_code() + ")"


####################### Measure Node Classes #######################


# Represents a basic measure in the fitness tree
class MeasureNode(Node):
    def __init__(self, measure, depth=0):
        super().__init__(measure, True, depth)

    def generate_subtree(self, nodes, terminals):
        pass

    def evaluate(self, measures):
        return measures[self.data]

    def to_str_tree(self, level=0):
        return "    " * level + str(self.data) + "\n"

    def to_str_code(self):
        return str(self.data)

#  Indicates if the individual can move in direction UP
class CanMove_UP(MeasureNode):
    def __init__(self, depth=0):
        super().__init__("CanMove_UP", depth)

#  Indicates if the individual can move in direction DOWN
class CanMove_DN(MeasureNode):
    def __init__(self, depth=0):
        super().__init__("CanMove_DN", depth)

#  Indicates if the individual can move in direction LEFT
class CanMove_LT(MeasureNode):
    def __init__(self, depth=0):
        super().__init__("CanMove_LT", depth)

#  Indicates if the individual can move in direction RIGHT
class CanMove_RT(MeasureNode):
    def __init__(self, depth=0):
        super().__init__("CanMove_RT", depth)

#  Represents the distance from the closest enemy in direction UP. The closest enemy is the enemy with the shortest
# distance from the individual with minimum separating walls
class EnemyDist_UP(MeasureNode):
    def __init__(self, depth=0):
        super().__init__("EnemyDist_UP", depth)


#  Represents the distance from the closest enemy in direction DOWN. The closest enemy is the enemy with the shortest
# distance from the individual with minimum separating walls
class EnemyDist_DN(MeasureNode):
    def __init__(self, depth=0):
        super().__init__("EnemyDist_DN", depth)

#  Represents the distance from the closest enemy in direction LEFT. The closest enemy is the enemy with the shortest
# distance from the individual with minimum separating walls
class EnemyDist_LT(MeasureNode):
    def __init__(self, depth=0):
        super().__init__("EnemyDist_LT", depth)

#  Represents the distance from the closest enemy in direction RIGHT. The closest enemy is the enemy with the shortest
# distance from the individual with minimum separating walls
class EnemyDist_RT(MeasureNode):
    def __init__(self, depth=0):
        super().__init__("EnemyDist_RT", depth)

#  Indicates if the individual is in danger (close to a bomb) in direction UP
class InDanger_UP(MeasureNode):
    def __init__(self, depth=0):
        super().__init__("InDanger_UP", depth)


#  Indicates if the individual is in danger (close to a bomb) in direction DOWN
class InDanger_DN(MeasureNode):
    def __init__(self, depth=0):
        super().__init__("InDanger_DN", depth)


#  Indicates if the individual is in danger (close to a bomb) in direction LEFT
class InDanger_LT(MeasureNode):
    def __init__(self, depth=0):
        super().__init__("InDanger_LT", depth)


#  Indicates if the individual is in danger (close to a bomb) in direction RIGHT
class InDanger_RT(MeasureNode):
    def __init__(self, depth=0):
        super().__init__("InDanger_RT", depth)


#  Represents the distance from the closest turn if moving UP
class NearTurn_UP(MeasureNode):
    def __init__(self, depth=0):
        super().__init__("NearTurn_UP", depth)


#  Represents the distance from the closest turn if moving DOWN
class NearTurn_DN(MeasureNode):
    def __init__(self, depth=0):
        super().__init__("NearTurn_DN", depth)


#  Represents the distance from the closest turn if moving LEFT
class NearTurn_LT(MeasureNode):
    def __init__(self, depth=0):
        super().__init__("NearTurn_LT", depth)


#  Represents the distance from the closest turn if moving RIGHT
class NearTurn_RT(MeasureNode):
    def __init__(self, depth=0):
        super().__init__("NearTurn_RT", depth)

#  Indicates if the enemy is in range for the individual to place a bomb
class EnemyInRange(MeasureNode):
    def __init__(self, depth=0):
        super().__init__("EnemyInRange", depth)