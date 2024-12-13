import unittest

from src.cell import Cell
from cell_state import CellState

class TestMinefield(unittest.TestCase):
    def test_init(self):
        cell1 = Cell(1, 6, CellState.OPENED)
        cell2 = Cell(2, 3, CellState.UNOPENED)
        cell3 = Cell(4, 5, CellState.FLAGGED)
        
        self.assertEqual(cell1.col, 1)
        self.assertEqual(cell1.row, 6)
        self.assertEqual(cell1.state, CellState.OPENED)
        
        self.assertEqual(cell2.col, 2)
        self.assertEqual(cell2.row, 3)
        self.assertEqual(cell2.state, CellState.UNOPENED)
        
        self.assertEqual(cell3.col, 2)
        self.assertEqual(cell3.row, 3)
        self.assertEqual(cell3.state, CellState.FLAGGED)
        

if(__name__ == "__main__"):
    unittest.main()