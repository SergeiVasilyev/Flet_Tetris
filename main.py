import asyncio
import flet as ft
from settings import *
from buttons_layout import buttons_layout
from main_screen import MainScreen
from tetris import Game


hiscore = ft.Text(f"Hiscore: 0", size=20)
lines = ft.Text(f"Lines: 0", size=20)
score = ft.Text(f"Score: 0", size=20)
level = ft.Text(f"Level: 0", size=20)
delay = ft.Text(f"Delay: 0", size=20)
speed = ft.Text(f"Speed: 1", size=20)

async def main(page: ft.Page):
    ms = MainScreen()
    main_screen = ms.background()
    main_container = main_screen.controls[0].content
    tetris = Game()
    hiscore.value = f"Hiscore: {tetris.hiscore}"
    
    
    def reset_screen(refresh=False):
        for y in range(20):
            for x in range(10):
                color = BRIGHT_COLOR if refresh and tetris.board[y][x] == 1 else MUTE_COLOR
                main_container.controls[y*10+x].border = ft.border.all(2, color)
                main_container.controls[y*10+x].content.controls[0].bgcolor = color
        

    def board_update(is_show, tetris):
        if tetris.current_tetromino:
            for block in tetris.current_tetromino.shape():
                block.y = 0 if block.y < 0 or block.y >= 20 else block.y
                main_container.controls[block.y * 10 + block.x].border = ft.border.all(2, BRIGHT_COLOR if is_show else MUTE_COLOR)
                main_container.controls[block.y * 10 + block.x].content.controls[0].bgcolor = BRIGHT_COLOR if is_show else MUTE_COLOR

    def update_dashboard():
        global lines, level, score, delay, hiscore
        hiscore.value = f"Hiscore: {tetris.hiscore}"
        lines.value = f"Lines: {tetris.lines}"
        level.value = f"Level: {tetris.level}"
        score.value = f"Score: {tetris.score}"
        delay.value = f"Delay: {tetris.delay}"
        speed.value = f"Speed: {tetris.speed}"


    async def set_dropped(wait=0.5):
        if tetris.collision(row=1): 
            await asyncio.sleep(wait) # last chance to move tetromino
            if tetris.collision(row=1): # check again if tetromino can move
                tetris.dropped()
                tetris.new_tetromino()
            reset_screen(True) # refresh board. On last step, dropped tetromino leaves trace.
            update_dashboard()

    async def game(e):
        if tetris.status != 1:
            tetris.inits()
        while e.control.selected:
            await down(delay=tetris.delay)

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

    async def down(delay):
        if tetris.current_tetromino.row != -1:
            board_update(False, tetris)
        if not tetris.collision(row=1):
            tetris.down()
        board_update(True, tetris)
        await page.update_async()
        await asyncio.sleep(delay)
        await set_dropped()
 

    async def drop(e):
        while tetris.current_tetromino.row > 0:
            await down(delay=0)

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
    start_btn = ft.Chip(label=ft.Text('Start', color="black"), on_select=game, shape=ft.StadiumBorder(), elevation=3, shadow_color="black", )
    restart_btn = ft.ElevatedButton("R", on_click=restart, style=func_btn_style)
    func_buttons = [start_btn, restart_btn]
    rotate_btn = ft.ElevatedButton("Rotate", on_click=rotate, style=rotate_btn_style)
    left_btn = ft.ElevatedButton("Left", on_click=left, on_long_press=left_long, style=direction_btn_style)
    right_btn = ft.ElevatedButton("Right", on_click=right, on_long_press=right_long, style=direction_btn_style)
    up_btn = ft.ElevatedButton("Up", on_click=drop, style=direction_btn_style)
    drop_btn = ft.ElevatedButton("Drop", on_click=drop, style=direction_btn_style)
    directions = [up_btn, left_btn, right_btn, drop_btn, rotate_btn]

    buttons_block = buttons_layout(func_buttons, directions)

    # Info screen
    info_container = ft.Container(
        content=ft.Column([hiscore, lines, score, level, delay, speed]),
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
    # page.bgcolor = ft.colors.BLUE_GREY_300
    page.bgcolor = "#2980B9"
    await page.add_async(tetris_row, buttons_block)

ft.app(target=main)

