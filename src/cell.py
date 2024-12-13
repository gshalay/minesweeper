from cell_state import CellState

class Cell():
    def __init__(self, value):
      self.state = CellState.UNOPENED
      self.value = value

    def __eq__(self, otherCell):
      return (self.state == otherCell.state and self.value == otherCell.value)
    
    def getState(self):
      return self.state
    
    def setState(self, state):
      self.state = state
    
    def getValue(self):
      return self.state
    
    def setValue(self, value):
      self.value = value