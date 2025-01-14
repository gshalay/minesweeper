from tkinter import Tk, font
from PIL import ImageFont
from constants import *
import pyglet

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
        self.root.geometry(str(int(width) + 10) + "x" + str(int(height) + 10))
        self.root.protocol("WM_DELETE_WINDOW", self.close)

        pyglet.options['win32_gdi_font'] = True
        pyglet.font.add_file(FONT_PATH)

        self.technology_bold_font = self.initialize_font(TECH_PATH, FONT_SIZE_LARGE)
    
    def redraw(self):
        self.root.update_idletasks()
        self.root.update()

    def wait_for_close(self):
        self.is_running = True

        while self.is_running:
            self.redraw()
    
    def close(self):
        self.is_running = False

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

    def print_font_details(self, font_path, font_size):
        try:
            # Load the font
            font = ImageFont.truetype(font_path, font_size)
            
            # Print details of the font
            print(f"Font Path: {font_path}")
            print(f"Font Size: {font_size}")
            print(f"Font Name: {font.getname()[0]}")  # Family name
            print(f"Font Style: {font.getname()[1]}")  # Style (if any)
            print(f"Font Type: {font.getformat()}")  # Format (e.g., TTF)
            print(f"Font Glyphs: {font.getnumfaces()}")  # Number of glyphs

        except Exception as e:
            print(f"Error loading font: {e}")
    
    def print_loaded_font_details(self, font):
        try:
            print(f"typeof: {type(font)}")
            print(f"Font Name: {font.getname()[0]}")  # Family name
            print(f"Font Style: {font.getname()[1]}")  # Style (if any)
            print(f"Font Type: {font.getformat()}")  # Format (e.g., TTF)
            print(f"Font Glyphs: {font.getnumfaces()}")  # Number of glyphs

        except Exception as e:
            print(f"Error loading loaded font: {e}")