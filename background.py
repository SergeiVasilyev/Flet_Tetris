import copy
import flet as ft
from flet import Container, Stack


def background():
    class ContainerModified(Container):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.dropped = False

    box_width = 20
    box_height = 20
    box_margin = 3
    box_border_radius = 2
    mute_color = ft.colors.GREY_500
    bright_color = ft.colors.BLACK

    main_cont_padding = box_margin
    main_cont_width = (box_width + box_margin*2) * 10 + main_cont_padding * 2
    main_cont_height = (box_height + box_margin*2) * 20 + main_cont_padding * 2

    stack2 = Stack()
    stack2.controls = [ContainerModified(width=10, height=10, bgcolor=mute_color, margin=box_margin, border_radius=box_border_radius)]

    stack = Stack()
    main_container = ContainerModified(bgcolor="#afb582", content=stack, width=main_cont_width, height=main_cont_height, padding=box_margin)

    for i in range(20):
        for j in range(10):
            stack.controls += [ContainerModified(width=box_width, height=box_height, bgcolor="#afb582", margin=box_margin, border_radius=box_border_radius, border=ft.border.all(2, mute_color), offset=ft.transform.Offset(j, i), content=copy.deepcopy(stack2))]

    return main_container

if __name__ == "__main__":
    def main(page: ft.Page):
        main_container = background()

        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.bgcolor = ft.colors.BLUE_GREY_300
        page.add(main_container)

    ft.app(target=main)