from heapq import heappush, heappop
from itertools import count

from lib.utils import visualize
from models.tree import Node, traverse_path
from models.problem import problem

counter = count()


def greedy_best_first(problem: problem, verbose=False):
    frontier = [(None, None, Node.root(problem))]
    explored = set()

    while frontier:
        if verbose:
            visualize(problem.get_map_encoding(), frontier)

        _, _, node = heappop(frontier)
        if node.state in explored:
            continue

        if problem.goal_test(node.state):
            return traverse_path(node)

        explored.add(node.state)

        possible_actions = problem.actions(node.state)

        for action in possible_actions:
            child = Node.child(problem, node, action)

            if child.state not in explored:
                heappush(frontier, (child.h, next(counter), child))
