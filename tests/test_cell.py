import unittest
import sys
import os

# Add src to path.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from cell import Cell
from cell_state import CellState
from constants import *

class TestMinefield(unittest.TestCase):
    def test_init(self):
        cell1 = Cell()
        self.assertEqual(cell1.state, CellState.UNOPENED)
        self.assertEqual(cell1.value, BLANK_VAL)
        
    def test_is_mine(self):
        actual1 = Cell()
        actual2 = Cell()
        
        actual2.value = MINE_VAL
        
        self.assertTrue(actual1.is_mine())
        self.assertFalse(actual2.is_mine())

    def test_is_mine(self):
        actual1 = Cell()
        actual2 = Cell()
        
        actual2.value = MINE_VAL
        
        self.assertTrue(actual1.is_blank())
        self.assertFalse(actual2.is_blank())
        

if(__name__ == "__main__"):
    unittest.main()