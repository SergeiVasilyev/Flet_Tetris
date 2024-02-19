from functools import reduce
from settings import *
from initialization import Initialization
from tetrominoes import TETROMINOES, EL_Z
import random




class Tetris:
    def __init__(self, main_container, board, tetramino, row_position=-1, col_position=4):
        self.main_container = main_container
        self.board = board
        self.tetramino = tetramino
        self.tetromino_blocks_positions = []
        self.row_position = self.__row_position = row_position
        self.col_position = self.__col_position = col_position
        self.score = 0

    # def init(self):
    #     self.board = None
    #     self.tetramino = None
    #     self.main_container = None
    #     self.tetromino_blocks_positions = []
    #     self.reset_position()
    #     self.refresh_tetromino()

    def generate_element(self):
        return random.choice([*TETROMINOES])
    
    def refresh_tetromino(self):
        self.tetramino = TETROMINOES[self.generate_element()]
        return self.tetramino

    def reset_position(self):
        self.row_position = self.__row_position
        self.col_position = self.__col_position

    def draw(self, drawing):
        self.tetromino_blocks_positions = []
        for x, y in self.tetramino:
            # print(x, y, self.row_position, self.col_position)
            try:
                self.board[y+self.row_position][x+self.col_position] = 1 if drawing else 0
                self.tetromino_blocks_positions.append([(y+self.row_position)*10+(x+self.col_position), y+self.row_position, x+self.col_position])
            except:
                print('error', self.board, x, y, self.row_position, self.col_position)
        return self.board # self

    def vertical_collision(self):
        for i in self.tetromino_blocks_positions:
            if i[1] >= 19:
                return True
            elif self.board[i[1]+1][i[2]] == -1:
                return True
        return False

    def mark_as_dropped(self):
        for j in self.tetromino_blocks_positions:
            self.board[j[1]][j[2]] = -1 # mark as dropped

    def horizontal_collision(self, x): # 1 - right, -1 - left
        for i in self.tetromino_blocks_positions:
            if x + i[2] < 0 or x + i[2] > 9 or self.board[i[1]][x+i[2]] == -1:
                return True
        return False

    def element_length(self):
        max_len = 0
        res = reduce(lambda x, y: [x[i] or y[i] for i in range(len(x))], self.tetramino)
        max_len = sum(res)
        return max_len

    def is_full(self):
        if -1 in self.board[1]:
            return True
        return False

    def path_correction(self, check_element):
        for el in check_element:
            if el[0] + self.col_position > 9:
                self.col_position = 9 - el[0]
            elif el[0] + self.col_position < 0:
                self.col_position = 0 - el[0]
            elif el[1] + self.row_position > 19:
                self.row_position = 19 - el[1]
            elif el[1] + self.row_position < 0:
                self.row_position = 0 - el[1]
        return check_element
    

def save_highscore(score):
    with open('highscore.txt', 'w') as f:
        f.write(str(score))