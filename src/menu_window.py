from tkinter import Frame, Button, messagebox
from cell_state import CellState
from window import Window
from PIL import Image, ImageTk
from PIL import ImageFont
from constants import *
import numpy as np
import time

class MenuWindow(Window):
    def __init__(self, width, height, minefield):    
        super().__init__(self.normalize_dim_size(width), self.normalize_dim_size(height))
        self.minefield = minefield
        self.buttons = np.empty((self.minefield.num_rows, self.minefield.num_cols), dtype=object)
        self.default_btn_bg = None # Set later when creating the board since the color can vary based on system architecture.
        
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
        self.root.rowconfigure(0, weight=2)  # 1/8
        self.root.rowconfigure(1, weight=6)  # 7/8

        # Ensure the column expands to fill horizontal space
        self.root.columnconfigure(0, weight=1)
        
        self.info_frame.grid_propagate(False)
        self.field_frame.grid_propagate(False)

        # Update the frame dimensions for use later.
        self.redraw()

        # Create Cells
        self._populate_board()

        # Update the frame dimensions for use later.
        self.redraw()

    def restyle_image(self, button, new_image, cell):
        if new_image is None:
            # Handle the case when no image is provided
            if cell.state == CellState.OPENED:
                button.config(relief="flat", borderwidth=0, bg="white")
            else:
                button.config(image='', bg="#d9d9d9")  # Clear the image explicitly
            button.image = None  # Ensure reference is consistent
            return

        # Open and resize the image
        image = Image.open(new_image)
        cell_width = self.field_frame.winfo_width() // self.minefield.num_cols
        cell_height = self.field_frame.winfo_height() // self.minefield.num_rows
        resized_image = image.resize((cell_width, cell_height), Image.Resampling.LANCZOS)

        # Convert to PhotoImage
        new_image_obj = ImageTk.PhotoImage(resized_image)

        # Configure the button based on the cell state
        if cell.state == CellState.OPENED:
            if cell.value == MINE_VAL:
                button.config(image=new_image_obj, relief="flat", borderwidth=0, bg="red")
            else:
                button.config(image=new_image_obj, relief="flat", borderwidth=0, bg="white")
        else:
            button.config(image=new_image_obj)

        # Assign the new image object to prevent garbage collection
        button.image = new_image_obj
    
    def get_cell_image(self, cell):
        match(cell.state):
            case CellState.OPENED:
                match(cell.value):
                    case 1:
                        return ONE_PATH
                    case 2:
                        return TWO_PATH
                    case 3:
                        return THREE_PATH
                    case 4:
                        return FOUR_PATH
                    case 5:
                        return FIVE_PATH
                    case 6:
                        return SIX_PATH
                    case 7:
                        return SEVEN_PATH
                    case 8:
                        return EIGHT_PATH
                    case -2:
                        return MINE_PATH
                    case _:
                        return None
            case CellState.FLAGGED:
                return FLAG_PATH
            case CellState.UNOPENED:
                return None
    
    def refresh_board(self):
        for i in range(self.minefield.num_rows):
            for j in range(self.minefield.num_cols):
                self.restyle_image(self.buttons[i, j], self.get_cell_image(self.minefield.board[i, j]), self.minefield.board[i, j])
    
    def reveal_cell(self, row, col, isLeftClick=True):
        current_state = self.minefield.board[row, col].state
        
        match(current_state):
            case CellState.UNOPENED:
                if(isLeftClick):
                    retVal = self.minefield.open_coord(row, col)
                    self.redraw()
                    self.refresh_board()
                    self.redraw()
                    if(retVal == MINE_VAL):
                        time.sleep(0.5)
                        messagebox.showerror("Game Over!", "KABOOM! Game Over!")
                        self.root.destroy()
                    elif(self.minefield.is_solved()):
                        time.sleep(0.5)
                        messagebox.showinfo("Winner!", "Minefield Solved! Congrats!")
                        self.root.destroy()
                else:
                    retVal = self.minefield.flag_coord(row, col)
                    self.redraw()
                    self.refresh_board()
                    self.redraw()
                return
            case CellState.OPENED:
                return
            case CellState.FLAGGED:
                self.minefield.unflag_coord(row, col)
                if(isLeftClick):
                    retVal = self.minefield.open_coord(row, col)
                    self.refresh_board()
                    self.redraw()
                    if(retVal == MINE_VAL):
                        messagebox.showerror("Game Over!", "KABOOM! Game Over!")
                        self.destroy()

                # Change the image back to none.
                elif(not isLeftClick):
                    self.refresh_board()
                    self.redraw()
                return
            case _:
                return
        
    def create_button(self, row, col):
        # Create the button with the resized image
        b = Button(self.field_frame, image=None)
        b.bind("<Button-1>", lambda event: self.reveal_cell(row, col))
        b.bind("<Button-3>", lambda event: self.reveal_cell(row, col, False))
        
        b.image = None  # Keep a reference to prevent garbage collection
        b.grid(row=row, column=col, sticky="nsew")  # Expand to fill the grid cell

        return b
    
    def _populate_board(self):
        for row in range(0, self.minefield.num_rows):
            for col in range(0, self.minefield.num_cols):
                self.buttons[row, col] = self.create_button(row, col)

        self.default_btn_bg = str(self.buttons[0, 0].cget('background'))

        # Configure rows and columns to distribute space evenly
        cell_width = self.field_frame.winfo_width() // self.minefield.num_cols
        cell_height = self.field_frame.winfo_height() // self.minefield.num_rows    
        
        for row in range(self.minefield.num_rows):
            self.field_frame.rowconfigure(row, weight=1, minsize=cell_height)
        for col in range(self.minefield.num_cols):
            self.field_frame.columnconfigure(col, weight=1, minsize=cell_width)
        
        self.redraw()
        
    # A good ratio for the two frames is 1/8 and 7/8 of window height respectfully.
    def normalize_dim_size(self, size, factor=None):
        new_size = size
        if(new_size % DIM_ROUND_DIGIT != 0):
            new_size = int((new_size + (new_size % DIM_ROUND_DIGIT)))
        
        if(factor):    
            new_size = int((new_size * factor) + (new_size * factor) % DIM_ROUND_DIGIT)
        
        return new_size