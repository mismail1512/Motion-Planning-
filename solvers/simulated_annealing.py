from random import choice, random
from math import exp
from itertools import count
from models.problem import problem
from models.tree import Node, traverse_path


def simulated_annealing(problem: problem):
    # initial state is solution
    if problem.goal_test(problem.get_init_state()):
        return traverse_path(Node.root(problem.get_init_state()))

    current_state = problem.get_init_state()
    current_node = Node.root(problem)
    current_value = problem.heuristic(current_state)

    for t in count():

        T = exp(-t)

        if current_value is 0 or T is 0:
            return traverse_path(current_node)

        next_nodes = [Node.child(problem, current_node, action)
                      for action in problem.actions(current_state)]

        while True:
            next_node: Node = choice(next_nodes)
            next_value = problem.heuristic(next_node.state)
            delta = current_value - next_value

            if delta > 0 or random() < exp(delta / T):
                current_node = next_node
                current_state = next_node.state
                current_value = next_value
                break
