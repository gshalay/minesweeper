from window import Window
from PIL import Image, ImageTk
from tkinter import Frame, Button
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
        
        # Menu Frame
        # Num Flags, elapsed time, num mines
        self.info_frame = Frame(self.root, background="red")
        self.info_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.info_frame.rowconfigure(0, weight=1)
        self.info_frame.columnconfigure(0, weight=1)
        self.info_frame.columnconfigure(1, weight=1)
        self.info_frame.columnconfigure(2, weight=1)

        # Flags Placed Panel
        self.info_left_frame = Frame(self.info_frame, background="yellow")
        self.info_left_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        # Timer Frame
        self.info_middle_frame = Frame(self.info_frame, background="blue")
        self.info_middle_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        # Number of Mines Frame
        self.info_right_frame = Frame(self.info_frame, background="green")
        self.info_right_frame.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")

        # Minefield Frame (7/8 of the height)
        self.field_frame = Frame(self.root, background="blue")
        self.field_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        # Configure rows in the root window
        self.root.rowconfigure(0, weight=4)  # 1/8
        self.root.rowconfigure(1, weight=6)  # 7/8

        # Ensure the column expands to fill horizontal space
        self.root.columnconfigure(0, weight=1)
        
        # Update the frame dimensions for use later.
        self.redraw()

        # Create Cells
        self._populate_board()

        # Update the frame dimensions for use later.
        self.redraw()

    def reveal_cell(self):
        print("click event")
        
    def create_button(self, row, col):
        # Load the image file
        image_path = os.path.join(os.path.dirname(__file__), "../assets/blank.png")
        original_image = Image.open(image_path)

        # Calculate button dimensions
        btn_width = self.field_frame.winfo_width() // self.minefield.num_cols
        btn_height = self.field_frame.winfo_height() // self.minefield.num_rows

        # Resize the image to match button dimensions
        resized_image = original_image.resize((btn_width, btn_height), Image.Resampling.LANCZOS)
        tk_image = ImageTk.PhotoImage(resized_image)

        # Create the button with the resized image
        b = Button(self.field_frame, image=None, command=self.reveal_cell)
        b.image = None  # Keep a reference to prevent garbage collection
        b.grid(row=row, column=col, sticky="nsew")  # Expand to fill the grid cell

        return b
    
    def _populate_board(self):
        for row in range(0, self.minefield.num_rows):
            new_row = np.array([])
            self.field_frame.rowconfigure(row, weight=1)
            for col in range(0, self.minefield.num_cols):
                np.append(new_row, self.create_button(row, col))
                self.field_frame.rowconfigure(row, weight=1)
            np.append(self.buttons, new_row)

        # Configure rows and columns to distribute space evenly
        for row in range(self.minefield.num_rows):
            self.field_frame.rowconfigure(row, weight=1)
        for col in range(self.minefield.num_cols):
            self.field_frame.columnconfigure(col, weight=1)
        
        self.redraw()
        
    # A good ratio for the two frames is 1/8 and 7/8 of window height respectfully.
    def normalize_dim_size(self, size, factor=None):
        new_size = size
        if(new_size % DIM_ROUND_DIGIT != 0):
            new_size = int((new_size + (new_size % DIM_ROUND_DIGIT)))
        
        if(factor):    
            new_size = int((new_size * factor) + (new_size * factor) % DIM_ROUND_DIGIT)
        
        return new_size
            