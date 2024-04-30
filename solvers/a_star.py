from queue import PriorityQueue

from lib.utils import visualize
from models.tree import Node, traverse_path
from models.problem import problem


def a_star(problem: problem, verbose=False):
    # initial state is solution
    if problem.goal_test(problem.get_init_state()):
        return traverse_path(Node.root(problem.get_init_state()))

    # init a start priority queue and visited set
    frontier = PriorityQueue()
    root_a_star_score = 0
    frontier.put((root_a_star_score, Node.root(problem)))
    explored = {problem.get_init_state(): root_a_star_score}

    while not frontier.empty():
        if verbose:
            frontier_list = [(0, 0, x[1]) for x in frontier.queue]
            visualize(problem.get_map_encoding(), frontier_list)

        # choose the path with the lowest a star score
        a_star_score, lowest_path_node = frontier.get()
        current_node_heu = problem.heuristic(lowest_path_node.state)
        current_node_total_path_cost = a_star_score - current_node_heu

        # check if current state is solution
        if problem.goal_test(lowest_path_node.state):
            return traverse_path(lowest_path_node)

        # mark state as visisted
        explored[lowest_path_node.state] = a_star_score

        # explore neighbour nodes
        for action in problem.actions(lowest_path_node.state):
            next_node = Node.child(problem, lowest_path_node, action)
            next_node_heu = problem.heuristic(next_node.state)
            next_node_path_cost = problem.step_cost(
                lowest_path_node.state, action)
            next_node_a_star_score = current_node_total_path_cost + \
                next_node_path_cost + next_node_heu

            # if node not visited and the path has lower A* score add it to the priority queue
            if next_node.state in explored.keys():
                if explored[next_node.state] <= next_node_a_star_score:
                    continue

            frontier.put((next_node_a_star_score, next_node))
