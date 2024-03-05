import asyncio
import flet as ft
from settings import *
from buttons_layout import buttons_layout
from main_screen import MainScreen
from tetris import Game


lcd_font = "LCD"
hiscore_label = ft.Text(f"HI-SCORE", size=15)
hiscore = ft.Text(f"0", size=20, font_family=lcd_font, text_align=ft.TextAlign.CENTER)
lines = ft.Text(f"Lines: 0", size=20, font_family=lcd_font)
score_lable = ft.Text(f"SCORE", size=15)
score = ft.Text(f"0", size=20, font_family=lcd_font, text_align=ft.TextAlign.CENTER)
level_lable = ft.Text(f"LEVEL", size=15)
level = ft.Text(f"1", size=20, font_family=lcd_font)
delay = ft.Text(f"Delay: 0", size=20, font_family=lcd_font)
speed_lable = ft.Text(f"SPEED", size=15)
speed = ft.Text(f"1", size=20, font_family=lcd_font)
next_label = ft.Text(f"NEXT", size=15)
game_over_label = ft.Text("", size=15)

async def main(page: ft.Page):
    ms = MainScreen()
    main_screen = ms.background()
    next_viewer = ms.next_tetromino_viewer()
    main_container = main_screen.controls[0].content
    tetris = Game()
    hiscore.value = f"{tetris.hiscore}"
    
    
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
                block.y = 0 if block.y < 0 or block.y >= 20 else block.y
                main_container.controls[block.y * 10 + block.x].border = ft.border.all(2, BRIGHT_COLOR if is_show else MUTE_COLOR)
                main_container.controls[block.y * 10 + block.x].content.controls[0].bgcolor = BRIGHT_COLOR if is_show else MUTE_COLOR

    def next_view(is_show, tetris) -> None:
        """
        Function to update the next tetromino view based on the provided visibility flag and tetris state.

        :param is_show: bool - Flag to indicate whether to show the next tetromino view
        :param tetris: Tetris - The tetris state object
        """
        t = tetris.next_tetromino
        if t:
            for block in t.shape():
                next_viewer.content.controls[block.y * 4 + block.x].border = ft.border.all(2, BRIGHT_COLOR if is_show else MUTE_COLOR)
                next_viewer.content.controls[block.y * 4 + block.x].content.controls[0].bgcolor = BRIGHT_COLOR if is_show else MUTE_COLOR

    def update_dashboard():
        global lines, level, score, delay, hiscore_label, hiscore
        hiscore.value = f"{tetris.hiscore}"
        lines.value = f"Lines: {tetris.lines}"
        level.value = f"{tetris.level}"
        score.value = f"{tetris.score}"
        delay.value = f"Delay: {tetris.delay}"
        speed.value = f"{tetris.speed}"


    async def set_dropped(wait=0.5):
        if tetris.collision(row=1): 
            await asyncio.sleep(wait) # last chance to move tetromino
            if tetris.collision(row=1): # check again if tetromino can move
                next_view(False, tetris)
                tetris.dropped()
                tetris.new_tetromino()
            reset_screen(True)
            update_dashboard()
            next_view(True, tetris)
            
            
    async def game(e):
        game_over_label.value = ""
        if tetris.status != 1:
            if tetris.next_tetromino:
                next_view(False, tetris)
            tetris.inits()
            reset_screen()
            update_dashboard()
            next_view(True, tetris)

        while e.control.selected:
            start_btn.label = ft.Text('Pause', color="black")
            await down_step(delay=tetris.delay)
            if tetris.status == 2:
                reset_screen()
                start_btn.selected = False
                game_over_label.value = "GAME OVER"
                start_btn.label = ft.Text('Start', color="black")
                await page.update_async()
                tetris.status == 0
        else:
            start_btn.label = ft.Text('Start', color="black")
            await page.update_async()
        
            


    def restart(e):
        tetris.inits()
        reset_screen()

    async def rotate(e):
        board_update(False, tetris)
        tetris.rotate()
        board_update(True, tetris)
        await page.update_async()

    async def left(e):
        if tetris.current_tetromino.row >= 0:
            board_update(False, tetris)
        
        tetris.left()
        board_update(True, tetris)
        await page.update_async()

    async def right(e):
        if tetris.current_tetromino.row >= 0:
            board_update(False, tetris)
        
        tetris.right()
        board_update(True, tetris)
        await page.update_async()

    async def down_step(delay):
        if tetris.current_tetromino.row != -1:
            board_update(False, tetris)
        if not tetris.collision(row=1):
            tetris.down()
        board_update(True, tetris)
        await page.update_async()
        await asyncio.sleep(delay)
        await set_dropped()
 
    async def drop(e):
        while not tetris.current_tetromino.row <= 0:
            board_update(False, tetris)
            if not tetris.collision(row=1):
                tetris.down()
            else:
                await set_dropped()
        await page.update_async()

    async def down(e):
        await down_step(delay=0)

    async def down_long(e):
        while not tetris.current_tetromino.row <= 0:
            await down_step(delay=0)

    async def left_long(e):
        while not tetris.collision(col=-1):
            await left(e)

    async def right_long(e):
        while not tetris.collision(col=1):
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

    # Info screen
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

    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = page_padding
    page.window_height = 800
    page.window_width = 500
    page.fonts = {"LCD": "fonts/LCD2N.TTF"}
    page.bgcolor = "#2980B9"
    await page.add_async(tetris_row, buttons_block)

ft.app(target=main)

