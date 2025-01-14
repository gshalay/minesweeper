from tkinter import Frame, Label, messagebox, Toplevel
from game_window import GameWindow
from param_window import ParamWindow
from difficulty import Difficulty
from minefield import Minefield
from window import Window
from constants import *
import numpy as np
import pyglet

pyglet.font.add_file(TECH_PATH)

class MenuWindow(Window):
    def __init__(self, width, height, parent=None):  
        if parent:
            parent.destroy()
        
        super().__init__(width, height)
        self.root.title("Minesweeper - Main Menu")
        
        if(self.width < MIN_WINDOW_WIDTH):
            self.width = MIN_WINDOW_WIDTH
        elif(self.width > MAX_WINDOW_WIDTH):
            self.width = MAX_WINDOW_WIDTH
        
        if(self.height < MIN_WINDOW_HEIGHT):
            self.height = MIN_WINDOW_HEIGHT
        elif(self.height > MAX_WINDOW_HEIGHT):
            self.height = MAX_WINDOW_HEIGHT
        
        # Title Frame
        self.title_frame = Frame(self.root, background="red")
        self.title_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.title_frame.rowconfigure(0, weight=1)
        self.title_frame.rowconfigure(1, weight=1)
        self.title_frame.columnconfigure(0, weight=1)
        
        self.title_lbl = Label(self.title_frame, font=self.technology_bold_font, anchor="nw")
        self.title_lbl.grid(row=0, column=0, padx=2, pady=2, sticky="nsew")
        self.title_lbl["text"] = "Minesweeper"
        
        self.hint_lbl = Label(self.title_frame, font=self.technology_bold_font, anchor="nw")
        self.hint_lbl.grid(row=1, column=0, padx=2, pady=2, sticky="nsew")
        self.hint_lbl["text"] = "Select Difficulty..."
        
        # Easy Option Frame
        self.easy_frame = Frame(self.root, background="yellow")
        self.easy_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.easy_frame.rowconfigure(1, weight=1)
        self.easy_frame.columnconfigure(0, weight=1)
        
        self.easy_lbl = Label(self.easy_frame, font=self.technology_bold_font, anchor="nw")
        self.easy_lbl.grid(row=0, column=0, padx=2, pady=2, sticky="nsew")
        self.easy_lbl["text"] = "EASY\t(9 x 9 with 10 mines)"
        self.easy_lbl.bind("<Enter>", lambda event: self.on_enter(self.easy_lbl, "green", "white"))
        self.easy_lbl.bind("<Leave>", lambda event: self.on_leave(self.easy_lbl))
        self.easy_lbl.bind("<Button-1>", lambda event: self.open_game(Difficulty.EASY))
        
        self.easy_frame.grid_columnconfigure(0, weight=1)
        self.easy_frame.grid_rowconfigure(0, weight=1)
        self.easy_frame.grid_propagate(False)
        self.redraw()
        
        # Medium Option Frame
        self.medium_frame = Frame(self.root, background="blue")
        self.medium_frame.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
        self.medium_frame.rowconfigure(0, weight=1)
        self.medium_frame.columnconfigure(0, weight=1)
        
        self.medium_lbl = Label(self.medium_frame, font=self.technology_bold_font, anchor="nw")
        self.medium_lbl.grid(row=0, column=0, padx=2, pady=2, sticky="nsew")
        self.medium_lbl["text"] = "MEDIUM\t(16 x 16 with 40 mines)"
        self.medium_lbl.bind("<Enter>", lambda event: self.on_enter(self.medium_lbl, "#2a52be", "white"))
        self.medium_lbl.bind("<Leave>", lambda event: self.on_leave(self.medium_lbl))
        self.medium_lbl.bind("<Button-1>", lambda event: self.open_game(Difficulty.MEDIUM))

        self.medium_frame.grid_columnconfigure(0, weight=1)
        self.medium_frame.grid_rowconfigure(0, weight=1)
        self.medium_frame.grid_propagate(False)
        self.redraw()
        
        # Hard Option Frame
        self.hard_frame = Frame(self.root, background="green")
        self.hard_frame.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")
        self.hard_frame.rowconfigure(0, weight=1)
        self.hard_frame.columnconfigure(0, weight=1)
        
        self.hard_lbl = Label(self.hard_frame, font=self.technology_bold_font, anchor="nw")
        self.hard_lbl.grid(row=0, column=0, padx=2, pady=2, sticky="nsew")
        self.hard_lbl["text"] = "HARD\t(22 x 22 with 60 mines)"
        self.hard_lbl.bind("<Enter>", lambda event: self.on_enter(self.hard_lbl, "#fca503", "white"))
        self.hard_lbl.bind("<Leave>", lambda event: self.on_leave(self.hard_lbl))
        self.hard_lbl.bind("<Button-1>", lambda event: self.open_game(Difficulty.HARD))
        
        self.hard_frame.grid_columnconfigure(0, weight=1)
        self.hard_frame.grid_rowconfigure(0, weight=1)
        self.hard_frame.grid_propagate(False)
        self.redraw()

        # Expert Option Frame
        self.expert_frame = Frame(self.root, background="purple")
        self.expert_frame.grid(row=4, column=0, padx=5, pady=5, sticky="nsew")
        self.expert_frame.rowconfigure(0, weight=1)
        self.expert_frame.columnconfigure(0, weight=1)
        
        self.expert_lbl = Label(self.expert_frame, font=self.technology_bold_font, anchor="nw")
        self.expert_lbl.grid(row=0, column=0, padx=2, pady=2, sticky="nsew")
        self.expert_lbl["text"] = "EXPERT\t(30 x 16 with 99 mines)"
        self.expert_lbl.bind("<Enter>", lambda event: self.on_enter(self.expert_lbl, "#fc3d03", "white"))
        self.expert_lbl.bind("<Leave>", lambda event: self.on_leave(self.expert_lbl))
        self.expert_lbl.bind("<Button-1>", lambda event: self.open_game(Difficulty.EXTREME))
        
        self.expert_frame.grid_columnconfigure(0, weight=1)
        self.expert_frame.grid_rowconfigure(0, weight=1)
        self.expert_frame.grid_propagate(False)
        self.redraw()
        
        # Custom Option Frame
        self.custom_frame = Frame(self.root, background="red")
        self.custom_frame.grid(row=5, column=0, padx=5, pady=5, sticky="nsew")
        self.custom_frame.rowconfigure(0, weight=1)
        self.custom_frame.columnconfigure(0, weight=1)
        
        self.custom_lbl = Label(self.custom_frame, font=self.technology_bold_font, anchor="nw")
        self.custom_lbl.grid(row=0, column=0, padx=2, pady=2, sticky="nsew")
        self.custom_lbl["text"] = "Custom"
        self.custom_lbl.bind("<Enter>", lambda event: self.on_enter(self.custom_lbl, "purple", "white"))
        self.custom_lbl.bind("<Leave>", lambda event: self.on_leave(self.custom_lbl))
        self.custom_lbl.bind("<Button-1>", lambda event: self.open_game(Difficulty.CUSTOM))
        
        self.custom_frame.grid_columnconfigure(0, weight=1)
        self.custom_frame.grid_rowconfigure(0, weight=1)
        self.custom_frame.grid_propagate(False)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_rowconfigure(4, weight=1)
        self.root.grid_rowconfigure(5, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Update the frame dimensions for use later.
        self.redraw()
        
    def open_game(self, difficulty):
        match(difficulty):
            case Difficulty.EASY:
                self.game = GameWindow(MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT, Minefield(Difficulty.EASY), self.root)
                self.game.protocol("WM_DELETE_WINDOW", self.show)
            case Difficulty.MEDIUM:
                self.game = GameWindow(MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT, Minefield(Difficulty.MEDIUM), self.root)
                self.game.protocol("WM_DELETE_WINDOW", self.show)
                self.root.wait_window(self.game)
            case Difficulty.HARD:
                self.game = GameWindow(MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT, Minefield(Difficulty.HARD), self.root)
                self.game.protocol("WM_DELETE_WINDOW", self.show)
                self.root.wait_window(self.game)
            case Difficulty.EXTREME:
                self.game = GameWindow(MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT, Minefield(Difficulty.EXTREME), self.root)
                self.game.protocol("WM_DELETE_WINDOW", self.show)
            case Difficulty.CUSTOM:
                self.hide()
                param_window = ParamWindow(self.root, MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT)
                self.root.wait_window(param_window)
                self.game = GameWindow(MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT, Minefield(Difficulty.CUSTOM, param_window.rows, param_window.cols, param_window.mines), self.root)
                self.game.protocol("WM_DELETE_WINDOW", self.show)
            case _:
                messagebox.showerror("Unknown difficulty.")
                
    def on_enter(self, control, bg, fg):
        control.old_colors = (control["background"], control["foreground"])
        parent = self.root.nametowidget(control.winfo_parent())
        control["background"] = bg
        control["foreground"] = fg
        parent["relief"] = "raised"
    
    def on_leave(self, control):
        parent = self.root.nametowidget(control.winfo_parent())
        control["background"] = control.old_colors[0]
        control["foreground"] = control.old_colors[1]
        parent["relief"] = "flat"
        
    def hide(self):
        self.root.wm_withdraw()
    
    def show(self):
        self.root.wm_deiconify()