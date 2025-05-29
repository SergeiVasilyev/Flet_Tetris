import flet as ft
from settings import *



def direction_btn_style(text: str, margin_left=0, width=75, height=75):
    """Generate a style for a button with a specified text and size. The default width and height are 75.
    
    Args:
        text (str): The text to appear on the button.
        margin_left (int, optional): The left margin of the button. Defaults to 0.
        width (int, optional): The width of the button. Defaults to 75.
        height (int, optional): The height of the button. Defaults to 75.
    
    Returns:
        ft.Container: The container with the specified style.
    """
    return ft.Container(content=ft.Text(text, color="black", text_align="center"), 
                        border_radius=50, 
                        width=width, 
                        height=height, 
                        alignment=ft.alignment.center,
                        bgcolor=BTN_COLOR, 
                        margin=ft.margin.only(left=margin_left), 
                        gradient=ft.RadialGradient(
                            colors=[ft.Colors.YELLOW_600, 
                                    ft.Colors.YELLOW_800], 
                                    radius=0.9), 
                        shadow=ft.BoxShadow(
                            blur_radius=3, 
                            spread_radius=1, 
                            color=ft.Colors.GREY_700, 
                            offset=ft.Offset(1, 1)))


func_btn_style = ft.ButtonStyle(shape=ft.CircleBorder(), padding=ft.padding.all(0), color="black", bgcolor="white", shadow_color="black", elevation=3)