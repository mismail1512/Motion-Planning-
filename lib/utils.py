import json
import lib.settings as set_man

_ZC_ROAD_MAP = '''
###############################
#############A#################
###====$$===========$$======###
###=########==########====#####
###==#######==#########=#######
###=########$$#########=#######
#F==########==#####-----H---B##
##==########==#####I---------##
##==########==#####----------##
##==###-====xx=====---#####==##
##$$-#--====G======---#####$$##
##==-#--=--#####--=---#####==##
##==-#-=L--#####--K=--#####==##
#Exx-#==##-#####-##===#####xxC#
#===--==##-#####-##===#####==-#
#$$=-#=======J========#####$$-#
#===-#--===#####===---#####==-#
#==M-#--===#####====-----##==-#
#==--======#####==========P==-#
#==N-#--===========---####-==-#
#==----------==-----######-==-#
#==---###----xx---########-==-#
#==--#####====================#
#############D#################
###############################
'''

ZC_DRAW_MAP = '''
###############################
#############A#################
###                         ###
### ########  #########  ######
###  #######  ######### #######
### ########  #########  ######
#F  ########  #####     H   B##
##  ########  #####I         ##
##  ########  #####          ##
##  ########          ###### ##
##   #       G        ###### ##
##   #     #####      ###### ##
##   #  L  #####  K   ###### ##
#E   # ### ##### ###  ###### C#
#      ### ##### ###  ######  #
#    #       J        ######  #
#    #     #####      ######  #
#  M #     #####         ###  #
#          #####          P   #
#  N #                ####    #
#                   ######    #
#     ###         ########    #
#    #####                    #
#############D#################
###############################
'''


_encoded_map_width = -1
_encoded_map_height = -1
_visualizer_step_counter = 0


def create_zc_map_state(location: str, distantiation: str):
    settings = set_man.get_settings()
    location_symbol = settings['map_symbols'][location]
    distentaion_symbol = settings['map_symbols'][distantiation]

    return _ZC_ROAD_MAP.replace('=', ' ').replace(
        '-', ' ').replace('$', ' ').replace('x', ' ').replace(location_symbol, '*').replace(distentaion_symbol, '+')


def get_map_width(map_encoding: str):
    global _encoded_map_width

    if _encoded_map_width == -1:
        map_lines = [line for line in map_encoding.split('\n') if line != '']
        _encoded_map_width = len(map_lines[0])

    return _encoded_map_width


def get_map_height(map_encoding: str):
    global _encoded_map_height

    if _encoded_map_height == -1:
        map_lines = [line for line in map_encoding.split('\n') if line != '']
        _encoded_map_height = len(map_lines)

    return _encoded_map_height


def get_map_symbol(index):
    flat_zc_map = _ZC_ROAD_MAP.replace('\n', '')
    return tuple(flat_zc_map)[index]


def compute_map_xy(map_encoding: str, index):
    y = index // get_map_width(map_encoding)
    x = index - y * get_map_width(map_encoding) - 1

    return (x, y)


def visualize(map_encoding: str, frontier: list):
    global _visualizer_step_counter

    _visualizer_step_counter += 1
    print(f"frontier at step {_visualizer_step_counter}")

    for _, _, node in frontier:
        print()

        for i in range(0, get_map_width(map_encoding) * get_map_height(map_encoding), get_map_width(map_encoding)):
            print(' '.join(node.state[i:i + get_map_width(map_encoding)]))

        print('-' * 100)


def draw_road_map(location, actions: list[str]):
    pivot_x = -1
    pivot_y = -1
    map_grid = []

    if ',' in location:
        pivot_x, pivot_y = (
            int(location.split(',')[1]), int(location.split(',')[0]))

        map_grid = [[char for char in line]
                    for line in ZC_DRAW_MAP.split('\n') if line != '']

    else:
        settings = set_man.get_settings()
        location_symbol = settings['map_symbols'][location]
        start_index = tuple(ZC_DRAW_MAP.replace(
            '\n', '')).index(location_symbol)

        pivot_x, pivot_y = compute_map_xy(ZC_DRAW_MAP, start_index)

        map_grid = [[char for char in line] for line in ZC_DRAW_MAP.replace(
            location_symbol, '*').split('\n') if line != '']

    for action in actions:
        if action == 'up':
            pivot_y -= 1
            map_grid[pivot_y][pivot_x] = '|'

        elif action == 'down':
            pivot_y += 1
            map_grid[pivot_y][pivot_x] = '|'

        elif action == 'left':
            pivot_x -= 1
            map_grid[pivot_y][pivot_x] = '-'

        elif action == 'right':
            pivot_x += 1
            map_grid[pivot_y][pivot_x] = '-'

    # restore symbol after being removed
    map_grid[pivot_y][pivot_x] = '+'

    map_str = '\n'.join([''.join(line_arr) for line_arr in map_grid])

    return map_str


def print_map_xy_grid():
    map_lines = [line for line in ZC_DRAW_MAP.split('\n') if line != '']

    print('  ' + ' '.join([str(i) for i in range(len(map_lines[0]))]))

    for index, line in enumerate(map_lines):
        formatted_line = ' '.join([c for c in line])
        print(f"{index} {formatted_line}")


def create_xy_map_state(location: tuple[int, int], distantiation: tuple[int, int]):
    map_grid = [[char for char in line]
                for line in _ZC_ROAD_MAP.replace('=', ' ').replace(
        '-', ' ').replace('$', ' ').replace('x', ' ').split('\n') if line != '']

    if map_grid[location[0]][location[1]] == '#':
        print('wrong location')
        return None

    if map_grid[distantiation[0]][distantiation[1]] == '#':
        print('wrong distantiation')
        return None

    map_grid[location[0]][location[1]] = '*'
    map_grid[distantiation[0]][distantiation[1]] = '+'

    map_str = '\n'.join([''.join(line_arr) for line_arr in map_grid])

    return map_str


def format_json(json_obj: dict):
    return json.dumps(json_obj, indent=2)
