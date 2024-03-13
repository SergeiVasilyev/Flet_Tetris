import flet as ft
from main_screen import MainScreen


# ms = MainScreen()
# main_screen = ms.background()

def options_fn(ms):

    title = ft.Container(content=ft.Text("OPTIONS", size=30, color="black"), padding=10, alignment=ft.alignment.center)
    clockwise = ft.Container(content=ft.Row([ft.Text("CLOCKWISE", size=16), ft.Switch()], alignment=ft.MainAxisAlignment.SPACE_BETWEEN))
    reset_highscrore = ft.Container(content=ft.Row([ft.Text("RESET HIGHSCORE", size=16), ft.ElevatedButton("RESET")], alignment=ft.MainAxisAlignment.SPACE_BETWEEN))
    save_game = ft.Container(content=ft.Row([ft.Text("SAVE GAME", size=16), ft.ElevatedButton("SAVE")], alignment=ft.MainAxisAlignment.SPACE_BETWEEN))
    load_game = ft.Container(content=ft.Row([ft.Text("LOAD GAME", size=16), ft.ElevatedButton("LOAD")], alignment=ft.MainAxisAlignment.SPACE_BETWEEN))
    credits_label = ft.Container(content=ft.Text("Autor: Sergey Vasilev, 2024 \nGitHub: https://github.com/SergeiVasilyev/", size=10, color="black"), )

    options = ft.Column([title, clockwise, reset_highscrore, save_game, load_game], spacing=20)

    options_credits = ft.Column([options, credits_label], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    options_container = ft.Container(options_credits, width=ms.main_cont_width+150, height=ms.main_cont_height, bgcolor="#afb582", padding=10)

    return options_container

    # main_screen.controls[0] = options_container
    # main_screen.controls.pop()

# if __name__ == '__main__':
#     def main(page: ft.Page):
#         page.add(main_screen)

#     ft.app(target=main)
