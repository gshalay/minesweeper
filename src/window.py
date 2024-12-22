from tkinter import Tk, Frame

class Window:
    def __init__(self, width, height):
        self.root = Tk()
        self.width = width
        self.height = height
        self.is_running = False
        self.title = "Minesweeper"
        
        # Game Window
        self.root.title(self.title)
        self.root.config(bg="#dadada")
        self.root.geometry(str(width + 10) + "x" + str(height + 10))
        self.root.protocol("WM_DELETE_WINDOW", self.close)
    
    def redraw(self):
        self.root.update_idletasks()
        self.root.update()

    def wait_for_close(self):
        self.is_running = True

        while self.is_running:
            self.redraw()
    
    def close(self):
        self.is_running = False