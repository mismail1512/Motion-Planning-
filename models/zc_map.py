import string

from lib.utils import get_map_width, get_map_height, get_map_symbol, compute_map_xy
from models.problem import problem


class zc_map(problem):
    _init_state: tuple
    _goal_state: tuple
    _encoded_map: str

    _heuristic: str

    def __init__(self, init_state: str, heuristic: str):
        self._encoded_map = init_state
        self._heuristic = heuristic

        # create init state
        flat_init_state = init_state.replace('\n', '')
        self._init_state = tuple(flat_init_state)

        # create goal state
        goal_state = flat_init_state.replace('*', ' ')
        goal_state = goal_state.replace('+', '*')
        self._goal_state = tuple(goal_state)

        self._action_values = {
            'up': -get_map_width(self._encoded_map),
            'down': +get_map_width(self._encoded_map),
            'left': -1,
            'right': +1
        }

    def get_init_state(self):
        return self._init_state

    def get_map_encoding(self):
        return self._encoded_map

    def actions(self, state):
        index = state.index('*')
        possible_actions = []

        bottom_limit = (get_map_width(self._encoded_map) * get_map_height(self._encoded_map) -
                        1) // get_map_width(self._encoded_map)

        if index // get_map_width(self._encoded_map) > 0 and state[index - get_map_width(self._encoded_map)] != '#':
            possible_actions.append('up')

        if index // get_map_width(self._encoded_map) < bottom_limit and state[index + get_map_width(self._encoded_map)] != '#':
            possible_actions.append('down')

        if index % get_map_width(self._encoded_map) > 0 and state[index-1] != '#':
            possible_actions.append('left')

        if index % get_map_width(self._encoded_map) < get_map_width(self._encoded_map) - 1 and state[index + 1] != '#':
            possible_actions.append('right')

        return possible_actions

    def result(self, state, action):
        index = state.index('*')
        new_index = index + self._action_values[action]

        list_state = list(state)

        if list_state[index] == '*' and list_state[new_index] == '+':
            list_state[index] = ' '
            list_state[new_index] = '*'

        else:
            list_state[index], list_state[new_index] = list_state[new_index], list_state[index]

        return tuple(list_state)

    def goal_test(self, state):
        return state == self._goal_state

    def step_cost(self, state, action):
        current_index = state.index('*')
        target_index = current_index + self._action_values[action]

        target_sybmol = get_map_symbol(target_index)

        if target_sybmol in string.ascii_uppercase:
            return 0

        step_cost_map = {
            '=': 1,  # cars road
            '-': 2,  # passengers road
            'x': 3,  # crossing
            '$': 4,  # car slow down
        }

        return step_cost_map[target_sybmol]

    def heuristic(self, state):
        if self._heuristic == 'MAN':
            return abs(state.index('*') - self._goal_state.index('*'))

        elif self._heuristic == 'EUC':
            currnet_x, current_y = compute_map_xy(
                self._encoded_map, state.index('*'))
            target_x, target_y = compute_map_xy(
                self._encoded_map, self._goal_state.index('*'))

            return ((target_x - currnet_x) ** 2 + (target_y - current_y) ** 2) ** 0.5

        else:
            return 1
