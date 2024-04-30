from models.problem import problem
from models.tree import Node, traverse_path


def hill_climbing(problem: problem):
    # initial state is solution
    if problem.goal_test(problem.get_init_state()):
        return traverse_path(Node.root(problem.get_init_state()))

    current_node = Node.root(problem)
    current_state = problem.get_init_state()
    current_value = problem.heuristic(current_state)

    while True:
        next_state, next_value = None, None

        for action in problem.actions(current_state):
            new_state = problem.result(current_state, action)
            new_value = problem.heuristic(new_state)

            if next_value is None or next_value > new_value:
                next_state, next_value = new_state, new_value

        if current_value <= next_value:
            return traverse_path(current_node)

        current_state, current_value = next_state, next_value
        current_node = Node.child(problem, current_node, action)
