"""
Module containing different maps.
"""

from __future__ import annotations
import math
import time

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


class MiniMap:
    """
    Minimap class for creating a minimap object. This accepts an image which is the minimap displayed.
    It needs maps size and players position on the map to draw the player on the minimap.
    Note: The property player position needs to updated at each frame.
    """
    def __init__(self, image, position: list[int, int], map_size: list[int, int]):
        """
        :param image: Loaded Image of minimap
        :param position: Position of minimap on screen
        :param player_position: Players position on map
        :param map_size: Size of map in px
        """
        self.screen = pygame.display.get_surface()
        # Grab images and size data
        # TODO: Add player image on minimap
        self.image = image
        self.image_size = image.get_size()
        self.map_size = map_size
        # Ratio of image_size to map_size, used with multiplication to get player minimap position
        self.minimap_to_map_ratio = [self.image_size[0] / self.map_size[0], self.image_size[1] / self.map_size[1]]
        # Define position
        self.position = position  # This is the position of the image
        self.player_minimap_position = [0, 0]  # Players position on the minimap

    def map_position_to_minimap_position(self, map_position: list[int, int]) -> None:
        """
        Method updates the players position on the minimap, position is based on the top-left corner of the
        minimap image. Players position on map gets passed as argument.

        :param map_position: Position of player on map
        """
        self.player_minimap_position[0] = int(map_position[0] * self.minimap_to_map_ratio[0])
        self.player_minimap_position[1] = int(map_position[1] * self.minimap_to_map_ratio[1])

    def update(self, map_position: list[int, int]) -> None:
        """
        Method updates players position on the minimap based on the position of player on map.

        :param map_position: Position of player on map.
        """
        self.map_position_to_minimap_position(map_position)

    def draw(self) -> None:
        """
        Method draws minimap on screen along with player.
        """
        # Draw image
        self.screen.blit(self.image, self.position)
        # Draw player as circle, TODO: Draw player as passed image
        player_pos = [self.position[0] + self.player_minimap_position[0],
                      self.position[1] + self.player_minimap_position[1]]
        pygame.draw.circle(self.screen, (255, 30, 40), player_pos, 4)


class Tile:
    """
    Tile class for representing a single tile on map.
    """
    def __init__(self, screen: "Display", image: "Image", mask_image: "Image", position: list[int, int], size: list[int, int]):
        """
        :param screen: Currently opened display
        :param image: Image, used as ground
        :param position: Position of tile relative to top-left corner of map
        :param size: Size of tile in [px, px]
        """
        self.screen = screen
        self.image = image
        self.mask_image = mask_image
        self.position = position
        self.size = size

    def get_mask_value_at_point(self, point):
        return self.mask_image.get_at(point)

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
    def __init__(self, controller, folder_name):
        """
        :param game: Current game object
        :param folder_name: Name of map folder saved in assets/maps/
        """
        self.controller = controller
        self.screen = pygame.display.get_surface()
        self.screen_size = SCREEN_SIZE
        self.half_screen_width, self.half_screen_height = SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2
        self.folder_name = folder_name
        self.folder_path = join_paths(Paths.maps, self.folder_name)
        # These get set by the load_tiles method
        self.tiles: list[list] = None
        self.mask_tiles: list[list] = None
        self.tile_size = None
        self.number_of_tiles = None
        self.map_size = None
        self.offset = [0, 0]
        # Currently visible tiles
        self.visible_tiles = [[0, 0], [0, 1], [1, 0], [1, 1]]
        # Load all tile data
        self.__load_tiles()
        # Load minimap and create object, load after map loading so map size is set
        minimap_image = ImageLoader.load_transparent_image(join_paths(self.folder_path, "minimap.png"))
        self.minimap = MiniMap(
            image=minimap_image,
            position=[10, 575],
            map_size=self.map_size
        )

    def __load_tiles(self) -> None:
        """
        Method loads tiles into the tiles list grid.
        """
        start_time = time.time()
        ground_folder_path = join_paths(self.folder_path, "ground")
        mask_folder_path = join_paths(self.folder_path, "mask")
        ground_images = ImageLoader.load_tiles_from_folder(ground_folder_path)  # Loads every image in a grid
        mask_images = ImageLoader.load_tiles_from_folder(mask_folder_path)
        self.tiles = []
        self.tile_size = ground_images[0][0].get_size()  # Get size of one image
        current_position = [0, 0]
        for i in range(len(ground_images)):
            self.tiles.append([])
            current_position[0] = 0
            for j in range(len(ground_images[i])):
                image = ground_images[i][j]
                mask_image = ground_images[i][j]
                # Initializing Tile position by passing current_position, does not work as the initialized position
                # takes the last assigned value of current_position.
                self.tiles[i].append(
                    Tile(
                        self.screen,
                        image,
                        mask_image,
                        [current_position[0], current_position[1]],
                        self.tile_size
                    )
                )
                current_position[0] += self.tile_size[0]
            current_position[1] += self.tile_size[1]
        self.map_size = (current_position[0], current_position[1])
        self.number_of_tiles = [len(self.tiles), len(self.tiles[0])]
        print(f"Map loading took: {time.time() - start_time}s")

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
        # Update minimap player map position
        self.minimap.update(self.offset)

    def draw(self) -> None:
        """
        Method draws currently visible tiles on screen based on offset.
        """
        # Draw tiles on calculated positions, move them by offset and half screen size
        offset = [self.offset[0] - self.half_screen_width, self.offset[1] - self.half_screen_height]
        for indexes in self.visible_tiles:
            i, j = indexes[0], indexes[1]
            self.tiles[i][j].draw(offset)
        # Draw minimap
        self.minimap.draw()
