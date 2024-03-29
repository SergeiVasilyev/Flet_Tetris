import asyncio
import flet as ft
from settings import *
from buttons_layout import buttons_layout
from main_screen import MainScreen
from tetris import Game
from options import Options
from datetime import datetime


# Game screen layout 
ms = MainScreen()
main_screen = ms.background()
main_screen_stack = main_screen.controls.copy()
next_viewer = ms.next_tetromino_viewer()
main_container = main_screen.controls[0].content

# Game initialization
tetris = Game()
op = Options()
options = op.options_fn(ms.main_cont_width+150, ms.main_cont_height)
# options_hiscore = options.content.controls[0].controls[2].content.controls[0].value

# Initialization dashboard elements
lcd_font = "LCD"
hiscore_label = ft.Text(f"HI-SCORE", size=15, color="black")
hiscore = ft.Text(f"{tetris.hiscore_rw}", size=20,  color="black", font_family=lcd_font, text_align=ft.TextAlign.CENTER)
score_lable = ft.Text(f"SCORE", size=15, color="black")
score = ft.Text(f"0", size=20, color="black", font_family=lcd_font, text_align=ft.TextAlign.CENTER)
level_lable = ft.Text(f"LEVEL", size=15, color="black")
level = ft.Text(f"1", size=20, color="black", font_family=lcd_font)
speed_lable = ft.Text(f"SPEED", size=15, color="black")
speed = ft.Text(f"1", size=20, color="black", font_family=lcd_font)
next_label = ft.Text(f"NEXT", size=15, color="black")
game_over_label = ft.Text("", size=15, color="black")


