import copy
import flet as ft
from flet import Container, Stack
import random
from tetrominoes import TETROMINOES
from settings import *


class Initialization:
    def __init__(self):
        self.main_container = None
        self.board = []

    def generate_element(self):
        return random.choice([*TETROMINOES])

    def background(self):
        class ContainerModified(Container):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                self.dropped = False
                
        self.main_container = None
        main_cont_padding = box_margin
        main_cont_width = (box_width + box_margin*2) * 10 + main_cont_padding * 2
        main_cont_height = (box_height + box_margin*2) * 20 + main_cont_padding * 2

        stack2 = Stack()
        stack2.controls = [ContainerModified(width=10, height=10, bgcolor=mute_color, margin=3, border_radius=box_border_radius)]

        stack = Stack()
        self.main_container = ContainerModified(bgcolor="#afb582", content=stack, width=main_cont_width, height=main_cont_height, padding=box_margin)

        for i in range(20):
            for j in range(10):
                stack.controls += [ContainerModified(width=box_width, height=box_height, bgcolor="#afb582", margin=box_margin, border_radius=box_border_radius, border=ft.border.all(2, mute_color), offset=ft.transform.Offset(j, i), content=copy.deepcopy(stack2))]

        return self.main_container


    def init(self, restart=False):
        self.board = []
        for _ in range(board_height): # create board
            self.board.append([0 for _ in range(board_width)])
        if restart: 
            for i in range(20): # clear Flet board
                for j in range(10):
                    self.main_container.content.controls[i*10+j].border = ft.border.all(2, mute_color)
                    self.main_container.content.controls[i*10+j].content.controls[0].bgcolor = mute_color
        return self.board

