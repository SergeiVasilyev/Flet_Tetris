import flet as ft
from settings import *



def buttons_layout(func_buttons, directions) -> ft.Column:
    """Generates a layout for buttons based on the provided functional buttons and directions.
    Args:
        func_buttons: A tuple containing the start button and restart button.
        directions: A tuple containing the up button, left button, right button, drop button, and rotate button.

    Returns:
        The layout for the buttons block.
    """

    up_btn, left_btn, right_btn, drop_btn, rotate_btn = directions
    
    # Func buttons
    func_buttons = ft.Row([*func_buttons], alignment=ft.MainAxisAlignment.END, spacing=20)
    func_buttons_container = ft.Container(
        content=func_buttons,
        padding=ft.Padding(0, 0, 20, 0),
    )

    # Direction buttons
    botton_row1 = ft.Row([up_btn], 
           alignment=ft.MainAxisAlignment.CENTER, spacing=0
           )
    botton_row2 = ft.Row([left_btn, right_btn], 
           alignment=ft.MainAxisAlignment.SPACE_BETWEEN, spacing=0
           )
    botton_row3 = ft.Row([drop_btn], 
           alignment=ft.MainAxisAlignment.CENTER, spacing=0
           )
    container = ft.Container(
        content=botton_row1, padding=0
    )
    container2 = ft.Container(
        content=botton_row2, padding=0
    )
    container3 = ft.Container(
        content=botton_row3, padding=0
    )

    direction_buttons_col = ft.Container(
        ft.Column(
            [container, container2, container3],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            width=220,
            spacing=0,
        ),
        alignment=ft.alignment.center,
        padding=ft.Padding(20, 0, 0, 0),
    )

    botton_row4 = ft.Row(
        [rotate_btn],
        spacing=0
    )

    container4 = ft.Container(
        content=botton_row4,
        padding=ft.Padding(0, 0, 20, 0),

    )

    rotate_button_col = ft.Column(
        [container4],
    )

    direction_rotation_row = ft.Container(
        ft.Row(
            [direction_buttons_col, rotate_button_col],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        alignment=ft.alignment.center,
    )

    buttons_block = ft.Container(
        ft.Column(
            [func_buttons_container, direction_rotation_row],
            width=550,
            spacing=10,
        ),
        alignment=ft.alignment.center,
    )

    return buttons_block