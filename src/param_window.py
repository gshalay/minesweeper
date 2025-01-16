from constants import *
from tkinter import Frame, Label, Text, Button, Toplevel, font
from PIL import ImageFont
import pyglet


class ParamWindow(Toplevel):
    def __init__(self, parent, width, height):
        super().__init__(parent)
        self.rows = self.cols = self.mines = None
        self.geometry(f"{MIN_WINDOW_WIDTH // 2}x{MIN_WINDOW_HEIGHT // 3}")
        pyglet.options['win32_gdi_font'] = True
        pyglet.font.add_file(FONT_PATH)
        self.technology_bold_font = self.initialize_font(TECH_PATH, FONT_SIZE_LARGE)
        self.update_idletasks()

        

        # Params Frame
        self.params_frame = Frame(self, background="red")
        self.params_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.params_frame.rowconfigure(0, weight=1)
        self.params_frame.rowconfigure(1, weight=1)
        self.params_frame.rowconfigure(2, weight=1)
        self.params_frame.rowconfigure(3, weight=1)
        self.params_frame.columnconfigure(0, weight=1)
        self.params_frame.columnconfigure(1, weight=2)
        self.update_idletasks()
        
        self.rows_lbl = Label(self.params_frame, font=("Helvetica", 14))
        self.rows_lbl.grid(row=0, column=0, padx=2, pady=2, sticky="nsew")
        self.rows_lbl["text"] = "Rows:"
        
        self.rows_txt = Text(self.params_frame, font=("Helvetica", 14), height=1, width=10)
        self.rows_txt.grid(row=0, column=1, padx=2, pady=2, sticky="nsew")
        self.update_idletasks()
        
        self.cols_lbl = Label(self.params_frame, font=("Helvetica", 14))
        self.cols_lbl.grid(row=1, column=0, padx=2, pady=2, sticky="nsew")
        self.cols_lbl["text"] = "Columns:"
        
        self.cols_txt = Text(self.params_frame, font=("Helvetica", 14), height=1, width=10)
        self.cols_txt.grid(row=1, column=1, padx=2, pady=2, sticky="nsew")
        self.update_idletasks()
        
        self.mines_lbl = Label(self.params_frame, font=("Helvetica", 14))
        self.mines_lbl.grid(row=2, column=0, padx=2, pady=2, sticky="nsew")
        self.mines_lbl["text"] = "Mines:"
        
        self.mines_txt = Text(self.params_frame, font=("Helvetica", 14), height=1, width=10)
        self.mines_txt.grid(row=2, column=1, padx=2, pady=2, sticky="nsew")
        self.update_idletasks()
        
        self.ok_btn = Button(self.params_frame, font=self.technology_bold_font, command=self.submit)
        self.ok_btn.grid(row=3, column=0, padx=2, pady=2, sticky="nsew")
        self.ok_btn["text"] = "OK"
        
        self.cancel_btn = Button(self.params_frame, font=self.technology_bold_font, command=self.cancel)
        self.cancel_btn.grid(row=3, column=1, padx=2, pady=2, sticky="nsew")
        self.cancel_btn["text"] = "Cancel"
        self.update_idletasks()
        self.params_frame.grid_propagate(True)

        self.protocol("WM_DELETE_WINDOW", self.cancel)
        
    def cancel(self):
        self.destroy()
        
    def submit(self):
        self.rows = int(self.rows_txt.get(1.0, "end-1c"))
        self.cols = int(self.cols_txt.get(1.0, "end-1c"))
        self.mines = int(self.mines_txt.get(1.0, "end-1c"))
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
            