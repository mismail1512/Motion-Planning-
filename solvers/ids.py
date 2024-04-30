from lib.utils import visualize
from models.problem import problem
from models.tree import Node, traverse_path


def dls(problem: problem, limit: int, verbose=False):
    # initial state is solution
    if problem.goal_test(problem.get_init_state()):
        return traverse_path(Node.root(problem.get_init_state()))

    # init DFS graph
    frontier = [Node.root(problem)]
    explored = {problem.get_init_state()}

    # init depth tracker
    depth_map = {
        problem.get_init_state(): 0,
    }

    # while stack not empty
    while frontier:
        if verbose:
            frontier_list = [(0, 0, x) for x in list(frontier)]
            visualize(problem.get_map_encoding(), frontier_list)

        # get top node from the stack
        current_node = frontier.pop()

        # if current state is solution return
        if problem.goal_test(current_node.state):
            return traverse_path(current_node)

        # mark node as visited
        explored.add(current_node.state)

        # explore neighbour nodes
        for action in problem.actions(current_node.state):
            next_node = Node.child(problem, current_node, action)
            depth_map[next_node.state] = depth_map[current_node.state] + 1

            # if node not visited and not too far add it to the stack
            if next_node.state not in explored and depth_map[next_node.state] < limit:
                frontier.append(next_node)


def ids(problem: problem):
    # note: we can use max depth to break this loop in case of very big graphs
    current_depth = 1

    while True:
        solution_actions = dls(problem, current_depth)

        if solution_actions:
            return solution_actions

        current_depth += 1
