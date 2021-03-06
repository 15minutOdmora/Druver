"""
Module for anything related to files
"""

from __future__ import annotations
from typing import Callable
import os
import time
import json

import pygame

from game.constants import Paths, join_paths


def abs_path(path: str) -> str:
    """
    Function gets the absolute path given certain path.
    :param path: Relative path
    :return: Absolute path
    """
    return os.path.abspath(path)


def get_indexes_from_string(in_str: str) -> list:
    """
    Function converts strings like '001' into list [0, 0, 1]
    :param in_str: Input string to convert
    :return: tuple with converted values
    """
    num_list = []
    for char in in_str:
        try:
            num_list.append(int(char))
        except ValueError:
            num_list.append(None)
    return num_list


class ImageLoader:
    @staticmethod
    def load_image(image_path: str) -> "Surface":
        """
        Method loads given path into image.
        """
        return pygame.image.load(abs_path(image_path)).convert()  # .convert() optimizes speed by 5x

    @staticmethod
    def load_transparent_image(image_path: str):
        """
        Method loads given path into image.

        Args:
            image_path (str): Path to image to load

        Returns:
            image: Image from the pygame image module
        """
        return pygame.image.load(abs_path(image_path)).convert_alpha()  # .convert() optimizes speed by 5x

    @staticmethod
    def load_folder(folder_path: str) -> list:
        """
        Method loads all ImageLoader from the folder intro a sprite list.

        Args:
            folder_path (str): Path to folder to load images from

        Returns:
            list: List containing pygame images
        """
        image_list = []
        for image_path in os.listdir(folder_path):
            path = os.path.join(folder_path, image_path)
            image_list.append(ImageLoader.load_image(path))
        return image_list

    @staticmethod
    def load_transparent_folder(folder_path: str) -> list:
        """
        Method loads all ImageLoader from the folder intro a sprite list.

        Args:
            folder_path (str): Path to folder to load images from

        Returns:
            list: List containing pygame images
        """
        image_list = []
        for image_path in os.listdir(folder_path):
            path = os.path.join(folder_path, image_path)
            image_list.append(ImageLoader.load_transparent_image(path))
        return image_list

    @staticmethod
    def load_tiles_from_folder(
            folder_path: str,
            update_method: Callable = lambda _: _,
            currently_loading: str = "") -> list[list[tuple]]:
        """
        Method loads tiles from folder, where each tile is an image with the name ij.format where i, j represent
        position on of tile in grid.
        Optional currently_loading parameter can be passed as a callable function with one parameter, this function
        gets called for every tile load, tile positioning in grid, and 2 times before hand and once after, passing
        string representing current action.
        Another optional argument currently_loading can be passed which gets placed before the string representing
        current action on update_method call.
        :param folder_path: str path to folder to load from
        :param update_method: Callable function with one parameter which gets called on different progress occasions
        :param currently_loading: str that gets placed beforehand of current action string passed to update_method
        :return:
        """
        update_method(currently_loading + " fetching files.")
        images = DirectoryReader.get_all_files(folder_path)
        update_method(currently_loading + " sorting file names.")
        rows, columns = [], []
        for name, path in images:
            update_method(currently_loading + f" checking {name}")
            indexes = name.split(".")[0]  # Get left side of.
            try:
                rows.append(int(indexes[0]))
                columns.append(int(indexes[1]))
            except ValueError:
                raise ValueError(f"Loading tiles format error, incorrect format for image: {name} in folder: {folder_path}")
        # Create grid based on max values from rows and columns
        grid = [[None for j in range(max(columns) + 1)] for i in range(max(rows) + 1)]  # Add 1 as indexing starts at 0
        # Add images to grid
        for name, path in images:
            indexes = get_indexes_from_string(name.split(".")[0])
            update_method(currently_loading + f" loading tile {indexes[0]}, {indexes[1]}")
            grid[indexes[0]][indexes[1]] = ImageLoader.load_image(path)
        update_method(currently_loading + f" finished.")
        return grid

    @staticmethod
    def get_number_of_files(folder_path: str) -> int:
        """
        Function returns number of items in given directory.
        :param folder_path: str Path to folder
        :return: int Number of files in given folder
        """
        return len(os.listdir(folder_path))


