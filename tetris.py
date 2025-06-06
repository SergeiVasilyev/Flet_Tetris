from datetime import datetime
import random
from tetrominoes import TETROMINOES
from settings import *
from data_rw import load_data, save_data


class Block:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def is_block_inside_board(self):
        """Check if the block is inside the game board."""
        return self.x in range(BOARD_WIDTH) and self.y in range(BOARD_HEIGHT)


class Tetromino:
    def __init__(self, element_name: str):
        if element_name not in TETROMINOES:
            raise ValueError(f"{element_name} is not a valid Tetromino element name.")

        self.tetromino = TETROMINOES[element_name]
        self.row = -1
        self.col = BOARD_WIDTH // 2
        self.orientation = 0

    def is_shape_inside_board(self) -> bool:
        """Check if the entire shape is inside the board."""
        for block in self.shape():
            if not block.is_block_inside_board():
                return False
        return True

    def rotate(self, back=False, rotate_direction=1) -> int:
        """Rotate the orientation of the object by 90 degrees in the specified direction.
        :param back: a boolean indicating whether to rotate in the opposite direction (default is False)
        :return: the new orientation value after rotation
        """
        direction = 1 * rotate_direction if back else -1 * rotate_direction
        self.orientation = (self.orientation + direction) % 4
        return self.orientation

    def shape(self) -> list:
        """Returns a list of Block objects representing the shape of the tetromino at its current orientation."""
        return [Block(self.col + x, self.row + y) for x, y in self.tetromino[self.orientation]]

    

class TetrominoGenerator:
    def __init__(self, cart=None):
        self._cart = cart

    @property
    def cart(self) -> list:
        """Generate a cart by randomly choosing two elements from the TETROMINOES list."""
        if not self._cart:
            return [random.choice([*TETROMINOES]) for _ in range(2)]
        return self._cart
    
    @cart.setter
    def cart(self, cart):
        self._cart = cart

    def add_next_tetromino(self) -> Tetromino:
        """Gets first element from the cart, removes it from the cart and return the new Tetromino object based on the first element.
        After that, add a new element to the cart"""
        next_tetramino, self.cart = self.cart[0], self.cart[1:] + [random.choice([*TETROMINOES])]
        return Tetromino(next_tetramino)

    def get_next_tetromino(self) -> Tetromino:
        """Return the next Tetromino object based on the first element in the cart."""
        return Tetromino(self.cart[0])


class Status:
    INIT = 0
    RUNNING = 1
    GAME_OVER = 2

