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
                    tetris.score += 1
                    info.value = f'Score: {tetris.score}'
                    await page.update_async()
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
        # print(start_btn.on_click)
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

    # async def down(e):
    #     print(e.control.bgcolor, e.data)
    #     print('down')
    #     e.control.bgcolor = "blue" if e.data == "true" else "yellow"
    #     await e.control.update_async()
        # e.control.update()
        # while tetris.row_position != -1:
        #     await animate(e)

    async def on_click(e: ft.LongPressEndEvent):
        print(e.control, e.data)
        print('down')
        e.control.bgcolor = "blue" if e.data == "true" else "yellow"
        await e.control.update_async()

    func_btn_style = ft.ButtonStyle(
        shape=ft.CircleBorder(),
        padding=ft.padding.all(10),
    )
        
    direction_btn_style = ft.ButtonStyle(shape=ft.CircleBorder(), padding=35, bgcolor=BTN_COLOR)
    rotate_btn_style = ft.ButtonStyle(shape=ft.CircleBorder(), padding=60, bgcolor=BTN_COLOR)

    start_btn = ft.ElevatedButton("S", on_click=game, data=True, style=func_btn_style)
    restart_btn = ft.ElevatedButton("R", on_click=restart, style=func_btn_style)
    func_buttons = ft.Row([start_btn, restart_btn], alignment=ft.MainAxisAlignment.END)
    func_container = ft.Container(
        content=func_buttons,
    )

    rotate_btn = ft.ElevatedButton("Rotate", on_click=rotate, style=rotate_btn_style)

    left_btn = ft.ElevatedButton("Left", on_click=left, on_long_press=left_long, style=direction_btn_style)
    right_btn = ft.ElevatedButton("Right", on_click=right, on_long_press=right_long, style=direction_btn_style)
    up_btn = ft.ElevatedButton("Up", on_click=drop, style=direction_btn_style)
    drop_btn = ft.ElevatedButton("Drop", on_click=drop, style=direction_btn_style)
    down_btn = ft.ElevatedButton("Down", on_click=drop, style=direction_btn_style)

    buttons1 = ft.Row([up_btn], 
           alignment=ft.MainAxisAlignment.CENTER
           )
    buttons2 = ft.Row([left_btn, right_btn], 
           alignment=ft.MainAxisAlignment.SPACE_BETWEEN
           )
    buttons3 = ft.Row([drop_btn], 
           alignment=ft.MainAxisAlignment.CENTER
           )
    container = ft.Container(
        content=buttons1,
        # border=ft.border.all(1, ft.colors.BLACK),
    )
    container2 = ft.Container(
        content=buttons2,
        # border=ft.border.all(1, ft.colors.BLACK),
    )
    container3 = ft.Container(
        content=buttons3,
        # border=ft.border.all(1, ft.colors.BLACK),
    )

    column = ft.Column(
        [container, container2, container3],
        horizontal_alignment=ft.CrossAxisAlignment.START,
        width=240,
        spacing=0
    )

    button4 = ft.Row(
        [rotate_btn],
    )
    container4 = ft.Container(
        content=button4,
    )
    column4 = ft.Column(
        [container4],
    )

    row_main = ft.Row(
        [column, column4],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    col_main = ft.Column(
        [func_container, row_main],
        width=550,
        spacing=10
    )

    info = ft.Text(f"Score: {tetris.score}", size=20)
    info_container = ft.Container(
        content=info
    )

    tetris_row = ft.Row(
        [main_container, info_container],
        alignment=ft.MainAxisAlignment.CENTER
    )

    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = page_padding
    # page.window_width = main_cont_width + page_padding * 2
    page.window_height = 800
    page.window_width = 500
    page.bgcolor = ft.colors.BLUE_GREY_300
    await page.add_async(tetris_row, col_main)

ft.app(target=main)



