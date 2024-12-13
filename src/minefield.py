import numpy as np
import random

from constants import *
from difficulty import Difficulty
from cell_state import CellState
from cell import Cell

class Minefield():
    def __init__(self, difficulty):
      match(difficulty):
        case Difficulty.EASY:
          self.init(EASY_COLS, EASY_ROWS, EASY_NUM_MINES)
          return
        case Difficulty.MEDIUM:
          self.init(MED_COLS, MED_ROWS, MED_NUM_MINES)
          return
        case Difficulty.HARD:
          self.init(HARD_COLS, HARD_ROWS, HARD_NUM_MINES)
          return
        case Difficulty.EXTREME:
          self.init(EXP_COLS, EXP_ROWS, EXP_NUM_MINES)
          return
        case Difficulty.CUSTOM:
          print("Custom mode not yet supported.")
          return NotImplementedError
        case _:
          raise Exception("Unknown difficulty.")
          
    def init(self, num_cols, num_rows, num_mines):
      self.num_cols = num_cols
      self.num_rows = num_rows
      self.num_mines = num_mines
      self.size = num_cols * num_rows
      self.board = self._create_board()
      self.place_mines()
      self.place_adjacencies()
      
      print("This is the game board after building:")
      print(self.board)
      
    def get_board_pos(self, idx):
      current_idx = idx
      row = 0
      
      while current_idx > self.num_cols:
        current_idx -= self.num_cols
        row += 1
        
      return (current_idx - 1, row) 

    def place_mines(self):
      placed_mines = 0
      
      while placed_mines < self.num_mines:
        mine_placed = False
        
        while not mine_placed:
          rand_idx = random.randint(0, self.size)          
          coord = self.get_board_pos(rand_idx)
          
          if(self.board[coord[0]][coord[1]].getValue() == BLANK_VAL):
            self.board[coord[0]][coord[1]].setValue(MINE_VAL)
            mine_placed = True
            placed_mines += 1
    
    def is_mine(self, i, j):
      return (self.board[i][j].getValue() == MINE_VAL)
    
    def count_adjacent_mines(self, i, j):
      # Total of 8 possible locations for a mine to be for each cell.
      adjacent_mines = 0
      
      ## Top Row
      # Top Left
      if(i - 1 >= 0 and j - 1 >= 0 and self.is_mine(i - 1, j - 1)):
        adjacent_mines += 1
        
      # Top Middle
      if(i in range(0, self.num_cols) and j - 1 in range(0, self.num_rows) and self.is_mine(i, j - 1)):
        adjacent_mines += 1
        
      # Top Right
      if(i + 1 in range(0, self.num_cols) and j - 1 in range(0, self.num_rows) and self.is_mine(i + 1, j - 1)):
        adjacent_mines += 1
        
      ## Middle Row
      # Middle Left
      if(i - 1 in range(0, self.num_cols) and j in range(0, self.num_rows) and self.is_mine(i - 1, j)):
        adjacent_mines += 1
      
      # Middle Right
      if(i + 1 in range(0, self.num_cols) and j in range(0, self.num_rows) and self.is_mine(i + 1, j)):
        adjacent_mines += 1
        
      ## Bottom Row  
      # Bottom Left
      if(i - 1 in range(0, self.num_cols) and j + 1 in range(0, self.num_rows) and self.is_mine(i - 1, j + 1)):
        adjacent_mines += 1
        
      # Bottom Middle
      if(i in range(0, self.num_cols) and j + 1 in range(0, self.num_rows) and self.is_mine(i, j + 1)):
        adjacent_mines += 1
        
      # Bottom Right
      if(i + 1 in range(0, self.num_cols) and j + 1 in range(0, self.num_rows) and self.is_mine(i + 1, j + 1)):
        adjacent_mines += 1
      
      return adjacent_mines
      
    def place_adjacencies(self):
      for i in range(0, self.num_cols):
        for j in range(0, self.num_rows):
          self.board[i][j].setValue(self.count_adjacent_mines(i, j))
        
    def _create_board(self):
      return np.full((self.num_cols, self.num_rows), Cell(BLANK_VAL), dtype = Cell)