class DirectoryReader:
    @staticmethod
    def get_all_folders(dir_path: str) -> list[tuple]:
        """
        Method finds all folder names and its paths in the given path.

        Args:
            dir_path (str): Path to directory to search from

        Returns:
            tuple: 1st. element is name of folder, second is path.
        """
        folder_list = []
        for item in os.scandir(dir_path):
            if item.is_dir():
                folder_list.append((item.name, os.path.abspath(item.path)))
        return folder_list

    @staticmethod
    def get_all_files(dir_path: str) -> list[tuple]:
        """
        Method finds all file names and its paths in the given path.

        Args:
            dir_path (str): Path to directory to search from

        Returns:
            list[tuple]: Where the key is the name of the file and the value is its path
        """
        file_list = []
        for item in os.scandir(dir_path):
            if item.is_file():
                file_list.append((item.name, os.path.abspath(item.path)))  # Append tuple
        return file_list

    @staticmethod
    def get_map_previews(map_folder_path: str = Paths.maps) -> list:
        """
        Method loads a list of map previews where it loads each maps data in a dict and then returns a list of
        dictionaries.
        :param map_folder_path: str path to folder containing map folders
        :return: list -> todo: example of dict
        """
        map_previews = []
        all_map_folders = DirectoryReader.get_all_folders(map_folder_path)
        for name, path in all_map_folders:
            if "_" in name:
                continue
            map_dict = {"name": name,
                        "image": join_paths(path, "preview.png")
                        }
            # Todo Add loading of properties json about map
            map_previews.append(map_dict)
        return map_previews

    @staticmethod
    def get_car_previews(car_folder_path: str = Paths.cars) -> list:
        """
        Method loads a list of car previews where it loads each cars data in a dict and then returns a list of
        dictionaries.
        :param car_folder_path: str path to folder containing car folders
        :return: list -> todo: example of dict
        """
        car_previews = []
        all_car_folders = DirectoryReader.get_all_folders(car_folder_path)
        for name, path in all_car_folders:
            if "_" in name:
                continue
            car_dict = {"name": name,
                        "preview": join_paths(path, "preview")
                        }
            # Todo Add loading of config json
            car_previews.append(car_dict)
        return car_previews


class Json:
    """
    Class for loading, writing and updating data in json files.
    All json files must contain dictionaries as the main scope object.
    """
    @staticmethod
    def load(path: str) -> dict:
        """
        Method loads a single json file, returning its contents.

        :param path: Path to Json file
        :return: dict or list, content of the Json file
        """
        try:
            with open(path, "r") as f:
                data = json.load(f)
            return data
        except FileNotFoundError:
            print(f"Json.load: Unable to find Json file on path:\n    {path}")

    @staticmethod
    def update(path: str, data: dict) -> dict:
        """
        Method will update the dictionary with data and return the updated dict.

        :param path: Path to Json file
        :param data: Dictionary of key-value pairs to update in the json file
        :return: Updated dictionary
        """
        # Read data
        try:
            with open(path, "r") as f:
                read_data = json.load(f)
        except FileNotFoundError:
            print(f"Json.update: Unable to find Json file on path:\n    {path}")
            return
        # Update
        read_data.update(data)
        # Save, at this point we know the path exists
        with open(path, "w") as f:
            json.dump(read_data, f, indent=4)
        return read_data

    @staticmethod
    def save(path: str, data: dict) -> None:
        """
        Method saves data into the path file.

        :param path: Path to Json file to save to
        :param data: Dictionary to save in the json file
        """
        # Check if path contains .json
        if not (".json" in path):
            path += ".json"
        # Write data
        try:
            with open(path, "w") as f:
                json.dump(data, f, indent=4)
        except FileNotFoundError:
            print(f"Json.save: Unable to find Json file on path:\n    {path}")
            return
