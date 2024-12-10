class Cell():
    def __init__(self, col, row, state):
      self.col = col
      self.row = row
      self.state = state

    def _create_board(self):
      board = []  
      for i in range(0, self.num_rows):
        row = [] 
        for j in range(0, self.num_cols):
          row.append(0)
    
      board.append(row)
      return board

    