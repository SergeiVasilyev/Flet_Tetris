# Flet Tetris Game v1.0.3

My implementation of the console game Tetris from the 90s using the cross-platform Flet framework

Python version ```3.10.9```

Flet version ```0.28.3```

### New in version 1.0.3

Updated the handler for long presses of directional keys, including keyboard presses.

### Mobile version

![alt text for screen readers](https://github.com/SergeiVasilyev/Flet_Tetris/blob/main/Doc/pics/Screen_mobile_03-800.png "Main screen")
![alt text for screen readers](https://github.com/SergeiVasilyev/Flet_Tetris/blob/main/Doc/pics/Screen_mobile_03a-800.png "Settings screen")


### Desctop version
<img src="https://github.com/SergeiVasilyev/Flet_Tetris/blob/main/Doc/pics/Tetris_desctop_main.png" alt="Main screen" style="width:35%; height:auto;"> <img src="https://github.com/SergeiVasilyev/Flet_Tetris/blob/main/Doc/pics/Tetris_desctop_options.png" alt="Settings screen" style="width:35%; height:auto;">


## Installation
```
python -m venv venv
```
```
pip install -r requirements.txt
```

## Run
```
flet main.py
```

## Run in dev mode on Android
```
flet run --android
```
More information here: https://flet.dev/docs/guides/python/testing-on-android

## Build Android apk
```
flet build apk
```
More information here: https://flet.dev/docs/guides/python/packaging-app-for-distribution

## Hotkeys
```
Start / Pause - 'E' or 'P'
Restart - 'R'
Settings - 'Escape' or 'Backspace'
Left - 'A' or 'Arrow Left'
Right - 'D' or 'Arrow Right'
Up - 'W' or 'Arrow Up'
Down - 'S' or 'Arrow Down'
Rotate - 'F' or 'r_ctrl'
```
