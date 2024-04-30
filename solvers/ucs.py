from queue import PriorityQueue

from lib.utils import visualize
from models.tree import Node, traverse_path
from models.problem import problem


def ucs(problem: problem, verbose=False):
    # initial state is solution
    if problem.goal_test(problem.get_init_state()):
        return traverse_path(Node.root(problem.get_init_state()))

    # init UCS priority queue and visited set
    frontier = PriorityQueue()
    frontier.put((0, Node.root(problem)))
    explored = {problem.get_init_state()}

    while not frontier.empty():
        if verbose:
            frontier_list = [(0, 0, x[1]) for x in frontier.queue]
            visualize(problem.get_map_encoding(), frontier_list)

        # choose the path with the lowest cost
        cost, lowest_path_node = frontier.get()

        # check if current state is solution
        if problem.goal_test(lowest_path_node.state):
            return traverse_path(lowest_path_node)

        # mark state as visisted
        explored.add(lowest_path_node.state)

        # explore neighbour nodes
        for action in problem.actions(lowest_path_node.state):
            next_node = Node.child(problem, lowest_path_node, action)

            # if node not visited add it to the priority queue
            if next_node.state not in explored:
                # compute action cost
                action_cost = problem.step_cost(lowest_path_node.state, action)
                path_cost = cost + action_cost

                frontier.put((path_cost, next_node))
