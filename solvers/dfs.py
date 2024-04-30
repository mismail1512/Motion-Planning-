from lib.utils import visualize

from models.problem import problem
from models.tree import Node, traverse_path


def dfs(problem: problem, verbose=False):
    # initial state is solution
    if problem.goal_test(problem.get_init_state()):
        return traverse_path(Node.root(problem.get_init_state()))

    # init DFS stack and visited set
    frontier = [Node.root(problem)]
    explored = {problem.get_init_state()}

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

            # if node not visited add it to the stack
            if next_node.state not in explored:
                frontier.append(next_node)
