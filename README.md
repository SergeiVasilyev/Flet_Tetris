# Flet Tetris game

An attempt to implement a portable Tetris game from the 90s using cross platform Flet framework

Python version 3.10.11
Flet version 0.21.1

### Mobile version

![alt text for screen readers](https://github.com/SergeiVasilyev/Flet_Tetris/blob/main/Doc/pics/Screen_mobile_02-800.png "Text to show on mouseover")

### Desctop version

![alt text for screen readers](https://github.com/SergeiVasilyev/Flet_Tetris/blob/main/Doc/pics/Screen_06.png "Text to show on mouseover")



## Installation
```
python -m venv venv
```
```
pip install -r requirements.txt
```

## Run
```
python main.py
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


## TODO

- Reset highscore
- Game saving
- Options (Color, Clockwise)
- Hotkeys for desctop version


