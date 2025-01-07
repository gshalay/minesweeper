from window import Window
from tkinter import Frame, Label, Text, Button, Toplevel

class ParamWindow():
    def __init__(self, parent):
        self.root = Toplevel(parent)
        self.rows = self.cols = self.mines = None
        
        # Params Frame
        self.params_frame = Frame(self.root, background="red")
        self.params_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.params_frame.rowconfigure(0, weight=1)
        self.params_frame.rowconfigure(1, weight=1)
        self.params_frame.columnconfigure(0, weight=1)
        
        self.rows_lbl = Label(self.params_frame, font=("Helvetica", 14), anchor="nw")
        self.rows_lbl.grid(row=0, column=0, padx=2, pady=2, sticky="nsew")
        self.rows_lbl["text"] = "Rows:"
        
        self.rows_txt = Text(self.params_frame, font=("Helvetica", 14), anchor="nw")
        self.rows_txt.grid(row=0, column=1, padx=2, pady=2, sticky="nsew")
        
        self.cols_lbl = Label(self.params_frame, font=("Helvetica", 14), anchor="nw")
        self.cols_lbl.grid(row=1, column=0, padx=2, pady=2, sticky="nsew")
        self.cols_lbl["text"] = "Columns:"
        
        self.cols_txt = Text(self.params_frame, font=("Helvetica", 14), anchor="nw")
        self.cols_txt.grid(row=1, column=1, padx=2, pady=2, sticky="nsew")
        
        self.mines_lbl = Label(self.params_frame, font=("Helvetica", 14), anchor="nw")
        self.mines_lbl.grid(row=2, column=0, padx=2, pady=2, sticky="nsew")
        self.mines_lbl["text"] = "Mines:"
        
        self.mines_txt = Text(self.params_frame, font=("Helvetica", 14), anchor="nw")
        self.mines_txt.grid(row=2, column=1, padx=2, pady=2, sticky="nsew")
        
        self.ok_btn = Button(self.params_frame, font=self.technology_bold_font, anchor="nw", command=submit)
        self.ok_btn.grid(row=3, column=0, padx=2, pady=2, sticky="nsew")
        self.ok_btn["text"] = "OK"
        
        self.cancel_btn = Button(self.params_frame, font=self.technology_bold_font, anchor="nw", command=cancel)
        self.cancel_btn.grid(row=3, column=0, padx=2, pady=2, sticky="nsew")
        self.cancel_btn["text"] = "Cancel"
        
        self.root.protocol("WM_DELETE_WINDOW", self.cancel)
        
        def cancel(self):
            self.top.destroy()
            
        def submit(self):
            self.rows = self.rows_txt.winfo_text()
            self.cols = self.cols_txt.winfo_text()
            self.mines = self.mines_txt.winfo_text()
            self.root.destroy()  # Close the child window
            