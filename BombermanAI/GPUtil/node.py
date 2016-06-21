from random import seed, randint, random

DIV_BY_ZERO = 0.0000001
TERMINAL_RATIO = 0.2

# Class of all classes, oh mighty Node!
class Node(object):
    def __init__(self, data, is_terminal):
        self.data = data
        self.isTerminal = is_terminal
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

    def generate_subtree(self, nodes, terminals):
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
    def __init__(self):
        super().__init__("+", False)

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
    def __init__(self):
        super().__init__("-", False)

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
    def __init__(self):
        super().__init__("*", False)

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
    def __init__(self):
        super().__init__("/", False)

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
    def __init__(self):
        super().__init__("min", False)

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
    def __init__(self):
        super().__init__("max", False)

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
    def __init__(self):
        super().__init__("abs", False)

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
    def __init__(self):
        super().__init__("neg", False)

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
    def __init__(self):
        super().__init__("if_>=", False)

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
    def __init__(self):
        super().__init__("compare", False)

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
        return "    " * level + "compare (\n" + \
                self.children[0].to_str_tree(level+1) + \
                "    " * level + ", \n" + \
                self.children[1].to_str_tree(level+1) + ")"

    def to_str_code(self):
        return "compare(" + self.children[0].to_str_code() + \
                ", " + self.children[1].to_str_code() + ")"


####################### Measure Node Classes #######################


# Represents a basic measure in the fitness tree
class MeasureNode(Node):
    def __init__(self, measure):
        super().__init__(measure, True)

    def generate_subtree(self, nodes, terminals):
        pass

    def evaluate(self, measures):
        return measures[self.data]

    def to_str_tree(self, level=0):
        return "    " * level + str(self.data) + "\n"

    def to_str_code(self):
        return str(self.data)


#  Represents the distance from the closest enemy WITHOUT separating walls in direction UP
class NearEnemy_CLR_UP(MeasureNode):
    def __init__(self):
        super().__init__("NearEnemy_CLR_UP")


#  Represents the distance from the closest enemy WITHOUT separating walls in direction DOWN
class NearEnemy_CLR_DN(MeasureNode):
    def __init__(self):
        super().__init__("NearEnemy_CLR_DN")


#  Represents the distance from the closest enemy WITHOUT separating walls in direction LEFT
class NearEnemy_CLR_LT(MeasureNode):
    def __init__(self):
        super().__init__("NearEnemy_CLR_LT")


#  Represents the distance from the closest enemy WITHOUT separating walls in direction RIGHT
class NearEnemy_CLR_RT(MeasureNode):
    def __init__(self):
        super().__init__("NearEnemy_CLR_RT")


#  Represents the distance from the closest enemy WITH separating walls in direction UP
class NearEnemy_WALL_UP(MeasureNode):
    def __init__(self):
        super().__init__("NearEnemy_WALL_UP")


#  Represents the distance from the closest enemy WITH separating walls in direction DOWN
class NearEnemy_WALL_DN(MeasureNode):
    def __init__(self):
        super().__init__("NearEnemy_WALL_DN")


#  Represents the distance from the closest enemy WITH separating walls in direction LEFT
class NearEnemy_WALL_LT(MeasureNode):
    def __init__(self):
        super().__init__("NearEnemy_WALL_LT")


#  Represesnts the distance from the closest enemy WITH separating walls in direction RIGHT
class NearEnemy_WALL_RT(MeasureNode):
    def __init__(self):
        super().__init__("NearEnemy_WALL_RT")


#  Indicates if the individual is in danger (close to a bomb) in direction UP
class InDanger_UP(MeasureNode):
    def __init__(self):
        super().__init__("InDanger_UP")


#  Indicates if the individual is in danger (close to a bomb) in direction DOWN
class InDanger_DN(MeasureNode):
    def __init__(self):
        super().__init__("InDanger_DN")


#  Indicates if the individual is in danger (close to a bomb) in direction LEFT
class InDanger_LT(MeasureNode):
    def __init__(self):
        super().__init__("InDanger_LT")


#  Indicates if the individual is in danger (close to a bomb) in direction RIGHT
class InDanger_RT(MeasureNode):
    def __init__(self):
        super().__init__("InDanger_RT")


#  Represents the distance from the closest turn in direction UP
class NearTurn_UP(MeasureNode):
    def __init__(self):
        super().__init__("NearTurn_UP")


#  Represents the distance from the closest turn in direction DOWN
class NearTurn_DN(MeasureNode):
    def __init__(self):
        super().__init__("NearTurn_DN")


#  Represents the distance from the closest turn in direction LEFT
class NearTurn_LT(MeasureNode):
    def __init__(self):
        super().__init__("NearTurn_LT")


#  Represents the distance from the closest turn in direction RIGHT
class NearTurn_RT(MeasureNode):
    def __init__(self):
        super().__init__("NearTurn_RT")




