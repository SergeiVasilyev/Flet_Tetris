import asyncio
import random
from tetrominoes import TETROMINOES, EL_T, EL_L, EL_J, EL_O, EL_I, EL_S, EL_Z
from settings import *
import time
from data_rw import read_score, save_score


class Block:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def is_block_inside_board(self):
        return self.x in range(BOARD_WIDTH) and self.y in range(BOARD_HEIGHT)


class Tetromino:
    def __init__(self, element_name):
        self.tetromino = TETROMINOES[element_name]
        self.row = -1
        self.col = BOARD_WIDTH // 2
        self.orientation = 0
        self.dropped = False

    def is_shape_inside_board(self):
        for block in self.shape():
            if not block.is_block_inside_board():
                return False
        return True

    def rotate(self, back=False):
        direction = 1 if back else -1
        self.orientation = (self.orientation + direction) % 4
        return self.orientation

    def shape(self):
        # for x, y in self.tetromino:
        #     yield Block(self.col + x, self.row + y)
        return [Block(self.col + x, self.row + y) for x, y in self.tetromino[self.orientation]]

    

class TetrominoGenerator:
    def __init__(self, cart=[]):
        self.cart = self.generate_cart() if not cart else cart

    def generate_cart(self):
        cart = [random.choice([*TETROMINOES]) for _ in range(2)]
        return cart
    
    def add_next_tetromino(self):
        next = self.cart.pop(0)
        self.cart += self.generate_cart()
        return Tetromino(next)
    
    def get_next_tetromino(self):
        return Tetromino(self.cart[0])

class Status:
    INIT = 0
    RUNNING = 1
    GAME_OVER = 2

class Game:
    def __init__(self):
        self.status = Status.INIT
        self.board = []
        self.lines = 0
        self.score = 0
        self.level = 1
        self.delay = 1
        self.speed = 1
        self.hiscore = self.read_hiscore()
        self.current_tetromino = None
        self.next_tetromino = None

    def inits(self):
        self.status = Status.RUNNING
        self.tetromino_generator = TetrominoGenerator()
        self.board = [[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]
        self.current_tetromino = self.tetromino_generator.add_next_tetromino()
        self.next_tetromino = self.tetromino_generator.get_next_tetromino()
        self.lines = 0
        self.score = 0
        self.level = 1
        self.delay = 1
        self.speed = 1
    

    def read_hiscore(self):
        obj = read_score()
        if obj:
            return obj['score']
        return 0


    def running(self):
        if not self.current_tetromino:
            self.current_tetromino = self.tetromino_generator.add_next_tetromino()
            self.next_tetromino = self.tetromino_generator.get_next_tetromino()
            self.current_tetromino.row = -1
        if self.current_tetromino:
            self.down()
    
    def new_tetromino(self):
        self.current_tetromino.row = -1
        self.current_tetromino = self.tetromino_generator.add_next_tetromino()
        self.next_tetromino = self.tetromino_generator.get_next_tetromino()
        
    def left(self):
        if not self.collision(col=-1):
            self.current_tetromino.col -= 1

    def right(self):
        if not self.collision(col=1):
            self.current_tetromino.col += 1
            
    def down(self):
        if not self.collision(row=1):
            self.current_tetromino.row += 1
        else:
            self.dropped()
            self.new_tetromino()

    def collision(self, row=0, col=0):
        for block in self.current_tetromino.shape():
            if block.y+row >= BOARD_HEIGHT:
                return True
            elif block.x+col < 0 or block.x+col >= BOARD_WIDTH:
                return True
            elif block.is_block_inside_board() and self.board[block.y+row][block.x+col] == 1: # Have to check if block is inside board first
                return True
        return False
    
    def left_collision(self):
        for block in self.current_tetromino.shape():
            if block.x < 0:
                return True
        return False
    
    def right_collision(self):
        for block in self.current_tetromino.shape():
            if block.x >= BOARD_WIDTH:
                return True
        return False
    
    def bottom_or_board_collision(self):
        for block in self.current_tetromino.shape():
            board_cell = 0
            if block.is_block_inside_board():
                board_cell = self.board[block.y][block.x]
            if block.y >= BOARD_HEIGHT or board_cell == 1: #  or block.y < 0 to lock rotation when a piece is on top outside the board
                return True
        return False

    def rotate(self):
        self.current_tetromino.rotate()
        if not self.bottom_or_board_collision():
            while self.left_collision():
                self.current_tetromino.col += 1
            while self.right_collision():
                self.current_tetromino.col -= 1
        else:
            self.current_tetromino.rotate(back=True)

    def dropped(self):
        for block in self.current_tetromino.shape():
            self.board[block.y][block.x] = 1
            if sum(self.board[0]) > 0:
                self.status = Status.GAME_OVER
        self.score += 10
        self.clear_full_lines()
        if self.score > self.hiscore:
            save_score('Tetris', self.score)
        self.hiscore = self.read_hiscore()
        
    

    def clear_full_lines(self):
        lines = 0
        for y in range(BOARD_HEIGHT):
            if sum(self.board[y]) == BOARD_WIDTH:
                self.board.pop(y)
                self.board.insert(0, [0] * BOARD_WIDTH)
                lines += 1
                              
        self.lines += lines
        self.score += 100 * lines**2 + ((self.level-1) * 10)
        self.level = 1 + self.lines // 10
        self.delay = 1.0 - self.lines // 20 * 0.1
        self.speed = 1 + self.lines // 20


if __name__ == "__main__":
    start_time = time.time()

    t = TetrominoGenerator()
    print(t.cart)
    tetris = t.add_next_tetromino()
    for block in tetris.shape():
        print(block.x, block.y)
    
    print(tetris.rotate())

    for block in tetris.shape():
        print(block.x, block.y)

    game = Game()
    game.inits()
    print(game.board)

    for n in range(38):
        game.down()
        print(game.current_tetromino.row)
        # if game.collision(row=1):
        #     game.dropped()
        #     game.new_tetromino()
        # print(game.board)

    # Check what happen if tetromino has block outside board
    t = TetrominoGenerator(cart=['I', 'O'])
    tetris = t.add_next_tetromino()
    tetris.rotate()
    game.board[-2][5] = 1
    print(game.board)
    for n in tetris.shape():
        print(n.x, n.y) 
        print(n.is_block_inside_board())


    end_time = time.time()
    print(end_time - start_time)