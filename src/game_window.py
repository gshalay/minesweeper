from window import Window
from tkinter import Frame
from constants import *

class GameWindow(Window):
    def __init__(self, width, height):
        super().__init__(width, height)
        
        info_frame_height = normalize_dim_size(width)
        game_frame_height = normalize_dim_size(height)
        
        # Menu Frame
        # Num Flags, elapsed time, num mines
        info_frame = Frame(self.root, width=width, height=info_frame_height, background="red")
        info_frame.grid(row=0, column=0, padx=8, pady=8)
    
        # Minefield Frame
        field_frame = Frame(self.root, width=width, height=game_frame_height, background="blue")
        field_frame.grid(row=1, column=0, padx=8, pady=8)
    
    # A good ratio for the two frames is 1/8 and 7/8 of window height respectfully.
    def normalize_dim_size(size, factor=None):
        rounded_size = int(size + (size % DIM_ROUND_DIGIT))
        
        if(factor):    
            new_size = int(rounded_size * factor)
            return new_size

        else:
            return rounded_size
            