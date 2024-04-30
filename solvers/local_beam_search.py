from models.problem import problem
from models.tree import Node, traverse_path


def local_beam_search(problem: problem, beam_size=5):
    # init search problem
    frontier = [{
        'node': Node.root(problem),
        'state': problem.get_init_state(),
        'value': problem.heuristic(problem.get_init_state())}
    ]

    while True:
        possible_next_actions = []

        for option in frontier:
            # test goal
            if problem.goal_test(option['state']):
                return traverse_path(option['node'])

            # search possible next actions
            next_actions = problem.actions(option['state'])

            for action in next_actions:
                new_state = problem.result(option['state'], action)

                possible_next_actions.append({
                    'node': Node.child(problem, option['node'], action),
                    'state': new_state,
                    'value': problem.heuristic(new_state)
                })

        # pick @beam_size from next possible actions
        sorted_next_actions = sorted(
            possible_next_actions, key=lambda x: x['value'])
        frontier = sorted_next_actions[:beam_size]