class Game:
    def __init__(self, status=Status.INIT):
        self.status = status
        self.tetromino_generator = TetrominoGenerator()
        self.board = [[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]
        self.next_tetromino_board = [Block(x, y) for x in range(4) for y in range(2)]
        self.current_tetromino = self.tetromino_generator.add_next_tetromino()
        self.next_tetromino = self.tetromino_generator.get_next_tetromino()
        self.hiscore = self.hiscore_rw
        self._date = None
        self.lines = 0
        self.score = 0
        self.level = 1
        self.delay = 1
        self.speed = 1
        self.rotate_direction = 1
        self.delete_full_lines_list = []


    def inits(self):
        self.__init__(Status.RUNNING)


    @property
    def hiscore_rw(self) -> int:
        """
        This function is a property method that returns the highest score from the read_score object. 
        It does not take any parameters and returns an integer value representing the highest score, or 0 if the read_score object is empty.
        """
        obj = load_data(HIGHSCORE_FILE)
        try:
            score = obj['score']
        except:
            score = 0
        return score
    
    @hiscore_rw.setter
    def hiscore_rw(self, score):
        """Setter function for updating the high score in the game."""
        obj = {
            'name': 'Tetris',
            'score': score,
            'date': f"{datetime.now()}"
        }
        save_data(HIGHSCORE_FILE, obj)

    @property
    def date(self):
        return self._date
    
    @date.setter
    def date(self, val):
        self._date = val
    
    def save_game(self) -> bool:
        """
        Save the current game state to a file, including date, board, score, level, lines, delay, speed, and rotation direction.

        Returns:
            bool: True if the game state was successfully saved, False otherwise.
        """
        self.date = str(datetime.now())
        obj = {
            "date": self.date,
            "board": self.board,
            "score": self.score,
            "level": self.level,
            "lines": self.lines,
            "delay": self.delay,
            "speed": self.speed,
            "direction": self.rotate_direction
        }
        if save_data(GAME_STATE_FILE, obj):
            return True
        else:
            return False
        
    
    def load_game(self) -> bool:
        """
        Load the game state from a file and update the game object with the loaded data.

        :return: True if the game state was successfully loaded and updated, False otherwise
        """
        obj = load_data(GAME_STATE_FILE)
        try:
            self.date = obj['date']
            self.board = obj['board']
            self.score = obj['score']
            self.level = obj['level']
            self.lines = obj['lines']
            self.delay = obj['delay']
            self.speed = obj['speed']
            self.status = Status.RUNNING
            return True
        except:
            return False

    def new_tetromino(self) -> None:
        """
        Creates a new tetromino and sets its initial row to -1. 
        Retrieves the next tetromino from the tetromino generator and assigns it to the current tetromino. 
        Retrieves the following tetromino from the tetromino generator.
        """
        self.current_tetromino.row = -1
        self.current_tetromino = self.tetromino_generator.add_next_tetromino()
        self.next_tetromino = self.tetromino_generator.get_next_tetromino()
        

    def left(self):
        """Move the tetromino left if the left condition does not cause a collision."""
        if not self.collision_check([self.left_condition, self.board_condition], col=-1):
            self.current_tetromino.col -= 1


    def right(self):
        """Move the current tetromino to the right, if there is no collision with the right condition."""
        if not self.collision_check([self.right_condition, self.board_condition], col=1):
            self.current_tetromino.col += 1
            

    def down(self):
        """Move the tetromino down by one row if there is no collision, otherwise drop the tetromino and create a new one."""
        if not self.collision_check([self.bottom_condition, self.board_condition], row=1):
            self.current_tetromino.row += 1
        else:
            self.dropped()
            self.new_tetromino()


    def collision_check(self, list_of_condition_collisions=[], row=0, col=0) -> bool:
        """
        Check for collisions with the current tetromino at the specified row and column using the provided list of collision conditions.

        :param list_of_condition_collisions: List of collision condition functions
        :param row: This row is added to the current position of the tetromino blocks to check for collision at the next position.
        :param col: This column is added to the current position of the tetromino blocks to check for collision at the next position.
        :return: True if collision is detected, False otherwise
        """
        for block in self.current_tetromino.shape():
            if any(fn(block, row, col) for fn in list_of_condition_collisions):
                return True
        return False
    
    def bottom_condition(self, block, row, _) -> bool:
        """Check if the tetromino block is at the bottom of the board."""
        return block.y+row >= BOARD_HEIGHT
    
    def board_condition(self, block, row, col) -> bool:
        """Check if the tetromino block is inside the board."""
        return block.is_block_inside_board() and self.board[block.y+row][block.x+col] == 1
    
    def left_condition(self, block, _, col) -> bool:
        """Check if the tetromino block is at the left edge of the board."""
        return block.x+col < 0
    
    def right_condition(self, block, _, col) -> bool:
        """Check if the tetromino block is at the right edge of the board."""
        return block.x+col >= BOARD_WIDTH


    def rotate(self):
        """Rotate the current tetromino and adjust its position to avoid collisions."""
        self.current_tetromino.rotate(back=False, rotate_direction=self.rotate_direction)
        if not self.collision_check([self.bottom_condition, self.board_condition]):
            while self.collision_check([self.left_condition]):
                self.current_tetromino.col += 1
            while self.collision_check([self.right_condition]):
                self.current_tetromino.col -= 1
        else:
            self.current_tetromino.rotate(back=True, rotate_direction=self.rotate_direction)

    def dropped(self):
        """Update board and score after a piece has been dropped."""
        
        if not self.current_tetromino.is_shape_inside_board() and self.current_tetromino.row > 0:
            raise ValueError("Tetromino is out of the board")
        
        # Set the current tetromino to the board
        for block in self.current_tetromino.shape():
            self.board[block.y][block.x] = 1

        # If the board is full, end the game
        if any(self.board[0]):
            self.status = Status.GAME_OVER

        # Update the score
        self.score += 10
        self.clear_full_lines()
        
        # Update the high score
        if self.score > self.hiscore:
            # save_score('Tetris', self.score)
            obj = {
                'name': 'Tetris',
                'score': self.score,
                'date': f"{datetime.now()}"
            }
            save_data(HIGHSCORE_FILE, obj)
            self.hiscore = self.score
        
    

    def clear_full_lines(self):
        """Clears full lines in the game board and updates the score, lines, level, delay, and speed accordingly."""
        lines = 0
        self.delete_full_lines_list = []
        for y in range(BOARD_HEIGHT):
            if sum(self.board[y]) == BOARD_WIDTH:
                self.board.pop(y)
                self.board.insert(0, [0] * BOARD_WIDTH)
                lines += 1
                self.delete_full_lines_list.append(y)
                              
        self.lines += lines
        self.score += 100 * lines**2 + ((self.level-1) * 10) 
        self.level = 1 + self.lines // 10
        self.delay = max(0.1, 1.0 - (self.lines // 20) * 0.1)
        self.speed = 1 + self.lines // 20

