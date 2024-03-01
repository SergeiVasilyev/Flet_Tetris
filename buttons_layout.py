import flet as ft
from settings import *



def buttons_layout(func_buttons, directions):
    start_btn, restart_btn = func_buttons
    up_btn, left_btn, right_btn, drop_btn, rotate_btn = directions
    
    # Func buttons
    func_buttons = ft.Row([start_btn, restart_btn], alignment=ft.MainAxisAlignment.END)
    func_buttons_container = ft.Container(
        content=func_buttons,
    )

    # Direction buttons
    botton_row1 = ft.Row([up_btn], 
           alignment=ft.MainAxisAlignment.CENTER
           )
    botton_row2 = ft.Row([left_btn, right_btn], 
           alignment=ft.MainAxisAlignment.SPACE_BETWEEN
           )
    botton_row3 = ft.Row([drop_btn], 
           alignment=ft.MainAxisAlignment.CENTER
           )
    container = ft.Container(
        content=botton_row1,
    )
    container2 = ft.Container(
        content=botton_row2,
    )
    container3 = ft.Container(
        content=botton_row3,
    )

    direction_buttons_col = ft.Column(
        [container, container2, container3],
        horizontal_alignment=ft.CrossAxisAlignment.START,
        width=240,
        spacing=0
    )

    botton_row4 = ft.Row(
        [rotate_btn],
    )
    container4 = ft.Container(
        content=botton_row4,
    )
    rotate_button_col = ft.Column(
        [container4],
    )

    direction_rotation_row = ft.Row(
        [direction_buttons_col, rotate_button_col],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    buttons_block = ft.Column(
        [func_buttons_container, direction_rotation_row],
        width=550,
        spacing=10
    )

    return buttons_block