import unittest

from src.minefield import Minefield

class TestMinefield(unittest.TestCase):
    def test_init(self):
        field = Minefield(4, 4)
        self.assertEqual(field.num_cols, 4)
        self.assertEqual(field.num_rows, 5)
    
    def test_create_board(self):
        field = Minefield(4, 4)
        field = Minefield(8, 6)
        self.assertEqual(len(field.board), 16)
        self.assertEqual(len(field.board), 48)
        

if(__name__ == "__main__"):
    unittest.main()