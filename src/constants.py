import os

## UI Constants
DIM_ROUND_DIGIT = 8
MAX_WINDOW_WIDTH = 1852
MAX_WINDOW_HEIGHT = 972

MIN_WINDOW_WIDTH = 600
MIN_WINDOW_HEIGHT = 600


## UI Image Path constants
PATH_TRUNK = os.path.dirname(__file__)

ZERO_PATH  = os.path.join(PATH_TRUNK, "../assets/0.png")
ONE_PATH   = os.path.join(PATH_TRUNK, "../assets/1.png")
TWO_PATH   = os.path.join(PATH_TRUNK, "../assets/2.png")
THREE_PATH = os.path.join(PATH_TRUNK, "../assets/3.png")
FOUR_PATH  = os.path.join(PATH_TRUNK, "../assets/4.png")
FIVE_PATH  = os.path.join(PATH_TRUNK, "../assets/5.png")
SIX_PATH   = os.path.join(PATH_TRUNK, "../assets/6.png")
SEVEN_PATH = os.path.join(PATH_TRUNK, "../assets/7.png")
EIGHT_PATH = os.path.join(PATH_TRUNK, "../assets/8.png")

# BLANK_PATH = os.path.join(PATH_TRUNK, "../assets/blank.png")
FLAG_PATH  = os.path.join(PATH_TRUNK, "../assets/flag.png")
MINE_PATH  = os.path.join(PATH_TRUNK, "../assets/mine.png")
FONT_PATH  = os.path.join(PATH_TRUNK, "../assets/alarm_clock.ttf")

TECH_PATH  = os.path.join(PATH_TRUNK, "../assets/Technology-Bold.ttf")

## Minefield Constants
FLAGGED_VAL = -1
MINE_VAL = -2
BLANK_VAL = 0
MAX_DIM = 50
MAX_MINE_PERCENTAGE = 0.25 # Up to 25% of the board can be mines.
MOVE_ARG_LEN = 3
MOVE_TYPE_VALS = [ "f", "flag", "o", "open" ]
FLAG_MOVE_TYPE_VALS = [ "f", "flag" ] 
OPEN_MOVE_TYPE_VALS = [ "o", "open" ]
UNOPENED_CHAR = "U"
FLAGGED_CHAR = "F"
MINE_CHAR = "M"
BLANK_CHAR = " "

## Difficulty Dims
# EASY (9 x 9) board with 10 mines.
EASY_COLS = 9
EASY_ROWS = 9
EASY_NUM_MINES = 10

# MEDIUM (16 x 16) board with 40 mines.
MED_COLS = 16
MED_ROWS = 16
MED_NUM_MINES = 40

# HARD (22 x 22) board with 60 mines.
HARD_COLS = 22
HARD_ROWS = 22
HARD_NUM_MINES = 60

# EXPERT (30 x 16) board with 99 mines.
EXP_COLS = 30
EXP_ROWS = 16
EXP_NUM_MINES = 99

# Font constants
FONT_SIZE_SMALL  = 16
FONT_SIZE_MEDIUM = 25
FONT_SIZE_LARGE  = 50