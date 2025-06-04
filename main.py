import asyncio
import flet as ft
from datetime import datetime
from typing import Optional

from settings import *
from buttons_layout import buttons_layout
from main_screen import MainScreen
from tetris import Game
from options import Options
from styles import *

# Import pynput if available 
# For android compatibility wrap in try/except
try:
    from pynput import keyboard
    import threading
    from queue import Queue
    PYNPUT_AVAILABLE = True
except ImportError:
    PYNPUT_AVAILABLE = False



class TetrisApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.is_direction_button_pressed = False
        self.key_events: Optional[Queue] = None
        self.setup_page()
        
        # Initialize game components
        self.tetris = Game()
        self.op = Options()
        
        # Initialize UI after page setup
        asyncio.create_task(self.initialize_ui())
        # self.initialize_ui()
        
        # Setup keyboard handling
        self.setup_keyboard()

    def setup_page(self):
        """Configure page settings"""
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.padding = ft.padding.only(top=PAGE_PADDING, bottom=0, left=0, right=0)
        self.page.window.height = WINDOW_HEIGHT
        self.page.window.width = WINDOW_WIDTH
        self.page.fonts = FONTS
        self.page.bgcolor = PAGE_BACKGROUND_COLOR
        self.page.update()

    async def initialize_ui(self):
        """Initialize all UI components"""
        await self.setup_main_screen()
        await self.setup_dashboard()
        self.setup_buttons()
        self.setup_options()
        self.setup_event_handlers()
        
        # Add main container to page
        wrap = ft.Container(
            content=ft.Column([self.main_screen_wrap, self.buttons_block]),
            gradient=ft.RadialGradient(colors=["#478FBF", "#2980B9"], radius=1), 
            expand=True,
            padding=ft.padding.only(top=WRAP_PADDING_TOP, bottom=0)
        )
        self.page.add(wrap)

    async def setup_main_screen(self):
        """Setup main game screen"""
        self.ms = MainScreen()
        self.main_screen = self.ms.background()
        self.main_screen_stack = self.main_screen.controls.copy()
        self.next_viewer = self.ms.next_tetromino_viewer()
        self.main_container = self.main_screen.controls[0].content

    async def setup_dashboard(self):
        """Initialize dashboard elements"""
        lcd_font = "LCD"
        self.hiscore_label = ft.Text("HI-SCORE", size=15, color="black")
        self.hiscore = ft.Text(f"{self.tetris.hiscore_rw}", size=20, color="black", 
                              font_family=lcd_font, text_align=ft.TextAlign.CENTER)
        self.score_label = ft.Text("SCORE", size=15, color="black")
        self.score = ft.Text("0", size=20, color="black", font_family=lcd_font, 
                            text_align=ft.TextAlign.CENTER)
        self.level_label = ft.Text("LEVEL", size=15, color="black")
        self.level = ft.Text("1", size=20, color="black", font_family=lcd_font)
        self.speed_label = ft.Text("SPEED", size=15, color="black")
        self.speed = ft.Text("1", size=20, color="black", font_family=lcd_font)
        self.next_label = ft.Text("NEXT", size=15, color="black")
        self.game_over_label = ft.Text("", size=15, color="black")

        self.info_container = ft.Container(
            content=ft.Column([
                ft.Column([self.hiscore_label, self.hiscore], 
                         horizontal_alignment=ft.CrossAxisAlignment.END, spacing=5),
                ft.Column([self.score_label, self.score], 
                         horizontal_alignment=ft.CrossAxisAlignment.END, spacing=5),
                ft.Column([self.level_label, self.level], 
                         horizontal_alignment=ft.CrossAxisAlignment.END, spacing=5),
                ft.Column([self.speed_label, self.speed], 
                         horizontal_alignment=ft.CrossAxisAlignment.END, spacing=5),
                ft.Column([self.next_label, self.next_viewer], 
                         horizontal_alignment=ft.CrossAxisAlignment.END, spacing=5),
                ft.Column([self.game_over_label], 
                         horizontal_alignment=ft.CrossAxisAlignment.END, spacing=5),
            ], horizontal_alignment=ft.CrossAxisAlignment.END, spacing=18),
            alignment=ft.alignment.center
        )
        
        self.main_screen.controls[1].content = self.info_container

        self.main_screen_container = ft.Container(
            content=self.main_screen,
            border=ft.border.only(
                bottom=ft.border.BorderSide(4, ft.Colors.BLACK12), 
                right=ft.border.BorderSide(4, ft.Colors.BLACK12), 
                left=ft.border.BorderSide(4, ft.Colors.BLACK38), 
                top=ft.border.BorderSide(4, ft.Colors.BLACK38)),
            border_radius=20,
        )

        self.main_screen_wrap = ft.Row(
            [self.main_screen_container],
            alignment=ft.MainAxisAlignment.CENTER,
        )

    def setup_buttons(self):
        """Initialize control buttons"""
        # Functional buttons
        self.settings_btn = ft.IconButton(
            icon=ft.Icons.SETTINGS, icon_size=14, icon_color="black",
            bgcolor="white", on_click=self.settings, tooltip="Options",
            selected=False, width=30, height=30, style=func_btn_style
        )
        
        self.start_btn = ft.Chip(
            label=ft.Text('Start', color="black"), on_select=self.game,
            shape=ft.StadiumBorder(), elevation=3, shadow_color="black",
            bgcolor="white", label_style=ft.TextStyle(color="black"), 
            tooltip="Start / Pause"
        )
        
        self.restart_btn = ft.IconButton(
            icon=ft.Icons.REPLAY, icon_size=14, icon_color="black",
            bgcolor="white", on_click=self.restart, tooltip="Restart game",
            selected=False, width=30, height=30, style=func_btn_style
        )
        
        # Direction buttons
        self.rotate_btn = direction_btn_style("Rotate", width=135, height=135, border_radius=70)
        self.left_btn = direction_btn_style("Left")
        self.right_btn = direction_btn_style("Right")
        self.up_btn = direction_btn_style("Drop")
        self.down_btn = direction_btn_style("Down")
        
        # Add gesture handlers
        self.rotate_btn_gesture = self.gesture_handler(self.rotate_btn, {}, on_tap_down=self.rotate)
        self.left_btn_gesture = self.gesture_handler(self.left_btn, {"direction": self.left})
        self.right_btn_gesture = self.gesture_handler(self.right_btn, {"direction": self.right})
        self.down_btn_gesture = self.gesture_handler(self.down_btn, {"direction": self.down})
        self.up_btn_gesture = ft.GestureDetector(content=self.up_btn, on_tap=self.drop)
        
        self.buttons_block = buttons_layout(
            [self.start_btn, self.settings_btn, self.restart_btn],
            [self.up_btn_gesture, self.left_btn_gesture, 
             self.right_btn_gesture, self.down_btn_gesture, 
             self.rotate_btn_gesture]
        )

    def setup_options(self):
        """Setup options handlers"""
        self.op.reset_highscrore.on_click = self.reset_highscrore
        self.op.save_game.on_click = self.save_game
        self.op.load_game.on_click = self.load_game
        self.op.clockwise.on_change = self.clockwise

    def setup_event_handlers(self):
        """Setup keyboard event handlers"""
        self.page.on_keyboard_event = self.flet_keyboard

    def setup_keyboard(self):
        """Setup platform-specific keyboard handling"""
        if PYNPUT_AVAILABLE and self.page.platform.value in ["windows", "macos", "linux"]:
            self.key_events = Queue()
            threading.Thread(target=self.start_listener, daemon=True).start()
            asyncio.create_task(self.process_events())

    def gesture_handler(self, content, data, on_tap_down=None):
        """Helper for creating gesture detectors"""
        return ft.GestureDetector(
            content=content,
            on_tap_down=on_tap_down or self.on_tap_handler,
            on_tap_up=self.stop_holding,
            on_pan_end=self.stop_holding,
            data=data
        )

    def refresh_screen(self, refresh=False) -> None:
        """Update game screen"""
        for y in range(20):
            for x in range(10):
                color = BRIGHT_COLOR if refresh and self.tetris.board[y][x] == 1 or \
                    any(block.y == y and block.x == x for block in self.tetris.current_tetromino.shape()) \
                    else MUTE_COLOR
                self.main_container.controls[y*10+x].border = ft.border.all(2, color)
                self.main_container.controls[y*10+x].content.controls[0].bgcolor = color
        self.main_screen.update()

    async def tetromino_show_hide(self, is_show) -> None:
        """
        Update the board with the current tetromino's shape by changing the border and background color of the corresponding controls. 

        Parameters:
            is_show (bool): A flag indicating whether to show or hide the tetromino.
            tetris (Tetris): The Tetris object containing the current tetromino.
        """
        if self.tetris.current_tetromino:
            for block in self.tetris.current_tetromino.shape():
                if block.y >= 0 and block.y <= 20:
                    self.main_container.controls[block.y * 10 + block.x].border = ft.border.all(2, BRIGHT_COLOR if is_show else MUTE_COLOR)
                    self.main_container.controls[block.y * 10 + block.x].content.controls[0].bgcolor = BRIGHT_COLOR if is_show else MUTE_COLOR

    async def next_tetromino_show_hide(self, is_show) -> None:
        """Function to update the next tetromino view based on the provided visibility flag and tetris state.

        :param is_show: bool - Flag to indicate whether to show the next tetromino view
        :param tetris: Tetris - The tetris state object
        """
        shape_or_board = self.tetris.next_tetromino.shape() if is_show else self.tetris.next_tetromino_board
        if shape_or_board:
            for block in shape_or_board:
                self.next_viewer.content.controls[block.y * 4 + block.x].border = ft.border.all(2, BRIGHT_COLOR if is_show else MUTE_COLOR)
                self.next_viewer.content.controls[block.y * 4 + block.x].content.controls[0].bgcolor = BRIGHT_COLOR if is_show else MUTE_COLOR

    async def clear_next_tetromino_field(self):
        """Clear the next tetromino field."""
        for i in range(8):
            self.next_viewer.content.controls[i].border = ft.border.all(2, MUTE_COLOR)
            self.next_viewer.content.controls[i].content.controls[0].bgcolor = MUTE_COLOR

    async def update_dashboard(self):
        """Update the dashboard with the current game statistics including lines, level, score, delay, and speed."""
        self.hiscore.value = f"{self.tetris.hiscore_rw}"
        self.level.value = f"{self.tetris.level}"
        self.score.value = f"{self.tetris.score}"
        self.speed.value = f"{self.tetris.speed}"

    async def clear_lines(self, line, color, l) -> None:
        """Asynchronously clears lines on the main container with a specified color.
        :param line: The line number to clear.
        :param color: The color to use for clearing.
        :param l: Quantity of lines
        """
        for x in range(10):
            self.main_container.controls[line*10+x].border = ft.border.all(2, color)
            self.main_container.controls[line*10+x].content.controls[0].bgcolor = color
        self.main_screen.update()
        await asyncio.sleep(0.06 / l)

    async def filled_line_animation(self, lines) -> None:
        """Asynchronously animates the filled lines on the screen.
        Args:
            lines (List[int]): A list of line numbers to animate.
        """
        if lines:
            color = BRIGHT_COLOR
            for _ in range(2):
                color = MUTE_COLOR if color == BRIGHT_COLOR else BRIGHT_COLOR
                tasks = [self.clear_lines(line, color, len(lines)) for line in lines]
                await asyncio.gather(*tasks)


    async def set_dropped_and_update(self, wait=0.05) -> None:
        """
        An asynchronous function that sets the dropped state of the tetromino in the Tetris game. 
        It takes an optional 'wait' parameter with a default value of 0.05. 
        This function performs collision checks to determine if the tetromino can move, and if not, 
        it drops the tetromino, generates a new one, and updates the dashboard. 
        """
        if self.tetris.collision_check([self.tetris.bottom_condition, self.tetris.board_condition], row=1): 
            await asyncio.sleep(wait) # last chance to move tetromino
            if self.tetris.collision_check([self.tetris.bottom_condition, self.tetris.board_condition], row=1): # check again if tetromino can move
                await self.next_tetromino_show_hide(False) # hide next tetromino on the dashboard
                self.tetris.dropped() # drop the tetromino
                self.tetris.new_tetromino() # Generate new tetromino and reset tetromino row to -1
                await self.update_dashboard() # update the dashboard
                await self.next_tetromino_show_hide(True) # show next tetromino on the dashboard
                await self.filled_line_animation(self.tetris.delete_full_lines_list)
                self.refresh_screen(refresh=True) # refresh the screen

    async def game(self, e):
        """An asynchronous function that controls the game flow, 
        including initialization, updating the dashboard, and handling game over and pause states.
        """
        self.game_over_label.value = ""
        if self.tetris.status != 1: # if game is not running
            if self.tetris.next_tetromino:
                await self.next_tetromino_show_hide(False)
            self.tetris.inits()
            self.refresh_screen()
            await self.update_dashboard()
            await self.next_tetromino_show_hide(True)
        
        # while game is running and not paused
        while self.start_btn.selected and not self.settings_btn.selected:
            self.disable_buttons(disable_direction_buttons=False, disable_function_buttons=False)
            self.start_btn.label = ft.Text('Pause', color="black")
            self.start_btn.selected = True
            self.start_btn.update()
            await self.down_step(delay=self.tetris.delay)

            if self.tetris.status == 2: # if game is over
                self.disable_buttons(disable_direction_buttons=True, disable_function_buttons=False)
                self.refresh_screen()
                self.start_btn.selected = False
                self.start_btn.label = ft.Text('Start', color="black")
                self.start_btn.update()
                self.tetris.status == 0
        else:
            if self.settings_btn.selected:
                self.disable_buttons(disable_direction_buttons=True, disable_function_buttons=True)
            else:
                self.disable_buttons(disable_direction_buttons=True, disable_function_buttons=False)
            self.start_btn.label = ft.Text('Start', color="black")
            self.game_over_label.value = "PAUSE" if self.tetris.status == 1 else "GAME OVER"
            self.page.update()

    async def restart(self, e):
        """
        Restarts the game by clearing the next tetromino field, initializing the tetris game, resetting the screen, and updating the next tetromino view.
        Parameters:
            e: the event that triggers the restart function
        """
        await self.clear_next_tetromino_field()
        self.tetris.inits()
        self.refresh_screen(True)
        await self.next_tetromino_show_hide(True)
        self.main_container.update()


    async def rotate(self, e):
        """Rotates tetromino and updates screen."""
        if not self.start_btn.selected:
            return
        
        await self.tetromino_show_hide(False)
        self.tetris.rotate()
        await self.tetromino_show_hide(True)
        self.main_container.update()


    async def left(self, e):
        """Moves tetromino to the left and updates screen."""
        if not self.start_btn.selected:
            return

        await self.tetromino_show_hide(False)
        self.tetris.left()
        await self.tetromino_show_hide(True)
        self.main_container.update()


    async def right(self, e):
        """Moves tetromino to the right and updates screen."""
        if not self.start_btn.selected:
            return
        
        await self.tetromino_show_hide(False)
        self.tetris.right()
        await self.tetromino_show_hide(True)
        self.main_container.update()


    async def down_step(self, delay):
        """
        Asynchronously moves the current tetromino down, and delays the next action.
        :param delay: The time delay in seconds before the next action.
        """
        await self.down(None)
        await asyncio.sleep(delay) # Main delay

    async def drop(self, e):
        """Drops the current tetromino."""
        if not self.start_btn.selected:
            return
        
        await self.tetromino_show_hide(False)
        while not self.tetris.current_tetromino.row < 0:
            self.tetris.down()
            if self.tetris.collision_check([self.tetris.bottom_condition, self.tetris.board_condition], row=1):
                await self.tetromino_show_hide(True)
                await self.set_dropped_and_update(wait=0.03)
                break
        self.main_screen.update()

    async def down(self, e):
        """Moves the current tetromino down."""
        if not self.start_btn.selected:
            return
        
        await self.set_dropped_and_update()
        if not self.tetris.collision_check([self.tetris.bottom_condition, self.tetris.board_condition], row=1):
            await self.tetromino_show_hide(False)
        self.tetris.down()
        await self.tetromino_show_hide(True)
        self.main_screen.update()


    def disable_buttons(self, disable_direction_buttons=False, disable_function_buttons=False):
        """A function to block buttons."""
        self.start_btn.disabled = disable_function_buttons
        self.restart_btn.disabled = disable_function_buttons
        self.rotate_btn.disabled = disable_direction_buttons
        self.left_btn_gesture.disabled = disable_direction_buttons
        self.right_btn_gesture.disabled = disable_direction_buttons
        self.up_btn_gesture.disabled = disable_direction_buttons
        self.down_btn_gesture.disabled = disable_direction_buttons

    async def settings(self, e):
        """A function to handle settings changes and update the main screen accordingly."""
        options = self.op.options_fn(self.ms.main_cont_width+150, self.ms.main_cont_height)
        self.settings_btn.selected = not self.settings_btn.selected
        self.settings_btn.update()
        if self.settings_btn.selected:
            # Stop game and disable Start and Restart buttons
            self.start_btn.selected = False
            self.start_btn.update()
            self.disable_buttons(disable_direction_buttons=True, disable_function_buttons=True)

            self.op.reset_highscrore_label.value = f"{OPTIONS_LABELS[1]} {self.tetris.hiscore_rw}"
            self.op.load_game_label.value = f"{OPTIONS_LABELS[3]}"
            if self.tetris.date:
                date_format = '%Y-%m-%d %H:%M:%S.%f'
                date_obj = datetime.strptime(self.tetris.date, date_format)
                self.op.save_game_label.value = f"{OPTIONS_LABELS[2]} {date_obj.strftime('%d.%m.%y %H:%M')}"
            
            self.main_screen_stack = self.main_screen.controls.copy()
            self.main_screen.controls[0] = options
            self.main_screen.controls.pop() 
        else:
            # Enable Start and Restart buttons
            self.disable_buttons(disable_direction_buttons=True, disable_function_buttons=False)
            self.main_screen.controls = self.main_screen_stack.copy()
        
        self.page.update()


    def reset_highscrore(self, e):
        """Resets the highscore"""
        self.tetris.hiscore_rw = 0
        self.hiscore.value = 0
        self.op.reset_highscrore_label.value = f"{OPTIONS_LABELS[1]} {self.tetris.hiscore_rw}"
        self.page.update()

    def save_game(self, e):
        """A function that saves the game"""
        if self.tetris.save_game():
            self.op.save_game_label.value = f"{OPTIONS_LABELS[2]} - Game saved"
            self.page.update()
        else:
            self.op.save_game_label.value = f"{OPTIONS_LABELS[2]} - Failed to save"
            self.page.update()

    def load_game(self, e):
        """A function that loads the saved game"""
        if self.tetris.load_game():
            self.op.load_game_label.value = f"{OPTIONS_LABELS[3]} - Game loaded"
            self.refresh_screen(True)
            self.page.update()
        else:
            self.op.load_game_label.value = f"{OPTIONS_LABELS[3]} - Game not found"
            self.page.update()

    def clockwise(self, e: ft.ControlEvent):
        """A function to set the rotation direction"""
        if e.control.value:
            self.tetris.rotate_direction = 1
        else:
            self.tetris.rotate_direction = -1

    # ---Long press handlers---
    async def on_long_press_handler(self, e, fnc_handler):
        """A long press handler to call the specified function every 70 ms.
        
        Args:
            e: an event object
            fnc_handler: a function to call on long press
        """
        while self.is_direction_button_pressed:
            await fnc_handler(e)
            await asyncio.sleep(0.07)


    async def on_tap_handler(self, e: ft.ControlEvent):
        """A tap handler to call the specified function on tap, and then start long press handling.
        
        Args:
            e: an event object, where e.control.data["direction"] is the function to call
        """
        self.is_direction_button_pressed = True
        fnc_handler = e.control.data["direction"]
        await fnc_handler(e)
        await asyncio.sleep(0.08)
        asyncio.create_task(self.on_long_press_handler(e, fnc_handler))


    async def stop_holding(self, e):
        """Stops long press handling by setting is_direction_button_pressed to False."""
        self.is_direction_button_pressed = False

    # ---End of long press handlers---


    # Keyboard events for handle functional buttons
    async def flet_keyboard(self, e: ft.KeyboardEvent):
        if e.key == "Escape" or e.key == "Backspace":
                await self.settings(e)
        if not self.start_btn.disabled:
            if e.key == "R":
                await self.restart(e)
            if e.key == "E" or e.key == "P":
                self.start_btn.selected = not self.start_btn.selected
                self.start_btn.update()
                await self.game(e)

    

    # --- Keyboard events for handle direction keys (pynput) ---
    # It uses queue to store events amd handle holding keys
    # The use of pynput library is due to the fact that Flet does not support following the pressing and releasing of keyboard buttons.

    def on_press(self, key):
        try:
            if self.start_btn.selected:
                if key == keyboard.Key.down or key == keyboard.KeyCode(char='s'):
                    self.key_events.put({"handler": self.down})
                elif key == keyboard.Key.up or key == keyboard.KeyCode(char='w'):
                    self.key_events.put({"handler": self.drop})
                elif key == keyboard.Key.left or key == keyboard.KeyCode(char='a'):
                    self.key_events.put({"handler": self.left})
                elif key == keyboard.Key.right or key == keyboard.KeyCode(char='d'):
                    self.key_events.put({"handler": self.right})
                elif key == keyboard.Key.ctrl_r or key == keyboard.KeyCode(char='f'):
                    self.key_events.put({"handler": self.rotate})
        except Exception as e:
            print("Keyboard event error", e)

    # Keyboard listener thread 
    def start_listener(self):
        """
        A function to start a keyboard listener thread to capture keyboard events.

        The function uses the pynput library to listen for keyboard events and
        invokes the associated event handler functions when a key is pressed.

        The function starts the listener in a separate thread and waits for it to finish.
        """
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()

    # Events handler
    async def process_events(self):
        """
        An asynchronous function to continuously process keyboard events from the event queue.
        It retrieves events from the queue, executes the associated handler asynchronously,
        and sleeps for a short duration to prevent excessive CPU usage.
        """

        while True:
            if not self.key_events.empty():
                event = self.key_events.get()
                fnc = event.get("handler")
                await fnc(None)
            await asyncio.sleep(0.01)


async def main(page: ft.Page):
    """Main entry point"""
    tetris_app = TetrisApp(page)
    page.update()

ft.app(target=main)

