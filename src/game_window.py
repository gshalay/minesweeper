from tkinter import Frame, Button, messagebox, Label, StringVar, Toplevel, font, BOTH
from constants import *
from cell_state import CellState
from PIL import Image, ImageTk, ImageFont
from timer import Timer

import sys
import numpy as np
import time
import pyglet

pyglet.font.add_file(TECH_PATH)
sys.setrecursionlimit(2000)

class GameWindow(Toplevel):
    def __init__(self, width, height, minefield, parent):
        super().__init__(parent)
        
        self.hide()
        self.width = width
        self.height = height
        self.geometry(f"{width + 10}x{height + 10}")
        self.minefield = minefield
        self.title("Minesweeper")
        self.buttons = np.empty((self.minefield.num_rows, self.minefield.num_cols), dtype=object)
        self.default_btn_bg = None
        self.is_resizing = False
        
        pyglet.options['win32_gdi_font'] = True
        pyglet.font.add_file(FONT_PATH)
        self.technology_bold_font = self.initialize_font(TECH_PATH, FONT_SIZE_LARGE)
        self.protocol("WM_DELETE_WINDOW", self.close)

        if(self.width < MIN_WINDOW_WIDTH):
            self.width = MIN_WINDOW_WIDTH
        elif(self.width > MAX_WINDOW_WIDTH):
            self.width = MAX_WINDOW_WIDTH
        
        if(self.height < MIN_WINDOW_HEIGHT):
            self.height = MIN_WINDOW_HEIGHT
        elif(self.height > MAX_WINDOW_HEIGHT):
            self.height = MAX_WINDOW_HEIGHT
        
        # Track the last size of the flag image to prevent resize loops
        self.last_flag_img_size = None
        self.last_mine_img_size = None
        self.is_resizing = False  # Flag to prevent resizing feedback loop

        # Configure rows in the _root window
        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=14)

        # Menu Frame
        # Num Flags, elapsed time, num mines
        self.info_frame = Frame(self)
        self.info_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.info_frame.grid_propagate(False)
        self.update_idletasks()

        # Flags Placed Panel
        self.info_left_frame = Frame(self.info_frame)
        self.info_left_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.info_left_frame.grid_columnconfigure(0, weight=90)
        self.info_left_frame.grid_columnconfigure(1, weight=1)
        self.info_left_frame.grid_rowconfigure(0, weight=1)
        self.info_left_frame.grid_propagate(False)

        self.flag_img = Label(self.info_left_frame)
        self.flag_img.grid(row=0, column=0, padx=2, pady=2, sticky="nsew")

        self.update_idletasks()

        self.flag_lbl_var = StringVar(value=str(self.minefield.flags_placed).zfill(4))

        self.flag_lbl = Label(self.info_left_frame, textvariable=self.flag_lbl_var, font=self.technology_bold_font, fg="red", anchor="nw")
        self.flag_lbl.grid(row=0, column=1, padx=2, pady=2, sticky="nsew")

        # Timer Frame
        self.info_middle_frame = Frame(self.info_frame)
        self.info_middle_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        self.update_idletasks()
        
        self.timer_lbl = Label(self.info_middle_frame, font=self.technology_bold_font, anchor="nw", fg="red")
        self.timer_lbl.grid(row=0, column=0, padx=2, pady=2, sticky="nsew")
        self.info_middle_frame.grid_columnconfigure(0, weight=1)
        self.info_middle_frame.grid_rowconfigure(0, weight=1)
        self.info_middle_frame.grid_propagate(False)
        
        # Number of Mines Panel
        self.info_right_frame = Frame(self.info_frame)
        self.info_right_frame.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")
        self.info_right_frame.grid_columnconfigure(0, weight=90)
        self.info_right_frame.grid_columnconfigure(1, weight=1)
        self.info_right_frame.grid_rowconfigure(0, weight=1)
        self.info_right_frame.grid_propagate(False)

        self.mine_img = Label(self.info_right_frame)
        self.mine_img.grid(row=0, column=0, padx=2, pady=2, sticky="nsew")

        self.update_idletasks()

        self.mine_lbl_var = StringVar(value=str(self.minefield.num_mines).zfill(4))

        self.mine_lbl = Label(self.info_right_frame, textvariable=self.mine_lbl_var, font=self.technology_bold_font, fg="red", anchor="nw")
        self.mine_lbl.grid(row=0, column=1, padx=2, pady=2, sticky="nsew")

        self.info_frame.rowconfigure(0, weight=1)
        self.info_frame.columnconfigure(0, weight=4)
        self.info_frame.columnconfigure(1, weight=5)
        self.info_frame.columnconfigure(2, weight=4)

        # Minefield Frame (7/8 of the height)
        self.field_frame = Frame(self)
        self.field_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        # Ensure the column expands to fill horizontal space
        self.columnconfigure(0, weight=1)
        
        self.info_frame.grid_propagate(False)
        self.info_left_frame.grid_propagate(False)
        self.info_middle_frame.grid_propagate(False)
        self.info_right_frame.grid_propagate(False)
        self.field_frame.grid_propagate(False)

        # Update the frame dimensions for use later.
        self.update_idletasks()

        # Create Cells
        self._populate_board()

        # Update the frame dimensions for use later.
        self.update_idletasks()
        self.update_flag_image()
        self.update_mine_image()
        
        self.timer = Timer(self.timer_lbl, self)

        self.show()

        self.timer.start()

    def close(self):
        self.remove_button_bindings()
        self.destroy()
    
    def update_flag_image(self):
        # Manually check the size of the left frame
        lbl_width, lbl_height = self.flag_img.winfo_width(), self.flag_img.winfo_height()

        # Only update if the size has changed
        new_size = (lbl_width, lbl_height)
        if new_size != self.last_flag_img_size:
            self.last_flag_img_size = new_size
            resized_flag = self.update_image(FLAG_PATH, lbl_width, lbl_height)
            self.flag_img.configure(image=resized_flag)
            self.flag_img.image = resized_flag  # Retain reference to prevent GC

        # Schedule the next update (e.g., after 100 milliseconds)
        self.after(100, self.update_flag_image)

    def update_mine_image(self):
        # Manually check the size of the left frame
        lbl_width, lbl_height = self.mine_img.winfo_width(), self.mine_img.winfo_height()

        # Only update if the size has changed
        new_size = (lbl_width, lbl_height)
        if new_size != self.last_flag_img_size:
            self.last_mine_img_size = new_size
            resized_mine = self.update_image(MINE_PATH, lbl_width, lbl_height)
            self.mine_img.configure(image=resized_mine)
            self.mine_img.image = resized_mine  # Retain reference to prevent GC

        # Schedule the next update (e.g., after 100 milliseconds)
        self.after(100, self.update_mine_image)

    def update_image(self, path, h, w):
        label_width, label_height = h, w

        try:
            # Open and resize the image
            img_content = Image.open(path)
            resized_img = img_content.resize((label_width, label_height), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(resized_img)

            return photo

        except Exception as e:
            print(f"Error resizing flag image: {e}")

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
        # Update the flags label.
        self.flag_lbl_var.set(str(self.minefield.flags_placed).zfill(4))

        for i in range(self.minefield.num_rows):
            for j in range(self.minefield.num_cols):
                self.restyle_image(self.buttons[i, j], self.get_cell_image(self.minefield.board[i, j]), self.minefield.board[i, j])
    
    def reveal_cell(self, row, col, isLeftClick=True):
        current_state = self.minefield.board[row, col].state
        
        match(current_state):
            case CellState.UNOPENED:
                if(isLeftClick):
                    retVal = self.minefield.open_coord(row, col)
                    self.update_idletasks()
                    self.refresh_board()
                    self.update_idletasks()
                    if(retVal == MINE_VAL):
                        time.sleep(0.5)
                        self.timer.stop()
                        messagebox.showerror("Game Over!", "KABOOM! Game Over!")
                        self.close()
                    elif(self.minefield.is_solved()):
                        time.sleep(0.5)
                        self.timer.stop()
                        messagebox.showinfo("Winner!", "Minefield Solved! Congrats!")
                        self.close()
                else:
                    retVal = self.minefield.flag_coord(row, col)
                    self.update_idletasks()
                    self.refresh_board()
                    self.update_idletasks()
                return
            case CellState.OPENED:
                return
            case CellState.FLAGGED:
                self.minefield.unflag_coord(row, col)
                if(isLeftClick):
                    retVal = self.minefield.open_coord(row, col)
                    self.refresh_board()
                    self.update_idletasks()
                    if(retVal == MINE_VAL):
                        messagebox.showerror("Game Over!", "KABOOM! Game Over!")
                        self.close()

                # Change the image back to none.
                elif(not isLeftClick):
                    self.refresh_board()
                    self.update_idletasks()
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
    
    def remove_button_bindings(self):
        for i in range(0, self.minefield.num_rows):        
            for j in range(0, self.minefield.num_cols):
                self.buttons[i][j].unbind("<Button-1>")
                self.buttons[i][j].unbind("<Button-3>")
            
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
        
        self.update_idletasks()
        
    # A good ratio for the two frames is 1/8 and 7/8 of window height respectfully.
    def normalize_dim_size(self, size, factor=None):
        new_size = size
        if(new_size % DIM_ROUND_DIGIT != 0):
            new_size = int((new_size + (new_size % DIM_ROUND_DIGIT)))
        
        if(factor):    
            new_size = int((new_size * factor) + (new_size * factor) % DIM_ROUND_DIGIT)
        
        return new_size

    def initialize_font(self, path, font_size):
        try:
            # Load the .ttf font using PIL ImageFont
            pil_font = ImageFont.truetype(path, font_size)

            # Register the font with Tkinter
            custom_font = font.Font(family=pil_font.getname()[0], size=font_size)

            return custom_font
        except Exception as e:
            print(f"Error loading font: {e}")
            return None
    
    def hide(self):
        self.withdraw()
    
    def show(self):
        self.deiconify()