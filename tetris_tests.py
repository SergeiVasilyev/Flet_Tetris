import unittest
from tetris import Block, Game, Tetromino, TetrominoGenerator, Status
from tetrominoes import TETROMINOES
from settings import *

class TestBlock(unittest.TestCase):

    def test_is_block_inside_board(self):
        """Test if the block is inside the board by iterating through all possible positions."""
        block = Block(0, 0)
        for x in range(BOARD_WIDTH):
            for y in range(BOARD_HEIGHT):
                block.x = x
                block.y = y
                self.assertTrue(block.is_block_inside_board())
    
    def test_not_is_block_inside_board(self):
        """Test if the block is outside the board
        First iterate starts from BOARD_WIDTH and BOARD_HEIGHT to 50, 50
        Second iterate starts from x=0 and y=0 to -50, -50
        """
        block = Block(0, 0)
        for x in range(BOARD_WIDTH, 50):
            for y in range(BOARD_HEIGHT, 50):
                block.x = x
                block.y = y
                self.assertFalse(block.is_block_inside_board())

        for x in range(0, -50):
            for y in range(0, -50):
                block.x = x
                block.y = y
                self.assertFalse(block.is_block_inside_board())


class TestTetromino(unittest.TestCase):
    def test_shape(self):
        """Test if the shape of the tetromino is a list of Block objects."""
        for el in TETROMINOES:
            tetromino = Tetromino(el)
            self.assertEqual(len(tetromino.shape()), 4)
            for block in tetromino.shape():
                self.assertIsInstance(block, Block)
        self.assertIsInstance(tetromino.shape(), list)
        self.assertIsInstance(tetromino.shape()[0], Block)
    
    def test_not_shape(self):
        """Test if passed element name is not a valid Tetromino element name."""
        self.assertRaises(ValueError, Tetromino, 'wrong_element')
        self.assertRaises(ValueError, Tetromino, 'H')
        self.assertRaises(ValueError, Tetromino, 'Y')

    def test_rotate(self):
        """A test function to validate the rotation functionality of the Tetromino class."""
        tetromino = Tetromino('I')
        # clockwise movement
        for i in range(4):
            self.assertEqual(tetromino.orientation, i)
            tetromino.rotate(back=True)
        # counterclockwise movement
        for i in range(3, 0):
            self.assertEqual(tetromino.orientation, i)
            tetromino.rotate()
        # clockwise movement 2 times
        for i in range(8):
            self.assertEqual(tetromino.orientation, i % 4)
            tetromino.rotate(back=True)

    def test_is_shape_inside_board(self):
        """Function to test if the tetromino shape is inside the board. """
        tetromino = Tetromino('I')
        # [col-1,  0], [ 0,  0], [ 1,  0], [ 2,  0]
        tetromino.row = 0
        tetromino.col = 1
        self.assertTrue(tetromino.is_shape_inside_board())
        tetromino.row = 0
        tetromino.col = 0
        self.assertFalse(tetromino.is_shape_inside_board())

        # [ 0, row-1], [ 0,  0], [ 0,  1], [ 0,  2]
        tetromino.rotate()
        tetromino.row = 1
        tetromino.col = 0
        self.assertTrue(tetromino.is_shape_inside_board())
        tetromino.row = 0
        tetromino.col = 0
        self.assertFalse(tetromino.is_shape_inside_board())

    def test_shape(self):
        tetromino = Tetromino('I')
        self.assertEqual(len(tetromino.shape()), 4)
        self.assertIsInstance(tetromino.shape()[0], Block)


class TestTetrominoGenerator(unittest.TestCase):
    def test_add_next_tetromino(self):
        generator = TetrominoGenerator()
        self.assertIsInstance(generator.cart, list)

        tetromino = generator.add_next_tetromino()
        self.assertIsInstance(tetromino, Tetromino)


    def test_get_next_tetromino(self):
        generator = TetrominoGenerator()
        tetromino = generator.get_next_tetromino()
        self.assertIsInstance(tetromino, Tetromino)



class TestGame(unittest.TestCase):

    def test_create_game(self):
        game = Game()
        self.assertIsInstance(game.tetromino_generator, TetrominoGenerator)
        self.assertIsInstance(game.current_tetromino, Tetromino)
        self.assertIsInstance(game.next_tetromino, Tetromino)

    def test_left(self):
        """Move the current tetromino to the left and check for collisions."""
        game = Game()
        game.current_tetromino.row = 0
        game.current_tetromino.col = 5
        game.left()
        self.assertFalse(game.collision_check([game.left_condition], col=-1))
        game.current_tetromino.col = -1
        game.left()
        self.assertTrue(game.collision_check([game.left_condition], col=-1))

    def test_right(self):
        """Move the current tetromino to the right and check for collisions."""
        game = Game()
        game.current_tetromino.row = 0
        game.current_tetromino.col = 5
        game.right()
        self.assertFalse(game.collision_check([game.right_condition], col=1))
        game.current_tetromino.col = 10
        game.right()
        self.assertTrue(game.collision_check([game.right_condition], col=1))

    def test_down(self):
        """Move the current tetromino down and check for collisions at different positions."""
        game = Game()
        game.current_tetromino = Tetromino('L')
        game.current_tetromino.row = 5
        game.down()
        self.assertFalse(game.collision_check([game.bottom_condition], row=1))
        game.current_tetromino.row = 17
        game.down()
        self.assertTrue(game.collision_check([game.bottom_condition], row=1))
        game.current_tetromino.row = 19
        game.current_tetromino.col = 1
        # print([game.current_tetromino.shape()[i].y for i in range(len(game.current_tetromino.shape()))])
        self.assertRaises(ValueError, game.down)

    def test_dropped(self):
        """Test the dropped method of the Game class."""
        game = Game()
        game.current_tetromino = Tetromino('T')
        game.current_tetromino.row = 19
        self.assertEqual(game.current_tetromino.shape()[2].y, 20) # One block is out of the board
        self.assertRaises(ValueError, game.dropped)
        
        game.current_tetromino = Tetromino('I')
        game.current_tetromino.row = 19
        for i in range(4):
            self.assertEqual(game.current_tetromino.shape()[i].y, 19)
        game.current_tetromino.row = 20
        self.assertRaises(ValueError, game.dropped)

        game.current_tetromino.row = 0
        game.dropped()
        self.assertEqual(game.status, Status.GAME_OVER)

if __name__ == '__main__':
    unittest.main()




