from minefield import Minefield
from difficulty import Difficulty
from game_window import GameWindow
from menu_window import MenuWindow
from constants import *
import sys
import time

def get_max_mines(size):
    return int(size * MAX_MINE_PERCENTAGE)

def isfloat(val):
    try:
        float(val)
        return True
    except ValueError:
        return False
        

def get_int_selection(instruction, max_val):
    while True:
        selection = input(instruction + ": ")
        if(selection.isdigit()):
            selection = int(selection)
            if(selection < 0):
                print("Number entered was negative. Making it a positive number.")
                selection *= -1
        elif(isfloat(selection)):
            selection = float(selection)
            if(selection < 0.0):
                print("Number entered was negative. Making it a positive number.")
                selection *= -1.0
            selection = int(selection)
        
        else:
            print("Please enter a number, not text. Reprompting...")
            time.sleep(1)
            continue

        if(selection > max_val):
            print(f"Number entered was larger than the allowed max. Using the max value of {max_val}.")
            selection = max_val
        
        # Don't need to explicitly break the loop since returning will do this for us.
        return selection


def get_custom_minefield():
    num_rows = get_int_selection("Enter the number of rows", MAX_DIM)
    num_cols = get_int_selection("Enter the number of columns", MAX_DIM)
    num_mines = get_int_selection("Enter the number of mines", get_max_mines(num_rows * num_cols))

    return Minefield(Difficulty.CUSTOM, num_rows, num_cols, num_mines)
    
def get_minefield_cli():
    print("-------------------- MINESWEEPER GAME SETUP --------------------")
    print("SELECT DIFFICULTY:")
    print("1. EASY    (9x9) with 10 mines")
    print("2. MEDIUM  (16x16) with 40 mines")
    print("3. HARD    (22x22) with 60 mines")
    print("4. EXTREME (30x16) with 99 mines")
    print("5. CUSTOM  (custom board size and mine count)")
    print("----------------------------------------------------------------")

    while True:
        selection = input("Enter difficulty: ")
        match(selection.strip().lower()):
            case "1" | "1." | "easy":
                return Minefield(Difficulty.EASY)
            case "2" | "2." | "medium":
                return Minefield(Difficulty.MEDIUM)
            case "3" | "3." | "hard":
                return Minefield(Difficulty.HARD)
            case "4" | "4." | "extreme":
                return Minefield(Difficulty.EXTREME)
            case "5" | "5." | "custom":
                return get_custom_minefield()
            case _:
                print("Unknown difficulty, reprompting...")
                time.sleep(1)
                break

def do_game_loop(minefield):
    while not minefield.is_solved():
        print(minefield)
        print("Type your move in the following format (without less or greater than symbols): <f (for flag) or o (for open)> <row> <column>")
        print("Note: Unopened cells = U, Flagged cells = F (can still be opened), Blank or number are opened cells, and and M = a mine.")
        print("Note 2: The first row is 0 and the last row is the number of total rows - 1. The same is true for columns.")
        selection = input("Enter move: ").strip().lower().split()

        if(len(selection) != MOVE_ARG_LEN or 
            (selection[0] not in MOVE_TYPE_VALS) or 
            not selection[1].strip().isdigit() or 
            not selection[2].strip().isdigit() ):
            print("Invalid command. Reprompting...")
            time.sleep(1)
            continue
        
        row = int(selection[1]) * -1 if(int(selection[1]) < 0) else int(selection[1]) 
        col = int(selection[2]) * -1 if(int(selection[2]) < 0) else int(selection[2])

        # Flag move
        if(selection[0] in FLAG_MOVE_TYPE_VALS):
            if(minefield.flag_coord(row, col)):
                print(f"Flagged cell at row {row} and column {col}.")
                
            else:
                print(f"Couldn't flag cell {row}, {col}. It is either already flagged or already open.")
            
            time.sleep(1)

        # Open move
        elif(selection[0] in OPEN_MOVE_TYPE_VALS):
            if(minefield.open_coord(row, col) == MINE_VAL):
                print(minefield)
                # Game Over!
                return False
            elif(minefield.open_coord(row, col) != MINE_VAL):
                continue
            else:
                print(f"Couldn't flag cell {row}, {col}. It is either already flagged or already open.")
                time.sleep(1)
    
    # Minefield solved. Congrats!
    return True

def launch_cli():
    field_solved = do_game_loop(get_minefield_cli())

    if(field_solved):
        print("Minefield solved! Congrats!")
    else:
        print("KABOOM! Mine triggered! GAME OVER!")

def launch_ui():
    menu_window = MenuWindow(MIN_WINDOW_WIDTH * 1.5, MIN_WINDOW_HEIGHT * 1.5)
    menu_window.wait_for_close()
    
if(__name__ == "__main__"):
    if(len(sys.argv) != 2):
        print("Usage: python3 launch.py <mode> (-c for command-line, -u for gui)")
    
    else:    
        if(sys.argv[1] == "-c"):
            print("Launching CLI...")
            launch_cli()
        if(sys.argv[1] == "-u"):
            print("Launching UI...")
            launch_ui()