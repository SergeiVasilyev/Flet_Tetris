import flet as ft
from settings import *

class MainScreen:
    def __init__(self):
        self.main_cont_padding = BOX_MARGIN * 2
        self.main_cont_width = (BOX_WIDTH + BOX_MARGIN) * 10 + self.main_cont_padding
        self.main_cont_height = (BOX_WIDTH + BOX_MARGIN) * 20 + self.main_cont_padding
        
        # Pre-create common container styles
        self._bg_style = {
            "bgcolor": MAIN_SCREEN_BGCOLOR,
            "padding": self.main_cont_padding
        }
        
        # Pre-create box template
        self._box_template = self._create_box_template()

    def _create_box_template(self):
        """Create a reusable box template to avoid deepcopy"""
        inner_box = ft.Container(
            width=INNER_BOX_WIDTH,
            height=INNER_BOX_HEIGHT,
            bgcolor=MUTE_COLOR,
            border_radius=BOX_BORDER_RADIUS
        )
        
        return ft.Container(
            alignment=ft.alignment.center,
            border=ft.border.all(2, MUTE_COLOR),
            border_radius=ft.border_radius.all(BOX_BORDER_RADIUS),
            content=ft.Stack([inner_box])
        )

    def _create_grid_container(self, columns: int, rows: int) -> ft.Container:
        """Helper method to create a grid container with specified dimensions"""
        grid = ft.GridView(
            expand=True,
            max_extent=BOX_WIDTH,
            child_aspect_ratio=1,
            spacing=self.main_cont_padding,
            run_spacing=self.main_cont_padding,
            padding=0
        )
        
        # Add boxes to grid
        grid.controls.extend(
            self._create_box_template() for _ in range(columns * rows)
        )
        
        return ft.Container(
            grid,
            width=(BOX_WIDTH + BOX_MARGIN) * columns + self.main_cont_padding,
            **self._bg_style
        )

    def background(self) -> ft.Row:
        """Create the main game screen background layout"""
        main_container = self._create_grid_container(10, 20)
        sidebar = ft.Container(
            width=150,
            height=self.main_cont_height,
            **self._bg_style
        )
        
        return ft.Row(
            [main_container, sidebar],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=0
        )

    def next_tetromino_viewer(self) -> ft.Container:
        """Create the next tetromino preview container"""
        return self._create_grid_container(4, 2)