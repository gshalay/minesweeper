import numpy as np
import random

from constants import *
from difficulty import Difficulty
from cell_state import CellState
from cell import Cell

class Minefield():
    def __init__(self, difficulty, num_rows=None, num_cols=None, num_mines=None):
      match(difficulty):
        case Difficulty.EASY:
          self.init(EASY_ROWS, EASY_COLS, EASY_NUM_MINES)
          return
        case Difficulty.MEDIUM:
          self.init(MED_ROWS, MED_COLS, MED_NUM_MINES)
          return
        case Difficulty.HARD:
          self.init(HARD_ROWS, HARD_COLS, HARD_NUM_MINES)
          return
        case Difficulty.EXTREME:
          self.init(EXP_ROWS, EXP_COLS, EXP_NUM_MINES)
          return
        case Difficulty.CUSTOM:
          self.init(num_rows, num_cols, num_mines)
          return
        case _:
          raise Exception("Unknown difficulty.")
          
    def init(self, num_rows, num_cols, num_mines):
      self.num_cols = num_cols
      self.num_rows = num_rows
      self.num_mines = num_mines
      self.board = self._create_board()
      self.place_mines()
      self.place_adjacencies()
      self.obfuscated_board = self._obfuscate_board()

    def place_mines(self):
      placed_mines = 0

      while placed_mines < self.num_mines:
        mine_placed = False
        
        while not mine_placed:
          rand_row_idx = random.randint(0, self.num_rows - 1)
          rand_col_idx = random.randint(0, self.num_cols - 1)

          if(self.board[rand_row_idx][rand_col_idx].value == BLANK_VAL):
            self.board[rand_row_idx, rand_col_idx].value = MINE_VAL
            mine_placed = True
            placed_mines += 1
    
    def count_adjacent_mines(self, i, j):
      # Total of 8 possible locations for a mine to be for each cell.
      adjacent_mines = 0
      
      ## Top Row
      # Top Left
      if(i - 1 >= 0 and j - 1 >= 0 and self.board[i - 1, j - 1].is_mine()):
        adjacent_mines += 1
        
      # Top Middle
      if(i in range(0, self.num_rows) and j - 1 in range(0, self.num_cols) and self.board[i, j - 1].is_mine()):
        adjacent_mines += 1
        
      # Top Right
      if(i + 1 in range(0, self.num_rows) and j - 1 in range(0, self.num_cols) and self.board[i + 1, j - 1].is_mine()):
        adjacent_mines += 1
        
      ## Middle Row
      # Middle Left
      if(i - 1 in range(0, self.num_rows) and j in range(0, self.num_cols) and self.board[i - 1, j].is_mine()):
        adjacent_mines += 1
      
      # Middle Right
      if(i + 1 in range(0, self.num_rows) and j in range(0, self.num_cols) and self.board[i + 1, j].is_mine()):
        adjacent_mines += 1
        
      ## Bottom Row  
      # Bottom Left
      if(i - 1 in range(0, self.num_rows) and j + 1 in range(0, self.num_cols) and self.board[i - 1, j + 1].is_mine()):
        adjacent_mines += 1
        
      # Bottom Middle
      if(i in range(0, self.num_rows) and j + 1 in range(0, self.num_cols) and self.board[i, j + 1].is_mine()):
        adjacent_mines += 1
        
      # Bottom Right
      if(i + 1 in range(0, self.num_rows) and j + 1 in range(0, self.num_cols) and self.board[i + 1, j + 1].is_mine()):
        adjacent_mines += 1
      
      return adjacent_mines
      
    def place_adjacencies(self):
      for i in range(0, self.num_rows):
        for j in range(0, self.num_cols):
          if(self.board[i][j].value != MINE_VAL):
            self.board[i][j].value = self.count_adjacent_mines(i, j)
        
    def _create_board(self):
      return np.array([[Cell() for _ in range(self.num_cols)] for _ in range(self.num_rows)], dtype=Cell)
    
    def flag_coord(self, i, j):
      if(self.bounds_in_range(i, j) and self.board[i, j].state != CellState.OPENED):
        if(self.board[i, j].state == CellState.FLAGGED):
          return False

        self.board[i, j].state = CellState.FLAGGED
        return True
      else:
        return False

    def count_unopened_cells(self):
      ((25 < self.board) & (self.board < 100)).sum()

    def is_solved(self):
      cell_states = np.array([[cell.state for cell in row] for row in self.board]).flatten()

      # Create a mask where CellState is not unopened
      mask = cell_states != CellState.OPENED
      s = np.sum(mask)

      if(np.sum(mask) == self.num_mines):
        print(mask)
        print()
        print(cell_states)
        print()
        print(f"sum: {s}\tmines: {self.num_mines}")

      # Count elements that are not unopened
      return (np.sum(mask) == self.num_mines)


    def open_coord(self, i, j):
      self.board[i, j].state = CellState.OPENED
      
      if(self.board[i, j].value == BLANK_VAL):
        self.reveal_adjacent_blank_cells(i, j)
        return BLANK_VAL
      else:
        return self.board[i, j].value
    
    def bounds_in_range(self, i, j):
      return i in range(self.num_rows) and j in range(self.num_cols)
  
    def reveal_adjacent_blank_cells(self, i, j):
      ## Top Row
      # Top Left
      if(self.bounds_in_range(i - 1, j - 1) and self.board[i - 1, j - 1].state == CellState.UNOPENED):
        self.board[i - 1, j - 1].state = CellState.OPENED
        if(self.board[i - 1, j - 1].value == BLANK_VAL):
          self.reveal_adjacent_blank_cells(i - 1, j - 1)
        
      # Top Middle
      if(self.bounds_in_range(i, j - 1) and self.board[i, j - 1].state == CellState.UNOPENED):
        self.board[i, j - 1].state = CellState.OPENED
        if(self.board[i, j - 1].value == BLANK_VAL):
          self.reveal_adjacent_blank_cells(i, j - 1)
        
      # Top Right
      if(self.bounds_in_range(i + 1, j - 1) and self.board[i + 1, j - 1].state == CellState.UNOPENED):
        self.board[i + 1, j - 1].state = CellState.OPENED
        if(self.board[i + 1, j - 1].value == BLANK_VAL):
          self.reveal_adjacent_blank_cells(i + 1, j - 1)
        
      ## Middle Row
      # Middle Left
      if(self.bounds_in_range(i - 1, j) and self.board[i - 1, j].state == CellState.UNOPENED):
        self.board[i - 1, j].state = CellState.OPENED
        if(self.board[i - 1, j].value == BLANK_VAL):
          self.reveal_adjacent_blank_cells(i - 1, j)
      
      # Middle Right
      if(self.bounds_in_range(i + 1, j) and self.board[i + 1, j].state == CellState.UNOPENED):
        self.board[i + 1, j].state = CellState.OPENED
        if(self.board[i + 1, j].value == BLANK_VAL):
          self.reveal_adjacent_blank_cells(i + 1, j)
        
      ## Bottom Row  
      # Bottom Left
      if(self.bounds_in_range(i - 1, j + 1) and self.board[i - 1, j + 1].state == CellState.UNOPENED):
        self.board[i - 1, j + 1].state = CellState.OPENED
        if(self.board[i - 1, j + 1].value == BLANK_VAL):
          self.reveal_adjacent_blank_cells(i - 1, j + 1)
        
      # Bottom Middle
      if(self.bounds_in_range(i, j + 1) and self.board[i, j + 1].state == CellState.UNOPENED):
        self.board[i, j + 1].state = CellState.OPENED
        if(self.board[i, j + 1].value == BLANK_VAL):
          self.reveal_adjacent_blank_cells(i, j + 1)
        
      # Bottom Right
      if(self.bounds_in_range(i + 1, j + 1) and self.board[i + 1, j + 1].state == CellState.UNOPENED):
        self.board[i + 1, j + 1].state = CellState.OPENED
        if(self.board[i + 1, j + 1].value == BLANK_VAL):
          self.reveal_adjacent_blank_cells(i + 1, j + 1)
    
    def _obfuscate_board(self):
      return np.array([[" " for _ in range(self.num_cols)] for _ in range(self.num_rows)], dtype=str)
    
    def get_obfuscated_char(self, i, j):
      match(self.board[i, j].state):
        case CellState.UNOPENED:
          return UNOPENED_CHAR
        case CellState.FLAGGED:
          return FLAGGED_CHAR
        case CellState.OPENED:
          if(self.board[i, j].is_mine()):
            return MINE_CHAR
          elif(self.board[i, j].is_blank()):
            return BLANK_CHAR
          else:
            return str(self.board[i, j].value)
        case _:
          return str(self.board[i, j].value)

    def print_solution(self):
      rep = "[\n"
      
      # Solution representation.
      for i in range(0, self.num_rows):
        rep += "\t["
        for j in range(0, self.num_cols):
          rep += str(self.board[i, j].value).rjust(2, " ")

          if(j < self.num_cols - 1):
            rep += ", "

        rep += "]\n"
      return rep

    def __str__(self):
      rep = ""
      
      for i in range(0, self.num_rows):
        rep += "\t["
        for j in range(0, self.num_cols):
          rep += self.get_obfuscated_char(i, j)

          if(j < self.num_cols - 1):
            rep += "|"

        rep += "]\n"

      return rep