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
          
    def init(self, num_rows, num_cols, num_mines):
      self.num_cols = num_cols
      self.num_rows = num_rows
      self.num_mines = num_mines
      self.board = self._create_board()
      self.place_mines()
      self.place_adjacencies()
      self.obfuscated_board = self._obfuscate_board()
      
      print(self)

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
    
    def is_mine(self, i, j):
      return (self.board[i][j].value == MINE_VAL) 
    
    def count_adjacent_mines(self, i, j):
      # Total of 8 possible locations for a mine to be for each cell.
      adjacent_mines = 0
      
      ## Top Row
      # Top Left
      if(i - 1 >= 0 and j - 1 >= 0 and self.is_mine(i - 1, j - 1)):
        adjacent_mines += 1
        
      # Top Middle
      if(i in range(0, self.num_rows) and j - 1 in range(0, self.num_cols) and self.is_mine(i, j - 1)):
        adjacent_mines += 1
        
      # Top Right
      if(i + 1 in range(0, self.num_rows) and j - 1 in range(0, self.num_cols) and self.is_mine(i + 1, j - 1)):
        adjacent_mines += 1
        
      ## Middle Row
      # Middle Left
      if(i - 1 in range(0, self.num_rows) and j in range(0, self.num_cols) and self.is_mine(i - 1, j)):
        adjacent_mines += 1
      
      # Middle Right
      if(i + 1 in range(0, self.num_rows) and j in range(0, self.num_cols) and self.is_mine(i + 1, j)):
        adjacent_mines += 1
        
      ## Bottom Row  
      # Bottom Left
      if(i - 1 in range(0, self.num_rows) and j + 1 in range(0, self.num_cols) and self.is_mine(i - 1, j + 1)):
        adjacent_mines += 1
        
      # Bottom Middle
      if(i in range(0, self.num_rows) and j + 1 in range(0, self.num_cols) and self.is_mine(i, j + 1)):
        adjacent_mines += 1
        
      # Bottom Right
      if(i + 1 in range(0, self.num_rows) and j + 1 in range(0, self.num_cols) and self.is_mine(i + 1, j + 1)):
        adjacent_mines += 1
      
      return adjacent_mines
      
    def place_adjacencies(self):
      for i in range(0, self.num_rows):
        for j in range(0, self.num_cols):
          if(self.board[i][j].value != MINE_VAL):
            self.board[i][j].value = self.count_adjacent_mines(i, j)
        
    def _create_board(self):
      return np.array([[Cell() for _ in range(self.num_cols)] for _ in range(self.num_rows)], dtype=Cell)
    
    def open_coord(self, i, j):
      self.board[i, j].state = CellState.OPENED
      
      if(self.board[i, j] == BLANK_VAL):
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
      
    def __str__(self):
      rep = "[\n"
      
      for i in range(0, self.num_rows):
        rep += "\t["
        for j in range(0, self.num_cols):
          rep += str(self.board[i][j].value).rjust(2, " ")

          if(j < self.num_cols - 1):
            rep += ", "

        rep += "]\n"

      rep += "]\n\n"
      rep += "[\n"
      
      for i in range(0, self.num_rows):
        rep += "\t["
        for j in range(0, self.num_cols):
          rep += " "

          if(j < self.num_cols - 1):
            rep += "|"

        rep += "]\n"

      rep += "]"

      return rep