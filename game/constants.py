"""
Module containing game wide constants like paths, screen sizes, ...
"""

NAME = "Druver"

SCREEN_SIZE = (1280, 720)

FPS_CAP = 60


class Colors:
    white = (255, 255, 255)
    black = (0, 0, 0)


class BaseColors:
    background = Colors.black
    items = Colors.white

    button_outline = Colors.white
    button_fill = Colors.black

    main_text = Colors.white
