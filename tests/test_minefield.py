import unittest
import sys
import os

# Add src to path.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from minefield import Minefield
from difficulty import Difficulty
from constants import *

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
        

if(__name__ == "__main__"):
    unittest.main()