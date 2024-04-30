from models.problem import problem


class Node:
    def __init__(self, state, parent, action, path_cost, heuristic):
        self.state = state
        self.parent = parent
        self.action = action
        self.g = path_cost
        self.h = heuristic
        self.f = path_cost + heuristic

    @classmethod
    def root(cls, problem: problem):
        init_state = problem.get_init_state()
        return cls(init_state, None, None, 0, problem.heuristic(init_state))

    @classmethod
    def child(cls, problem, parent, action):
        child_state = problem.result(parent.state, action)
        return cls(
            child_state,
            parent,
            action,
            parent.g + problem.step_cost(parent.state, action),
            problem.heuristic(child_state))

    def __lt__(self, other):
        return ''.join(self.state) < ''.join(other.state)


def traverse_path(current_node: Node):
    actions = []
    cost = current_node.g

    while current_node.parent is not None:
        actions.append(current_node.action)
        current_node = current_node.parent

    actions.reverse()
    return actions, cost
