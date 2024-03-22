import flet as ft

# Board
BOARD_WIDTH = 10
BOARD_HEIGHT = 20

# Tetromino blocks
BOX_WIDTH = 20
BOX_HEIGHT = 20
INNER_BOX_WIDTH = 9
INNER_BOX_HEIGHT = 9
BOX_MARGIN = 1
BOX_BORDER_RADIUS = 2
MUTE_COLOR = ft.colors.GREY_500
BRIGHT_COLOR = ft.colors.BLACK

# Game init settings
PAGE_PADDING = 5
horizontal_offset = 4

ROW_POSITION =- 1
COL_POSITION = 4

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 800
PAGE_BACKGROUND_COLOR = "#2980B9"
FONTS = {"LCD": "fonts/LCD2N.TTF"}

# BUTTONS STYLE
BTN_COLOR = ft.colors.YELLOW_600


# OPTIONS LABELS
OPTIONS_LABELS = ["ROTATE CLOCKWISE", "RESET HIGH SCORE", "SAVE GAME", "LOAD GAME"]

# FILES
HIGHSCORE_FILE = "highscore.json"
GAME_STATE_FILE = "game_state.json"

CREDITS_TEXT = "Version: 1.0.2alpha, \nAutor: Sergey Vasilev, 2024 \nGitHub: https://github.com/SergeiVasilyev/"