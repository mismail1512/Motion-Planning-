import lib.settings as set_man
from models.problem import problem
from models.zc_map import zc_map
from lib.utils import create_zc_map_state, draw_road_map, print_map_xy_grid, format_json, create_xy_map_state

# solvers
from solvers.greedy_best_first import greedy_best_first
from solvers.a_star import a_star
from solvers.bfs import bfs
from solvers.dfs import dfs
from solvers.ids import ids
from solvers.ucs import ucs
from solvers.simulated_annealing import simulated_annealing
from solvers.hill_climbing import hill_climbing
from solvers.local_beam_search import local_beam_search

print_map_xy_grid()
print(format_json(set_man.get_settings()['map_symbols']))

location = input('enter your current location: ')
distantiation = input('enter your distantiation: ')

init_state: str = None

if ',' in location:
    location_xy = (int(location.split(',')[0]), int(location.split(',')[1]))
    distantiation_xy = (int(distantiation.split(
        ',')[0]), int(distantiation.split(',')[1]))

    init_state = create_xy_map_state(location_xy, distantiation_xy)
else:
    init_state = create_zc_map_state(location, distantiation)

heuristic = 'MAN'
zc_map_problem: problem = zc_map(init_state, heuristic)

solvers_map = {
    'gfs': greedy_best_first,
    'a_star': a_star,
    'bfs': bfs,
    'dfs': dfs,
    'ids': ids,
    'ucs': ucs,
    'sim': simulated_annealing,
    'hill': hill_climbing,
    'local': local_beam_search,
}

print(list(solvers_map.keys()))
solver_key = input('enter solving algorithm: ')
solver = solvers_map[solver_key]
solution = solver(zc_map_problem)
print(draw_road_map(location, solution[0]))
print(solution)
