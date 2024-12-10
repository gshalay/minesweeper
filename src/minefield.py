import numpy

class Minefield():
    def __init__(self, num_cols, num_rows):
      self.num_cols = num_cols
      self.num_rows = num_rows
      self.board = self._create_board()

    def _create_board(self):
      board = numpy.full((self.num_rows, self.num_cols), 0, dtype = int)
        
      return board

    
  
         
