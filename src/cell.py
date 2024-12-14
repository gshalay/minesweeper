from cell_state import CellState
from constants import *

class Cell():
    state = CellState.UNOPENED
    value = BLANK_VAL

    def __init__(self):
      return

    def __eq__(self, otherCell):
      return (self.state == otherCell.state and self.value == otherCell.value)