import asyncio
from functools import reduce
import flet as ft
from tetrominoes import TETROMINOES
from initialization import background, init, generate_element
from settings import *



row_position = -1
col_position = 3

board = init()
main_container = background()
tetramino = TETROMINOES[generate_element()]
tetromino_blocks_positions = []



def draw(drawing):
    global board, tetromino_blocks_positions, row_position, col_position, tetramino
    tetromino_blocks_positions = []
    for x, y in tetramino:
        board[y+row_position][x+col_position] = 1 if drawing else 0
        tetromino_blocks_positions.append([(y+row_position)*10+(x+col_position), y+row_position, x+col_position])
    return board

def vertical_collision():
    global tetromino_blocks_positions
    for i in tetromino_blocks_positions:
        if i[1] >= 19:
            return True
        elif board[i[1]+1][i[2]] == -1:
            return True
    return False

def mark_as_dropped():
    for j in tetromino_blocks_positions:
        board[j[1]][j[2]] = -1 # mark as dropped

def horizontal_collision(x):
    for i in tetromino_blocks_positions:
        if x + i[2] < 0 or x + i[2] > 9:
            return True
    return False

def element_length(tetramino):
    max_len = 0
    res = reduce(lambda x, y: [x[i] or y[i] for i in range(len(x))], tetramino)
    max_len = sum(res)
    return max_len

def is_full():
    if -1 in board[1]:
        return True
    return False

def path_correction(new_element):
    global tetramino, col_position, row_position
    for el in new_element:
        if el[0] + col_position > 9:
            col_position = 9 - el[0]
        elif el[0] + col_position < 0:
            col_position = 0 - el[0]
        elif el[1] + row_position > 19:
            row_position = 19 - el[1]
        elif el[1] + row_position < 0:
            row_position = 0 - el[1]
    return new_element

async def main(page: ft.Page):
    global board, tetromino_blocks_positions, row_position, col_position, tetramino, main_container

    def draw_element(drawing):
        global board, tetromino_blocks_positions, main_container
        draw(drawing)
        print(tetromino_blocks_positions)
        for el in tetromino_blocks_positions:
            main_container.content.controls[el[0]].border = ft.border.all(2, bright_color if drawing else mute_color)
            main_container.content.controls[el[0]].content.controls[0].bgcolor = bright_color if drawing else mute_color

    async def refresh_bord():
        for i in range(20):
            for j in range(10):
                main_container.content.controls[i*10+j].border = ft.border.all(2, bright_color if board[i][j] == -1 else mute_color)
                main_container.content.controls[i*10+j].content.controls[0].bgcolor = bright_color if board[i][j] == -1 else mute_color
        await page.update_async()

    def remove_line(row):
        while row != 0:
            board[row] = board[row - 1][:]
            row -= 1

    async def is_line_complete():
        for i in range(board_height):
            if -1 in board[i]:
                if abs(sum(board[i])) == board_width:
                    remove_line(i)
                    await refresh_bord()
        return True

    async def animate(e):
        global row_position, col_position, tetramino
        if row_position != -1:
            draw_element(False)
        row_position += 1
        draw_element(True)
        if is_full():
            init(True)
        if vertical_collision():
            mark_as_dropped()
            await is_line_complete()
            row_position = -1
            col_position = 3
            tetramino = TETROMINOES[generate_element()]
        await page.update_async()

    async def game(e):
        global row_position, col_position, tetramino
        while True:
            await animate(None)
            await asyncio.sleep(1)
            
            
    async def drop(e):
        global row_position
        while row_position != -1:
            await animate(None)


    async def restart(e):
        global main_container
        init(True)
        await page.update_async()
    
    
    async def rotate(e):
        global tetramino
        if row_position >= 0:
            draw_element(False)
            rotated_element = [(-y, x) for x, y in tetramino]
            tetramino = path_correction(rotated_element)
            draw_element(True)
            await page.update_async()

    async def left(e):
        global col_position
        if row_position >= 0:
            draw_element(False)
            if not horizontal_collision(-1):
                col_position -= 1
            draw_element(True)
            await page.update_async()

    async def right(e):
        global col_position
        if row_position >= 0:
            draw_element(False)
            if not horizontal_collision(1):
                col_position += 1
            draw_element(True)
            await page.update_async()
    

    button = ft.ElevatedButton("START!", on_click=game)
    drop_btn = ft.ElevatedButton("Drop!", on_click=drop)
    restart_btn = ft.ElevatedButton("Restart!", on_click=restart)
    rotate_btn = ft.ElevatedButton("Rotate", on_click=rotate)
    left_btn = ft.ElevatedButton("Left", on_click=left)
    right_btn = ft.ElevatedButton("Right", on_click=right)

    buttons = ft.Row([
        button,
        restart_btn,
    ],
    alignment=ft.MainAxisAlignment.CENTER)

    buttons2 = ft.Row([
        left_btn,
        right_btn,
        drop_btn,
        rotate_btn
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



