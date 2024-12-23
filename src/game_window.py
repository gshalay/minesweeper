from window import Window
from tkinter import Frame, Button, PhotoImage
from constants import *
import numpy as np
import os
class GameWindow(Window):
    def __init__(self, width, height, minefield):    
        super().__init__(self.normalize_dim_size(width), self.normalize_dim_size(height))
        self.minefield = minefield
        self.buttons = np.array([])
        
        if(self.width < MIN_WINDOW_WIDTH):
            self.width = MIN_WINDOW_WIDTH
        elif(self.width > MAX_WINDOW_WIDTH):
            self.width = MAX_WINDOW_WIDTH
        
        if(self.height < MIN_WINDOW_HEIGHT):
            self.height = MIN_WINDOW_HEIGHT
        elif(self.height > MAX_WINDOW_HEIGHT):
            self.height = MAX_WINDOW_HEIGHT
        
        info_frame_height = self.normalize_dim_size(self.width - 16, 1/8)
        game_frame_height = self.normalize_dim_size(self.height - 16, 7/8)
        
        # Menu Frame
        # Num Flags, elapsed time, num mines
        self.info_frame = Frame(self.root, width=width, height=info_frame_height, background="red")
        self.info_frame.grid(row=0, column=0, padx=8, pady=8)
    
        # Minefield Frame
        self.field_frame = Frame(self.root, width=width, height=game_frame_height, background="blue")
        self.field_frame.grid(row=1, column=0, padx=8, pady=8)
        
        # Create Cells
        self._populate_board()
        
    
    def reveal_cell(self):
        print("click event")
        
    def create_button(self, row, col):
        image_path = os.path.join(os.path.dirname(__file__), "../assets/blank.png")

        # Load the image as a PhotoImage object
        content = PhotoImage(file=image_path)
        b = Button(self.field_frame, width=int(self.field_frame.winfo_width() / self.minefield.num_rows), height=int(self.field_frame.winfo_height() / self.minefield.num_cols), image=content, command=self.reveal_cell)
        b.grid(row=row, column=col)
        
        return b
    
    def _populate_board(self):
        for row in range(0, self.minefield.num_rows):
            new_row = np.array([])
            
            for col in range(0, self.minefield.num_cols):
                np.append(new_row, self.create_button(row, col))
            
            np.append(self.buttons, new_row)
        
    # A good ratio for the two frames is 1/8 and 7/8 of window height respectfully.
    def normalize_dim_size(self, size, factor=None):
        new_size = size
        if(new_size % DIM_ROUND_DIGIT != 0):
            new_size = int((new_size + (new_size % DIM_ROUND_DIGIT)))
        
        if(factor):    
            new_size = int((new_size * factor) + (new_size * factor) % DIM_ROUND_DIGIT)
        
        return new_size
            