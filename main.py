import asyncio
import flet as ft
from settings import *
from buttons_layout import buttons_layout
from main_screen import MainScreen
from tetris import Game


# Game screen layout 
ms = MainScreen()
main_screen = ms.background()
next_viewer = ms.next_tetromino_viewer()
main_container = main_screen.controls[0].content
tetris = Game()

# Initialization dashboard elements
lcd_font = "LCD"
hiscore_label = ft.Text(f"HI-SCORE", size=15, color="black")
hiscore = ft.Text(f"{tetris.hiscore}", size=20,  color="black", font_family=lcd_font, text_align=ft.TextAlign.CENTER)
score_lable = ft.Text(f"SCORE", size=15, color="black")
score = ft.Text(f"0", size=20, color="black", font_family=lcd_font, text_align=ft.TextAlign.CENTER)
level_lable = ft.Text(f"LEVEL", size=15, color="black")
level = ft.Text(f"1", size=20, color="black", font_family=lcd_font)
speed_lable = ft.Text(f"SPEED", size=15, color="black")
speed = ft.Text(f"1", size=20, color="black", font_family=lcd_font)
next_label = ft.Text(f"NEXT", size=15, color="black")
game_over_label = ft.Text("", size=15, color="black")


async def main(page: ft.Page):    
    def reset_screen(refresh=False) -> None:
        """
        Reset the screen with optional refresh.
        :param refresh: boolean, optional, whether to refresh the screen
        """
        for y in range(20):
            for x in range(10):
                color = BRIGHT_COLOR if refresh and tetris.board[y][x] == 1 else MUTE_COLOR
                main_container.controls[y*10+x].border = ft.border.all(2, color)
                main_container.controls[y*10+x].content.controls[0].bgcolor = color
        

    def board_update(is_show, tetris) -> None:
        """
        Update the board with the current tetromino's shape by changing the border and background color of the corresponding controls. 

        Parameters:
            is_show (bool): A flag indicating whether to show or hide the tetromino.
            tetris (Tetris): The Tetris object containing the current tetromino.
        """
        if tetris.current_tetromino:
            for block in tetris.current_tetromino.shape():
                if block.y >= 0 and block.y <= 20:
                    main_container.controls[block.y * 10 + block.x].border = ft.border.all(2, BRIGHT_COLOR if is_show else MUTE_COLOR)
                    main_container.controls[block.y * 10 + block.x].content.controls[0].bgcolor = BRIGHT_COLOR if is_show else MUTE_COLOR

    def next_view(is_show, tetris) -> None:
        """
        Function to update the next tetromino view based on the provided visibility flag and tetris state.

        :param is_show: bool - Flag to indicate whether to show the next tetromino view
        :param tetris: Tetris - The tetris state object
        """
        next_tetromino = tetris.next_tetromino
        if next_tetromino:
            for block in next_tetromino.shape():
                next_viewer.content.controls[block.y * 4 + block.x].border = ft.border.all(2, BRIGHT_COLOR if is_show else MUTE_COLOR)
                next_viewer.content.controls[block.y * 4 + block.x].content.controls[0].bgcolor = BRIGHT_COLOR if is_show else MUTE_COLOR

    def clear_next_tetromino_field():
        """Clear the next tetromino field."""
        for i in range(8):
            next_viewer.content.controls[i].border = ft.border.all(2, MUTE_COLOR)
            next_viewer.content.controls[i].content.controls[0].bgcolor = MUTE_COLOR

    def update_dashboard():
        """Update the dashboard with the current game statistics including lines, level, score, delay, and speed."""
        global lines, level, score, delay, hiscore_label, hiscore
        hiscore.value = f"{tetris.hiscore}"
        level.value = f"{tetris.level}"
        score.value = f"{tetris.score}"
        speed.value = f"{tetris.speed}"


    async def set_dropped_and_update(wait=0.5):
        """
        An asynchronous function that sets the dropped state of the tetromino in the Tetris game. 
        It takes an optional 'wait' parameter with a default value of 0.5. 
        This function performs collision checks to determine if the tetromino can move, and if not, 
        it drops the tetromino, generates a new one, and updates the dashboard. 
        """
        if tetris.collision_check([tetris.bottom_condition, tetris.board_condition], row=1): 
            await asyncio.sleep(wait) # last chance to move tetromino
            if tetris.collision_check([tetris.bottom_condition, tetris.board_condition], row=1): # check again if tetromino can move
                next_view(False, tetris) # hide next tetromino on the dashboard
                tetris.dropped() # drop the tetromino
                tetris.new_tetromino() # Generate new tetromino and reset tetromino row to -1
            reset_screen(True) # refresh the screen
            update_dashboard() # update the dashboard
            next_view(True, tetris) # show next tetromino on the dashboard
            
            
    async def game(e):
        """An asynchronous function that controls the game flow, 
        including initialization, updating the dashboard, and handling game over and pause states.
        """
        game_over_label.value = ""
        if tetris.status != 1: # if game is not running
            if tetris.next_tetromino:
                next_view(False, tetris)
            tetris.inits()
            reset_screen()
            update_dashboard()
            next_view(True, tetris)
        
        # while game is running and not paused
        while e.control.selected:
            start_btn.label = ft.Text('Pause', color="black")
            await down_step(delay=tetris.delay)
            if tetris.status == 2: # if game is over
                reset_screen()
                start_btn.selected = False
                start_btn.label = ft.Text('Start', color="black")
                page.update()
                tetris.status == 0
        else:
            start_btn.label = ft.Text('Start', color="black")
            game_over_label.value = "PAUSE" if tetris.status == 1 else "GAME OVER"
            page.update()
        

    def restart(e):
        """
        Restarts the game by clearing the next tetromino field, initializing the tetris game, resetting the screen, and updating the next tetromino view.
        Parameters:
            e: the event that triggers the restart function
        """
        clear_next_tetromino_field()
        tetris.inits()
        reset_screen()
        next_view(True, tetris)

    async def rotate(e):
        """Rotates tetromino and updates screen."""
        board_update(False, tetris)
        tetris.rotate()
        board_update(True, tetris)
        page.update()

    async def left(e):
        """Moves tetromino to the left and updates screen."""
        if tetris.current_tetromino.row >= 0:
            board_update(False, tetris)
        
        tetris.left()
        board_update(True, tetris)
        page.update()

    async def right(e):
        """Moves tetromino to the right and updates screen."""
        if tetris.current_tetromino.row >= 0:
            board_update(False, tetris)
        
        tetris.right()
        board_update(True, tetris)
        page.update()

    async def down_step(delay):
        """
        Asynchronously moves the current tetromino down, and delays the next action.
        :param delay: The time delay in seconds before the next action.
        """
        if tetris.current_tetromino.row != -1:
            board_update(False, tetris)
        tetris.down()
        board_update(True, tetris)
        page.update()
        await asyncio.sleep(delay) # Main delay
        await set_dropped_and_update()
 
 
    async def drop(e):
        """Drops the current tetromino."""
        board_update(False, tetris)
        while not tetris.current_tetromino.row < 0:
            tetris.down()
            if tetris.collision_check([tetris.bottom_condition, tetris.board_condition], row=1):
                board_update(True, tetris)
                await set_dropped_and_update()
                break
        page.update()

    async def down(e):
        """Moves the current tetromino down."""
        await down_step(delay=0)

    async def down_long(e):
        """Moves the current tetromino down if button is held."""
        while not tetris.current_tetromino.row <= 0:
            await down_step(delay=0)

    async def left_long(e):
        """Moves the current tetromino to the left if button is held."""
        while not tetris.collision_check([tetris.left_condition], col=-1):
            await left(e)

    async def right_long(e):
        """Moves the current tetromino to the right if button is held."""
        while not tetris.collision_check([tetris.right_condition],col=1):
            await right(e)



    # Buttons style
    func_btn_style = ft.ButtonStyle(shape=ft.CircleBorder(), padding=ft.padding.all(10), color="black", bgcolor="white", shadow_color="black", elevation=3)
    direction_btn_style = ft.ButtonStyle(shape=ft.CircleBorder(), padding=35, bgcolor=BTN_COLOR, color="black", shadow_color="black", elevation=3)
    rotate_btn_style = ft.ButtonStyle(shape=ft.CircleBorder(), padding=60, bgcolor=BTN_COLOR, color="black", shadow_color="black", elevation=3)

    # Buttons
    start_btn = ft.Chip(label=ft.Text('Start', color="black"), on_select=game, shape=ft.StadiumBorder(), elevation=3, shadow_color="black", bgcolor="white", label_style=ft.TextStyle(color="black"))
    restart_btn = ft.ElevatedButton("R", on_click=restart, style=func_btn_style)
    func_buttons = [start_btn, restart_btn]
    rotate_btn = ft.ElevatedButton("Rotate", on_click=rotate, style=rotate_btn_style)
    left_btn = ft.ElevatedButton("Left", on_click=left, on_long_press=left_long, style=direction_btn_style)
    right_btn = ft.ElevatedButton("Right", on_click=right, on_long_press=right_long, style=direction_btn_style)
    up_btn = ft.ElevatedButton("Drop", on_click=drop, style=direction_btn_style)
    down_btn = ft.ElevatedButton("Down", on_click=down, on_long_press=down_long, style=direction_btn_style)
    directions = [up_btn, left_btn, right_btn, down_btn, rotate_btn]

    buttons_block = buttons_layout(func_buttons, directions)

    # Dashboard
    info_container = ft.Container(
        content=ft.Column([
            ft.Column([hiscore_label, hiscore,], horizontal_alignment=ft.CrossAxisAlignment.END, spacing=5),
            ft.Column([score_lable, score,], horizontal_alignment=ft.CrossAxisAlignment.END, spacing=5),
            ft.Column([level_lable, level,], horizontal_alignment=ft.CrossAxisAlignment.END, spacing=5),
            ft.Column([speed_lable, speed,], horizontal_alignment=ft.CrossAxisAlignment.END, spacing=5),
            ft.Column([next_label, next_viewer,], horizontal_alignment=ft.CrossAxisAlignment.END, spacing=5),
            ft.Column([game_over_label,], horizontal_alignment=ft.CrossAxisAlignment.END, spacing=5),
        ],
            horizontal_alignment=ft.CrossAxisAlignment.END,
            spacing=18
        ),
        alignment=ft.alignment.center
    )
    main_screen.controls[1].content = info_container

    # Borders around main screen
    main_screen_container = ft.Container(
        content=main_screen,
        border=ft.border.only(
            bottom=ft.border.BorderSide(4, ft.colors.BLACK12), 
            right=ft.border.BorderSide(4, ft.colors.BLACK12), 
            left=ft.border.BorderSide(4, ft.colors.BLACK38), 
            top=ft.border.BorderSide(4, ft.colors.BLACK38)),
        border_radius=20,
    )

    # Main screen
    tetris_row = ft.Row(
        [main_screen_container],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    # Page view settings
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = PAGE_PADDING
    page.window_height = WINDOW_HEIGHT
    page.window_width = WINDOW_WIDTH
    page.fonts = FONTS
    page.bgcolor = PAGE_BACKGROUND_COLOR
    page.add(tetris_row, buttons_block)

ft.app(target=main)

