from cell_state import CellState
from constants import *

class Cell():
    state = CellState.UNOPENED
    value = BLANK_VAL

    def __init__(self):
      return
      
    def is_mine(self):
      return self.value == MINE_VAL
    
    def is_blank(self):
      return self.value == 0
