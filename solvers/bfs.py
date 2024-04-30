from collections import deque

from lib.utils import visualize
from models.problem import problem
from models.tree import Node, traverse_path


def bfs(problem: problem, verbose=False):
    if problem.goal_test(problem.get_init_state()):
        return traverse_path(Node.root(problem.get_init_state()))

    frontier = deque([Node.root(problem)])
    explored = {problem.get_init_state()}

    while frontier:
        if verbose:
            frontier_list = [(0, 0, x) for x in list(frontier)]
            visualize(problem.get_map_encoding(), frontier_list)

        node = frontier.pop()

        for action in problem.actions(node.state):
            child = Node.child(problem, node, action)

            if child.state not in explored:
                if problem.goal_test(child.state):
                    return traverse_path(child)

                frontier.appendleft(child)
                explored.add(child.state)
