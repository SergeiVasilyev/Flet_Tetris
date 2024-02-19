import asyncio
from functools import reduce
import flet as ft
from tetrominoes import TETROMINOES
from settings import *
from utils import Tetris
from initialization import Initialization


init = Initialization()

main_container = init.background()
board = init.init()
tetramino = TETROMINOES[init.generate_element()]


tetris = Tetris(main_container, board, tetramino, row_position=ROW_POSITION, col_position=COL_POSITION)



async def main(page: ft.Page):

    def draw_element(drawing):
        tetris.draw(drawing)
        # print(tetris.tetromino_blocks_positions)
        for el in tetris.tetromino_blocks_positions:
            main_container.content.controls[el[0]].border = ft.border.all(2, bright_color if drawing else mute_color)
            main_container.content.controls[el[0]].content.controls[0].bgcolor = bright_color if drawing else mute_color

    async def refresh_bord():
        for i in range(20):
            for j in range(10):
                main_container.content.controls[i*10+j].border = ft.border.all(2, bright_color if tetris.board[i][j] == -1 else mute_color)
                main_container.content.controls[i*10+j].content.controls[0].bgcolor = bright_color if tetris.board[i][j] == -1 else mute_color
        await page.update_async()

    
    async def is_line_complete():
        def remove_line(row):
            while row != 0:
                board[row] = board[row - 1][:]
                row -= 1

        for i in range(board_height):
            if -1 in board[i]:
                if abs(sum(board[i])) == board_width:
                    remove_line(i)
                    await refresh_bord()
        return True

    async def animate(e):
        if tetris.row_position != -1:
            draw_element(False)
        tetris.row_position += 1
        draw_element(True)
        if tetris.is_full():
            tetris.board = init.init(True)
            tetris.main_container = init.background()
            tetris.tetramino = TETROMINOES[init.generate_element()]
            tetris.reset_position()
        if tetris.vertical_collision():
            tetris.mark_as_dropped()
            await is_line_complete()
            tetris.reset_position()
            tetris.refresh_tetromino()
        await page.update_async()

    async def game(e):
        print(button.on_click)
        while True:
            await animate(None)
            await asyncio.sleep(1)
            
            
    async def drop(e):
        while tetris.row_position != -1:
            await animate(None)


    async def restart(e):
        tetris.board = init.init(True)
        tetris.refresh_tetromino()
        tetris.reset_position()
        await page.update_async()
    
    async def rotate(e):
        if tetris.row_position >= 0:
            draw_element(False)
            rotated_element = [(-y, x) for x, y in tetris.tetramino]
            tetris.tetramino = tetris.path_correction(rotated_element)
            draw_element(True)
            await page.update_async()

    async def left(e):
        if tetris.row_position >= 0:
            draw_element(False)
            if not tetris.horizontal_collision(-1):
                tetris.col_position -= 1
            draw_element(True)
            await page.update_async()

    async def right(e):
        if tetris.row_position >= 0:
            draw_element(False)
            if not tetris.horizontal_collision(1):
                tetris.col_position += 1
            draw_element(True)
            await page.update_async()
    
    async def left_long(e):
        while not tetris.horizontal_collision(-1):
            await left(e)

    async def right_long(e):
        while not tetris.horizontal_collision(1):
            await right(e)

    async def down(e):
        print(e.control.bgcolor, e.data)
        print('down')
        e.control.bgcolor = "blue" if e.data == "true" else "yellow"
        await e.control.update_async()
        # e.control.update()
        # while tetris.row_position != -1:
        #     await animate(e)

    async def on_click(e: ft.LongPressEndEvent):
        print(e.control, e.data)
        print('down')
        e.control.bgcolor = "blue" if e.data == "true" else "yellow"
        await e.control.update_async()
        

    button = ft.ElevatedButton("START", on_click=game, data=True)
    drop_btn = ft.ElevatedButton("Drop", on_click=drop)
    restart_btn = ft.ElevatedButton("Restart", on_click=restart)
    rotate_btn = ft.ElevatedButton("Rotate", on_click=rotate)
    left_btn = ft.ElevatedButton("Left", on_click=left, on_long_press=left_long)
    right_btn = ft.ElevatedButton("Right", on_click=right, on_long_press=right_long)
    down_btn = ft.ElevatedButton("Down", bgcolor="yellow", on_long_press=on_click)

    buttons = ft.Row([
        button,
        restart_btn,
    ],
    alignment=ft.MainAxisAlignment.CENTER)

    buttons2 = ft.Row([
        left_btn,
        right_btn,
        drop_btn,
        rotate_btn,
        down_btn
    ],
    alignment=ft.MainAxisAlignment.CENTER)

    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = page_padding
    # page.window_width = main_cont_width + page_padding * 2
    page.window_height = 800
    page.bgcolor = ft.colors.BLUE_GREY_300
    await page.add_async(main_container, buttons, buttons2)

ft.app(target=main)



