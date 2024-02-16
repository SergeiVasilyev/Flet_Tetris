from functools import reduce
from settings import *
from initialization import background, init, generate_element
from tetrominoes import TETROMINOES, EL_Z

board = init()
main_container = background()
tetramino = TETROMINOES[generate_element()]
# tetramino = EL_Z


def draw(drawing):
    global board, tetromino_blocks_positions, row_position, col_position, tetramino
    tetromino_blocks_positions = []
    print(tetramino)
    for x, y in tetramino:
        board[y+row_position][x+col_position] = 1 if drawing else 0
        tetromino_blocks_positions.append([(y+row_position)*10+(x+col_position), y+row_position, x+col_position])
    return board

def vertical_collision():
    global tetromino_blocks_positions
    for i in tetromino_blocks_positions:
        if i[1] >= 19:
            return True
        elif board[i[1]+1][i[2]] == -1:
            return True
    return False

def mark_as_dropped():
    for j in tetromino_blocks_positions:
        board[j[1]][j[2]] = -1 # mark as dropped

def horizontal_collision(x):
    for i in tetromino_blocks_positions:
        if x + i[2] < 0 or x + i[2] > 9:
            return True
    return False

def element_length(tetramino):
    max_len = 0
    res = reduce(lambda x, y: [x[i] or y[i] for i in range(len(x))], tetramino)
    max_len = sum(res)
    return max_len

def is_full():
    if -1 in board[1]:
        return True
    return False

def path_correction(new_element):
    global tetramino, col_position, row_position
    for el in new_element:
        if el[0] + col_position > 9:
            col_position = 9 - el[0]
        elif el[0] + col_position < 0:
            col_position = 0 - el[0]
        elif el[1] + row_position > 19:
            row_position = 19 - el[1]
        elif el[1] + row_position < 0:
            row_position = 0 - el[1]
    return new_element