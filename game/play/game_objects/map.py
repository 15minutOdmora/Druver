"""
Module containing different maps.
"""
from __future__ import annotations
import math

import pygame

from game.constants import Paths, join_paths, SCREEN_SIZE
from game.helpers.file_handling import DirectoryReader, ImageLoader


def get_indexes(position: list[int], divisor: list[int]) -> list[int, int]:
    """
    Function calculates integer division of point and a divisor vector.
    Ex. position = point, divisor = tile size => indexes [i, j] of tile in grid where the point lies.
    :param position: list[int, int] position as list
    :param divisor: list[int, int] divisor pair where [xd, yd] xd is divisor on x axis, yd on y axis
    :return: list[int, int] indexes [i, j]
    """
    return [position[1] // divisor[1], position[0] // divisor[0]]


class Tile:
    """
    Tile class for representing a single tile on map.
    """
    def __init__(self, screen: "Display", image: "Image", position: list[int, int], size: list[int, int]):
        """
        :param screen: Currently opened display
        :param image: Image, used as ground
        :param position: Position of tile relative to top-left corner of map
        :param size: Size of tile in [px, px]
        """
        self.screen = screen
        self.image = image
        self.position = position
        self.size = size

    def update(self):
        pass

    def draw(self, offset: list[int, int]) -> None:
        """
        Method draws tile on screen moved by passed offset.
        :param offset: list[int, int] Offset to move tile
        """
        self.screen.blit(self.image, [self.position[0] - offset[0], self.position[1] - offset[1]])


class Map:
    """
    Class representing map.

    Attributes:
        tiles: Grid containing all tiles
        tile_size: Size of one tile
        map_size: Size of map in px
        offset: Offset to move map (based on player)
    """
    def __init__(self, game, folder_name):
        """
        :param game: Current game object
        :param folder_name: Name of map folder saved in assets/maps/
        """
        self.game = game
        self.controller = self.game.controller
        self.screen = pygame.display.get_surface()
        self.screen_size = SCREEN_SIZE
        self.half_screen_width, self.half_screen_height = SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2
        self.folder_name = folder_name
        # These get set by the load_tiles method
        self.tiles: list[list] = None
        self.tile_size = None
        self.number_of_tiles = None
        self.map_size = None
        self.offset = [0, 0]
        # Currently visible tiles
        self.visible_tiles = [[0, 0], [0, 1], [1, 0], [1, 1]]
        # Load all tile data
        self.__load_tiles()

    def __load_tiles(self) -> None:
        """
        Method loads tiles into the tiles list grid.
        """
        folder_path = join_paths(Paths.maps, self.folder_name)
        ground_folder_path = join_paths(folder_path, "ground")
        # TODO: Implement for mask, update for different sized tiles
        ground_images = ImageLoader.load_tiles_from_folder(ground_folder_path)  # Loads every image in a grid
        self.tiles = []
        self.tile_size = ground_images[0][0].get_size()  # Get size of one image
        current_position = [0, 0]
        for i in range(len(ground_images)):
            self.tiles.append([])
            current_position[0] = 0
            for j in range(len(ground_images[i])):
                image = ground_images[i][j]
                # Initializing Tile position by passing current_position, does not work as the initialized position
                # takes the last assigned value of current_position.
                self.tiles[i].append(
                    Tile(
                        self.screen,
                        image,
                        [current_position[0], current_position[1]],
                        self.tile_size
                    )
                )
                current_position[0] += self.tile_size[0]
            current_position[1] += self.tile_size[1]
        self.map_size = (current_position[0], current_position[1])
        self.number_of_tiles = [len(self.tiles), len(self.tiles[0])]

    def update_visible_tiles_indexes(self) -> None:
        """
        Method updates all currently visible tiles.
        """
        # Empty list, and create temporary list
        self.visible_tiles, visible_tiles = [], []
        # Corners
        top_left = get_indexes(
            [int(self.offset[0] - self.half_screen_width), int(self.offset[1] - self.half_screen_height)],
            self.tile_size
        )
        top_right = get_indexes(
            [int(self.offset[0] + self.half_screen_width), int(self.offset[1] - self.half_screen_height)],
            self.tile_size
        )
        bottom_right = get_indexes(
            [int(self.offset[0] - self.half_screen_width), int(self.offset[1] + self.half_screen_height)],
            self.tile_size
        )
        bottom_left = get_indexes(
            [int(self.offset[0] + self.half_screen_width), int(self.offset[1] + self.half_screen_height)],
            self.tile_size
        )
        # Create list
        visible_tiles += [top_left, top_right, bottom_right, bottom_left]
        for indexes in visible_tiles:
            i, j = indexes[0], indexes[1]
            if 0 <= i <= len(self.tiles) - 1:
                if 0 <= j <= len(self.tiles[i]) - 1:
                    self.visible_tiles.append(indexes)

    def update(self) -> None:
        """
        Method updates tiles. (And currently also the offset)
        """
        self.update_visible_tiles_indexes()

    def draw(self) -> None:
        """
        Method draws currently visible tiles on screen based on offset.
        """
        # Draw tiles on calculated positions, move them by offset and half screen size
        offset = [self.offset[0] - self.half_screen_width, self.offset[1] - self.half_screen_height]
        for indexes in self.visible_tiles:
            i, j = indexes[0], indexes[1]
            self.tiles[i][j].draw(offset)
