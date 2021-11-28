"""
Module containing game wide constants like paths, screen sizes, ...
"""

import os

NAME = "Druver"
SCREEN_SIZE = (1280, 720)
FPS_CAP = 60

DEVELOPMENT_URL = "https://github.com/15minutOdmora/Druver"


class Colors:
    white = (255, 255, 255)
    black = (0, 0, 0)


class BaseColors:
    background = Colors.black
    items = Colors.white

    button_outline = Colors.white
    button_fill = Colors.black

    main_text = Colors.white


def abs_path(relative_path):
    return os.path.abspath(relative_path)


def join_paths(path1, *paths):
    return os.path.join(path1, *paths)


class Paths:
    # Files are caps-lock directories are normally written
    assets = abs_path("game/assets")

    # Fonts
    fonts = join_paths(assets, "fonts")

    lo_res = join_paths(fonts, "lo-res")
    LO_RES_NARROW = join_paths(lo_res, "Lo-Res_22_Narrow.ttf")
    LO_RES_SERIF = join_paths(lo_res, "Lo-Res_22_Serif.ttf")

    # images
    images = join_paths(assets, "images")
    backgrounds = join_paths(images, "backgrounds")
    logo = join_paths(images, "logo")
    DRUVER_BIG_LOGO = join_paths(logo, "druver_big_logo.png")

    # maps
    maps = join_paths(assets, "maps")

    # objects
    objects = join_paths(assets, "objects")
    cars = join_paths(objects, "cars")

    # sounds
    sounds = join_paths(assets, "sounds")
    radio = join_paths(assets, "radio")

    buttons = join_paths(images, "buttons")
    start_game_button = join_paths(buttons, "start_game_button")
