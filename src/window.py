from tkinter import Tk, BOTH, Canvas

class Window:
    def __init__(self, width, height):
        self.title = "Maze Solver"
        self.root = Tk()
        self.width = width
        self.height = height
        
        # Info Canvas
        self.info_canvas = Canvas(width=width, height=300, relief="raised", background="black")
        
        # Field Canvas
        # self.canvas = Canvas(width=width+50, height=height+50)
        
        self.is_running = False
        self.root.geometry(str(width) + "x" + str(height))

        self.info_canvas.pack()
        # self.canvas.pack()
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