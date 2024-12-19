import unittest
import sys
import os
import numpy as np

# Add src to path.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from minefield import Minefield
from difficulty import Difficulty
from constants import *
from cell_state import CellState

class TestMinefield(unittest.TestCase):
    def test_init(self):
        field1 = Minefield(Difficulty.EASY)
        field2 = Minefield(Difficulty.MEDIUM)
        field3 = Minefield(Difficulty.HARD)
        field4 = Minefield(Difficulty.EXTREME)
        field5 = Minefield(Difficulty.CUSTOM, 3, 3, 4)
        
        self.assertEqual(field1.num_rows, EASY_ROWS)
        self.assertEqual(field1.num_cols, EASY_COLS)
        self.assertEqual(field1.num_mines, EASY_NUM_MINES)
        
        self.assertEqual(field2.num_rows, MED_ROWS)
        self.assertEqual(field2.num_cols, MED_COLS)
        self.assertEqual(field2.num_mines, MED_NUM_MINES)
        
        self.assertEqual(field3.num_rows, HARD_ROWS)
        self.assertEqual(field3.num_cols, HARD_COLS)
        self.assertEqual(field3.num_mines, HARD_NUM_MINES)
        
        self.assertEqual(field4.num_rows, EXP_ROWS)
        self.assertEqual(field4.num_cols, EXP_COLS)
        self.assertEqual(field4.num_mines, EXP_NUM_MINES)
        
        self.assertEqual(field5.num_rows, 3)
        self.assertEqual(field5.num_cols, 3)
        self.assertEqual(field5.num_mines, 4)
    
    def test_create_board(self):
        field = Minefield(Difficulty.CUSTOM, 4, 4, 6)
        field2 = Minefield(Difficulty.CUSTOM, 8, 6, 12)
        
        self.assertEqual(field.board.size, 16)
        self.assertEqual(field2.board.size, 48)
        
    def test_place_mines(self):
        field1 = Minefield(Difficulty.EASY)
        field2 = Minefield(Difficulty.MEDIUM)
        field3 = Minefield(Difficulty.HARD)
        field4 = Minefield(Difficulty.EXTREME)
        field5 = Minefield(Difficulty.CUSTOM, 3, 3, 4)
        
        mines1 = np.array([[cell.value for cell in row] for row in field1.board]).flatten()
        mines2 = np.array([[cell.value for cell in row] for row in field2.board]).flatten()
        mines3 = np.array([[cell.value for cell in row] for row in field3.board]).flatten()
        mines4 = np.array([[cell.value for cell in row] for row in field4.board]).flatten()
        mines5 = np.array([[cell.value for cell in row] for row in field5.board]).flatten()

        # Create a mask where CellState is not unopened
        mask1 = mines1 == MINE_VAL
        mask2 = mines2 == MINE_VAL
        mask3 = mines3 == MINE_VAL
        mask4 = mines4 == MINE_VAL
        mask5 = mines5 == MINE_VAL
        
        self.assertEqual(np.sum(mask1), EASY_NUM_MINES)
        self.assertEqual(np.sum(mask2), MED_NUM_MINES)
        self.assertEqual(np.sum(mask3), HARD_NUM_MINES)
        self.assertEqual(np.sum(mask4), EXP_NUM_MINES)
        self.assertEqual(np.sum(mask5), 4)
        
    def test_is_solved(self):
        field1 = Minefield(Difficulty.CUSTOM, 3, 3, 1)
        field2 = Minefield(Difficulty.CUSTOM, 2, 2, 1)
        
        # Check negative cases.
        self.assertFalse(bool(field1.is_solved()))
        self.assertFalse(bool(field2.is_solved()))
        
        # Modify board states to be in a solved state.
        field1.board[0, 0].value = field1.board[0, 1].value = field1.board[0, 2].value = field1.board[1, 0].value = field1.board[1, 1].value = field1.board[1, 2].value = field1.board[2, 0].value = field1.board[2, 1].value = 0 
        field1.board[2, 2].value = MINE_VAL
        
        field2.board[0, 0].value = field2.board[0, 1].value = field2.board[1, 0].value = 0 
        field2.board[1, 1].value = MINE_VAL
        
        field1.board[0, 0].state = field1.board[0, 1].state = field1.board[0, 2].state = field1.board[1, 0].state = field1.board[1, 1].state = field1.board[1, 2].state = field1.board[2, 0].state = field1.board[2, 1].state = CellState.OPENED
        field2.board[0, 0].state = field2.board[0, 1].state = field2.board[1, 0].state = CellState.OPENED
        
        self.assertTrue(bool(field1.is_solved()))
        self.assertTrue(bool(field2.is_solved()))
        
    def test_count_adjacent_mines(self):
        field = Minefield(Difficulty.CUSTOM, 3, 3, 4)
        
        field.board[0, 0].value = field.board[0, 2].value = field.board[1, 1].value = field.board[2, 0].value = field.board[2, 2].value = 0
        field.board[0, 1].value = field.board[1, 0].value = field.board[1, 2].value = field.board[2, 1].value = MINE_VAL

        self.assertEqual(field.count_adjacent_mines(0, 0), 2)
        self.assertEqual(field.count_adjacent_mines(0, 1), 2)
        self.assertEqual(field.count_adjacent_mines(0, 2), 2)
        self.assertEqual(field.count_adjacent_mines(1, 0), 2)
        self.assertEqual(field.count_adjacent_mines(1, 1), 4)
        self.assertEqual(field.count_adjacent_mines(1, 2), 2)
        self.assertEqual(field.count_adjacent_mines(2, 0), 2)
        self.assertEqual(field.count_adjacent_mines(2, 1), 2)
        self.assertEqual(field.count_adjacent_mines(2, 2), 2)

    # Checks if the solution and obfuscated board are generated properly.
    def test_solutions(self):
        field = Minefield(Difficulty.CUSTOM, 3, 3, 4)
        
        field.board[0, 0].value = field.board[0, 2].value = field.board[1, 1].value = field.board[2, 0].value = field.board[2, 2].value = 0
        field.board[0, 1].value = field.board[1, 0].value = field.board[1, 2].value = field.board[2, 1].value = MINE_VAL

        field.place_adjacencies()
        field._obfuscate_board()
        
        solution = "\t[ 2, -2,  2]\n\t[-2,  4, -2]\n\t[ 2, -2,  2]\n"      
        obfuscated = "\t[U|U|U]\n\t[U|U|U]\n\t[U|U|U]\n"
        
        self.assertEqual(field.print_solution(), solution)
        self.assertEqual(str(field), obfuscated)
        

if(__name__ == "__main__"):
    unittest.main()