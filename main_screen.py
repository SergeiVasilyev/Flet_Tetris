import copy
import flet as ft
from settings import *



class MainScreen():
    def background(self):
        main_cont_padding = BOX_MARGIN*2
        main_cont_width = (BOX_WIDTH + BOX_MARGIN) * 10 + main_cont_padding
        main_cont_height = (BOX_HEIGHT + BOX_MARGIN) * 20 + main_cont_padding

        sidebar = ft.Container(width=150, height=main_cont_height, padding=main_cont_padding, bgcolor="#afb582")

        main_container = ft.GridView(expand=True, max_extent=BOX_WIDTH, child_aspect_ratio=1, spacing=main_cont_padding, run_spacing=main_cont_padding, padding=0)

        main_screen_row = ft.Row([
            ft.Container(main_container, width=main_cont_width, padding=main_cont_padding, bgcolor="#afb582"), 
            sidebar],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=0,
            
        )
        
        stack2 = ft.Stack()
        stack2.controls = [ft.Container(width=INNER_BOX_WIDTH, height=INNER_BOX_HEIGHT, bgcolor=MUTE_COLOR, border_radius=BOX_BORDER_RADIUS)]

        for _ in range(200):
            main_container.controls.append(
                ft.Container(
                    alignment=ft.alignment.center,
                    border=ft.border.all(2, MUTE_COLOR),
                    border_radius=ft.border_radius.all(BOX_BORDER_RADIUS),
                    content=copy.deepcopy(stack2)
                )
            )

        return main_screen_row