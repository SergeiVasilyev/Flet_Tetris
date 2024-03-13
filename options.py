import flet as ft
from main_screen import MainScreen
from settings import *



class Options:
    def __init__(self) -> None:
        self.title = ft.Text("OPTIONS", size=30, color="black")
        self.clockwise = ft.Switch()
        self.reset_highscrore_label = ft.Text(f"{OPTIONS_LABELS[1]} 0", size=16)
        self.reset_highscrore = ft.ElevatedButton("RESET")
        self.save_game = ft.ElevatedButton("SAVE")
        self.load_game = ft.ElevatedButton("LOAD")


    def options_fn(self, container_width, container_height) -> ft.Column:
        title = ft.Container(content=self.title, padding=10, alignment=ft.alignment.center)

        clockwise = ft.Container(content=ft.Row([ft.Text("CLOCKWISE", size=16), self.clockwise], alignment=ft.MainAxisAlignment.SPACE_BETWEEN))
        reset_highscrore = ft.Container(content=ft.Row([self.reset_highscrore_label, self.reset_highscrore], alignment=ft.MainAxisAlignment.SPACE_BETWEEN))
        save_game = ft.Container(content=ft.Row([ft.Text("SAVE GAME", size=16), self.save_game], alignment=ft.MainAxisAlignment.SPACE_BETWEEN))
        load_game = ft.Container(content=ft.Row([ft.Text("LOAD GAME", size=16), self.load_game], alignment=ft.MainAxisAlignment.SPACE_BETWEEN))

        credits_label = ft.Container(content=ft.Text("Autor: Sergey Vasilev, 2024 \nGitHub: https://github.com/SergeiVasilyev/", size=10, color="black"), )

        options = ft.Column([title, clockwise, reset_highscrore, save_game, load_game], spacing=20)

        options_credits = ft.Column([options, credits_label], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        options_container = ft.Container(options_credits, width=container_width, height=container_height, bgcolor="#afb582", padding=10)

        return options_container