async def main(page: ft.Page):
      

    def refresh_screen(refresh=False) -> None:
        """
        Reset the screen with optional refresh.
        :param refresh: boolean, optional, whether to refresh the screen
        """
        for y in range(20):
            for x in range(10):
                # If the block is filled on the board or if the block is part of the current tetromino, show it in bright color
                color = BRIGHT_COLOR if refresh and tetris.board[y][x] == 1 or any(block.y == y and block.x == x for block in tetris.current_tetromino.shape()) else MUTE_COLOR
                main_container.controls[y*10+x].border = ft.border.all(2, color)
                main_container.controls[y*10+x].content.controls[0].bgcolor = color
        main_screen.update()
        

    def tetromino_show_hide(is_show, tetris) -> None:
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
        
    def next_tetromino_show_hide(is_show, tetris) -> None:
        """Function to update the next tetromino view based on the provided visibility flag and tetris state.

        :param is_show: bool - Flag to indicate whether to show the next tetromino view
        :param tetris: Tetris - The tetris state object
        """
        shape_or_board = tetris.next_tetromino.shape() if is_show else tetris.next_tetromino_board
        if shape_or_board:
            for block in shape_or_board:
                next_viewer.content.controls[block.y * 4 + block.x].border = ft.border.all(2, BRIGHT_COLOR if is_show else MUTE_COLOR)
                next_viewer.content.controls[block.y * 4 + block.x].content.controls[0].bgcolor = BRIGHT_COLOR if is_show else MUTE_COLOR

    def clear_next_tetromino_field():
        """Clear the next tetromino field."""
        for i in range(8):
            next_viewer.content.controls[i].border = ft.border.all(2, MUTE_COLOR)
            next_viewer.content.controls[i].content.controls[0].bgcolor = MUTE_COLOR

    def update_dashboard():
        """Update the dashboard with the current game statistics including lines, level, score, delay, and speed."""
        global level, score, hiscore_label, hiscore
        hiscore.value = f"{tetris.hiscore_rw}"
        level.value = f"{tetris.level}"
        score.value = f"{tetris.score}"
        speed.value = f"{tetris.speed}"
        

    async def clear_lines(line, color, l) -> None:
        """Asynchronously clears lines on the main container with a specified color.
        :param line: The line number to clear.
        :param color: The color to use for clearing.
        :param l: Quantity of lines
        """
        for x in range(10):
            main_container.controls[line*10+x].border = ft.border.all(2, color)
            main_container.controls[line*10+x].content.controls[0].bgcolor = color
        main_screen.update()
        await asyncio.sleep(0.06 / l)
            

    async def filled_line_animation(lines) -> None:
        """Asynchronously animates the filled lines on the screen.
        Args:
            lines (List[int]): A list of line numbers to animate.
        """
        if lines:
            color = BRIGHT_COLOR
            for _ in range(2):
                color = MUTE_COLOR if color == BRIGHT_COLOR else BRIGHT_COLOR
                tasks = [clear_lines(line, color, len(lines)) for line in lines]
                await asyncio.gather(*tasks)


    async def set_dropped_and_update(wait=0.05) -> None:
        """
        An asynchronous function that sets the dropped state of the tetromino in the Tetris game. 
        It takes an optional 'wait' parameter with a default value of 0.05. 
        This function performs collision checks to determine if the tetromino can move, and if not, 
        it drops the tetromino, generates a new one, and updates the dashboard. 
        """
        if tetris.collision_check([tetris.bottom_condition, tetris.board_condition], row=1): 
            await asyncio.sleep(wait) # last chance to move tetromino
            if tetris.collision_check([tetris.bottom_condition, tetris.board_condition], row=1): # check again if tetromino can move
                next_tetromino_show_hide(False, tetris) # hide next tetromino on the dashboard
                tetris.dropped() # drop the tetromino
                tetris.new_tetromino() # Generate new tetromino and reset tetromino row to -1
                update_dashboard() # update the dashboard
                next_tetromino_show_hide(True, tetris) # show next tetromino on the dashboard
                await filled_line_animation(tetris.delete_full_lines_list)
                refresh_screen(refresh=True) # refresh the screen
                

    async def game(e):
        """An asynchronous function that controls the game flow, 
        including initialization, updating the dashboard, and handling game over and pause states.
        """
        game_over_label.value = ""
        if tetris.status != 1: # if game is not running
            if tetris.next_tetromino:
                next_tetromino_show_hide(False, tetris)
            tetris.inits()
            refresh_screen()
            update_dashboard()
            next_tetromino_show_hide(True, tetris)
        
        # while game is running and not paused
        while start_btn.selected and not options_btn.selected:
            disable_buttons(disable_direction_buttons=False, disable_function_buttons=False)
            start_btn.label = ft.Text('Pause', color="black")
            start_btn.selected = True
            start_btn.update()
            await down_step(delay=tetris.delay)

            if tetris.status == 2: # if game is over
                disable_buttons(disable_direction_buttons=True, disable_function_buttons=False)
                refresh_screen()
                start_btn.selected = False
                start_btn.label = ft.Text('Start', color="black")
                start_btn.update()
                tetris.status == 0
        else:
            if options_btn.selected:
                disable_buttons(disable_direction_buttons=True, disable_function_buttons=True)
            else:
                disable_buttons(disable_direction_buttons=True, disable_function_buttons=False)
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
        refresh_screen(True)
        next_tetromino_show_hide(True, tetris)
        page.update()


    async def rotate(e):
        """Rotates tetromino and updates screen."""
        tetromino_show_hide(False, tetris)
        tetris.rotate()
        tetromino_show_hide(True, tetris)
        page.update()


    async def left(e):
        """Moves tetromino to the left and updates screen."""
        tetromino_show_hide(False, tetris)
        tetris.left()
        tetromino_show_hide(True, tetris)
        page.update()


    async def right(e):
        """Moves tetromino to the right and updates screen."""
        tetromino_show_hide(False, tetris)
        tetris.right()
        tetromino_show_hide(True, tetris)
        page.update()


    async def down_step(delay):
        """
        Asynchronously moves the current tetromino down, and delays the next action.
        :param delay: The time delay in seconds before the next action.
        """
        await down(None)
        await asyncio.sleep(delay) # Main delay
 
 
    async def drop(e):
        """Drops the current tetromino."""
        tetromino_show_hide(False, tetris)
        while not tetris.current_tetromino.row < 0:
            tetris.down()
            if tetris.collision_check([tetris.bottom_condition, tetris.board_condition], row=1):
                tetromino_show_hide(True, tetris)
                await set_dropped_and_update(wait=0.03)
                break
        main_screen.update()

    async def down(e):
        """Moves the current tetromino down."""
        await set_dropped_and_update()
        if not tetris.collision_check([tetris.bottom_condition, tetris.board_condition], row=1):
            tetromino_show_hide(False, tetris)
        tetris.down()
        tetromino_show_hide(True, tetris)
        main_screen.update()


    async def down_long(e):
        """Moves the current tetromino down if button is held."""
        while not tetris.collision_check([tetris.bottom_condition, tetris.board_condition], row=1):
            await asyncio.sleep(0)
            await down(e)
            

    async def left_long(e):
        """Moves the current tetromino to the left if button is held."""
        while not tetris.collision_check([tetris.left_condition, tetris.board_condition], col=-1):
            await left(e)

    async def right_long(e):
        """Moves the current tetromino to the right if button is held."""
        while not tetris.collision_check([tetris.right_condition, tetris.board_condition],col=1):
            await right(e)

    def disable_buttons(disable_direction_buttons=False, disable_function_buttons=False):
        """A function to block buttons."""
        start_btn.disabled = disable_function_buttons
        start_btn.update()
        restart_btn.disabled = disable_function_buttons
        restart_btn.update()
        rotate_btn.disabled = disable_direction_buttons
        rotate_btn.update()
        left_btn.disabled = disable_direction_buttons
        left_btn.update()
        right_btn.disabled = disable_direction_buttons
        right_btn.update()
        up_btn.disabled = disable_direction_buttons
        up_btn.update()
        down_btn.disabled = disable_direction_buttons
        down_btn.update()


    async def settings(e):
        """A function to handle settings changes and update the main screen accordingly."""
        global main_screen_stack, main_screen
        # print(options_btn.selected)
        options_btn.selected = not options_btn.selected
        options_btn.update()
        if options_btn.selected:
            # Stop game and disable Start and Restart buttons
            start_btn.selected = False
            start_btn.update()
            disable_buttons(disable_direction_buttons=True, disable_function_buttons=True)

            op.reset_highscrore_label.value = f"{OPTIONS_LABELS[1]} {tetris.hiscore_rw}"
            op.load_game_label.value = f"{OPTIONS_LABELS[3]}"
            if tetris.date:
                date_format = '%Y-%m-%d %H:%M:%S.%f'
                date_obj = datetime.strptime(tetris.date, date_format)
                op.save_game_label.value = f"{OPTIONS_LABELS[2]} {date_obj.strftime('%d.%m.%y %H:%M')}"
            
            main_screen_stack = main_screen.controls.copy()
            main_screen.controls[0] = options
            main_screen.controls.pop() 
        else:
            # Enable Start and Restart buttons
            disable_buttons(disable_direction_buttons=True, disable_function_buttons=False)
            main_screen.controls = main_screen_stack.copy()
        
        
        page.update()

        
    def reset_highscrore(e):
        """Resets the highscore"""
        tetris.hiscore_rw = 0
        hiscore.value = 0
        op.reset_highscrore_label.value = f"{OPTIONS_LABELS[1]} {tetris.hiscore_rw}"
        page.update()

    def save_game(e):
        """A function that saves the game"""
        if tetris.save_game():
            op.save_game_label.value = f"{OPTIONS_LABELS[2]} - Game saved"
            page.update()
        else:
            op.save_game_label.value = f"{OPTIONS_LABELS[2]} - Failed to save"
            page.update()

        
    def load_game(e):
        """A function that loads the saved game"""
        if tetris.load_game():
            op.load_game_label.value = f"{OPTIONS_LABELS[3]} - Game loaded"
            refresh_screen(True)
            page.update()
        else:
            op.load_game_label.value = f"{OPTIONS_LABELS[3]} - Game not found"
            page.update()

    def clockwise(e):
        """A function to set the rotation direction"""
        if e.control.value:
            tetris.rotate_direction = 1
        else:
            tetris.rotate_direction = -1


    # Option buttons.
    op.reset_highscrore.on_click = reset_highscrore
    op.save_game.on_click = save_game
    op.load_game.on_click = load_game
    op.clockwise.on_change = clockwise
    

    # Buttons style
    func_btn_style = ft.ButtonStyle(shape=ft.CircleBorder(), padding=ft.padding.all(0), color="black", bgcolor="white", shadow_color="black", elevation=3)
    direction_btn_style = ft.ButtonStyle(shape=ft.CircleBorder(), padding=35, bgcolor=BTN_COLOR, color="black", shadow_color="black", elevation=3)
    rotate_btn_style = ft.ButtonStyle(shape=ft.CircleBorder(), padding=60, bgcolor=BTN_COLOR, color="black", shadow_color="black", elevation=3)

    # Buttons
    options_btn = ft.IconButton(icon=ft.icons.SETTINGS, icon_size=14, icon_color="black", bgcolor="white", on_click=settings, tooltip="Options", selected=False, width=30, height=30, style=func_btn_style)

    start_btn = ft.Chip(label=ft.Text('Start', color="black"), on_select=game, shape=ft.StadiumBorder(), elevation=3, shadow_color="black", bgcolor="white", label_style=ft.TextStyle(color="black"), tooltip="Start / Pause")
    
    restart_btn = ft.IconButton(icon=ft.icons.REPLAY, icon_size=14, icon_color="black", bgcolor="white", on_click=restart, tooltip="Restart game", selected=False, width=30, height=30, style=func_btn_style)
    func_buttons = [start_btn, options_btn, restart_btn]

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

    async def keyboard(e: ft.KeyboardEvent):
        if not rotate_btn.disabled:
            if e.key == "A" or e.key == "Arrow Left":
                await left(e)
            if e.key == "D" or e.key == "Arrow Right":
                await right(e)
            if e.key == "S" or e.key == "Arrow Down":
                await down(e)
            if e.key == "W" or e.key == "Arrow Up":
                await drop(e)
            if e.key == "F" or e.key == "Numpad 0":
                await rotate(e)
        if not start_btn.disabled:
            if e.key == "Escape" or e.key == "Backspace":
                await settings(e)
            if e.key == "R":
                restart(e)
            if e.key == "E" or e.key == "P":
                start_btn.selected = not start_btn.selected
                start_btn.update()
                await game(e)

    page.on_keyboard_event = keyboard

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

