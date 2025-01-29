from constants import *
from tkinter import Frame, Label, Entry, Button, Toplevel, font, messagebox
from PIL import ImageFont
import pyglet


class ParamWindow(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.rows = self.cols = self.mines = self.retval = None
        self.geometry(f"{MIN_WINDOW_WIDTH // 2}x{MIN_WINDOW_HEIGHT // 3}")
        pyglet.options['win32_gdi_font'] = True
        pyglet.font.add_file(FONT_PATH)
        self.technology_bold_font = self.initialize_font(TECH_PATH, FONT_SIZE_LARGE)
        self.update_idletasks()

        self.validate_int_input = self.register(self.validate_integer)

        # Params Frame
        self.params_frame = Frame(self)
        self.params_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.params_frame.rowconfigure(0, weight=1)
        self.params_frame.rowconfigure(1, weight=1)
        self.params_frame.rowconfigure(2, weight=1)
        self.params_frame.rowconfigure(3, weight=1)
        self.params_frame.rowconfigure(4, weight=1)
        self.params_frame.columnconfigure(0, weight=1)
        self.params_frame.columnconfigure(1, weight=2)
        self.update_idletasks()
        
        self.err_lbl = Label(self.params_frame, font=("Helvetica", 14), fg="red")
        self.err_lbl.grid(row=0, column=0, columnspan=2, padx=2, pady=2, sticky="nsew")
        
        self.row_lbl = Label(self.params_frame, font=("Helvetica", 14))
        self.row_lbl.grid(row=1, column=0, padx=2, pady=2, sticky="nsew")
        self.row_lbl["text"] = "Rows:"

        self.rows_txt = Entry(self.params_frame, font=("Helvetica", 14), width=10, validate="key", validatecommand=(self.validate_int_input, "%P"))
        self.rows_txt.grid(row=1, column=1, padx=2, pady=2, sticky="nsew")
        self.update_idletasks()
        
        self.cols_lbl = Label(self.params_frame, font=("Helvetica", 14))
        self.cols_lbl.grid(row=2, column=0, padx=2, pady=2, sticky="nsew")
        self.cols_lbl["text"] = "Columns:"
        
        self.cols_txt = Entry(self.params_frame, font=("Helvetica", 14), width=10, validate="key", validatecommand=(self.validate_int_input, "%P"))
        self.cols_txt.grid(row=2, column=1, padx=2, pady=2, sticky="nsew")
        self.update_idletasks()
        
        self.mines_lbl = Label(self.params_frame, font=("Helvetica", 14))
        self.mines_lbl.grid(row=3, column=0, padx=2, pady=2, sticky="nsew")
        self.mines_lbl["text"] = "Mines:"
        
        self.mines_txt = Entry(self.params_frame, font=("Helvetica", 14), width=10, validate="key", validatecommand=(self.validate_int_input, "%P"))
        self.mines_txt.grid(row=3, column=1, padx=2, pady=2, sticky="nsew")
        self.update_idletasks()
        
        self.ok_btn = Button(self.params_frame, font=self.technology_bold_font, command=self.submit)
        self.ok_btn.grid(row=4, column=0, padx=2, pady=2, sticky="nsew")
        self.ok_btn["text"] = "OK"
        
        self.cancel_btn = Button(self.params_frame, font=self.technology_bold_font, command=self.cancel)
        self.cancel_btn.grid(row=4, column=1, padx=2, pady=2, sticky="nsew")
        self.cancel_btn["text"] = "Cancel"
        self.update_idletasks()
        self.params_frame.grid_propagate(True)

        self.protocol("WM_DELETE_WINDOW", self.cancel)
        
    def cancel(self):
        self.retval = 1
        self.destroy()
        
    def submit(self):
        self.rows = int(self.rows_txt.get())
        self.cols = int(self.cols_txt.get())
        self.mines = int(self.mines_txt.get())
        
        state = self.is_valid()
        self.err_lbl["text"] = state[0]
        
        if(state[1]):
            self.retval = 0
            self.destroy()  # Close the child window

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
    
    def validate_integer(self, val_to_process):
        return val_to_process.isdigit() or val_to_process == ""
    
    def is_valid(self):
        label_text = ""
        valid = False
        
        if(self.rows and self.cols and self.mines):
            params_normalized = []
            
            if(self.rows < 0):
                self.rows = self.rows * -1
            elif(self.rows > MAX_DIM):
                params_normalized.append("rows")
                self.rows = MAX_DIM                
            
            if(self.cols < 0):
                self.cols = self.cols * -1
            elif(self.cols > MAX_DIM):
                params_normalized.append("cols")
                self.cols = MAX_DIM
            
            if(params_normalized):
                prefix = "Rows " if(len(params_normalized) == 1) else "Rows and columns "
                    
                messagebox.showinfo("Normalized Board Dimensions", prefix + "exceeded the max of 50. Set to 50.")
            
            mine_threshold = ((self.rows * self.cols) * MAX_MINE_PERCENTAGE) // 1
            if(self.rows >= mine_threshold or self.cols >= mine_threshold or self.mines >= mine_threshold):
                messagebox.showinfo("Mine Amount", "Mine number entered exceeded threshold of " + str(int(mine_threshold)) + ". Mines set to " + str(mine_threshold) + "." )
            
            valid = True
                    
        else:
            if(not self.rows):
                label_text = "Specify number of rows."
            if(not self.cols):
                label_text = "Specify number of columns."
            if(not self.mines):
                label_text = "Specify number of mines."
            
        return (label_text, valid)
            