import copy
import flet as ft
from settings import *



class MainScreen():

    def __init__(self):
        self.main_cont_padding = BOX_MARGIN*2
        self.main_cont_width = (BOX_WIDTH + BOX_MARGIN) * 10 + self.main_cont_padding
        self.main_cont_height = (BOX_HEIGHT + BOX_MARGIN) * 20 + self.main_cont_padding

    def background(self):
        """A function to generate the background layout for the main screen."""
        sidebar = ft.Container(width=150, height=self.main_cont_height, padding=self.main_cont_padding, bgcolor="#afb582")

        main_container = ft.GridView(expand=True, max_extent=BOX_WIDTH, child_aspect_ratio=1, spacing=self.main_cont_padding, run_spacing=self.main_cont_padding, padding=0)

        main_screen_row = ft.Row([
            ft.Container(main_container, width=self.main_cont_width, padding=self.main_cont_padding, bgcolor="#afb582",), 
            sidebar],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=0,
            
        )
        
        stack2 = ft.Stack()
        stack2.controls = [ft.Container(width=INNER_BOX_WIDTH, height=INNER_BOX_HEIGHT, bgcolor=MUTE_COLOR, border_radius=BOX_BORDER_RADIUS) ]

        for _ in range(200):
            main_container.controls.append(
                ft.Container(
                    alignment=ft.alignment.center,
                    border=ft.border.all(2, MUTE_COLOR),
                    border_radius=ft.border_radius.all(BOX_BORDER_RADIUS),
                    content=copy.deepcopy(stack2),
                )
            )

        return main_screen_row
    

    def next_tetromino_viewer(self):
        """A function to generate the next tetromino viewer layout"""
        width = (BOX_WIDTH + BOX_MARGIN) * 4 + self.main_cont_padding

        next_container_grid = ft.GridView(expand=True, max_extent=BOX_WIDTH, child_aspect_ratio=1, spacing=self.main_cont_padding, run_spacing=self.main_cont_padding, padding=0)
        next_container = ft.Container(next_container_grid, width=width, padding=self.main_cont_padding, bgcolor="#afb582")

        stack = ft.Stack()
        stack.controls = [ft.Container(width=INNER_BOX_WIDTH, height=INNER_BOX_HEIGHT, bgcolor=MUTE_COLOR, border_radius=BOX_BORDER_RADIUS)]

        for _ in range(8):
            next_container_grid.controls.append(
                ft.Container(
                    alignment=ft.alignment.center,
                    border=ft.border.all(2, MUTE_COLOR),
                    border_radius=ft.border_radius.all(BOX_BORDER_RADIUS),
                    content=copy.deepcopy(stack)
                )
            )
        return next_container
    

if __name__ == '__main__':
    m = MainScreen()
    n = m.next_tetromino_viewer()
    n.content.controls[0].border = ft.border.all(2, BRIGHT_COLOR)
    
