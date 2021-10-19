"""
Module for anything related to files
"""

from __future__ import annotations
import os
import time

import pygame


def abs_path(path: str) -> str:
    """
    Function gets the absolute path given certain path.
    :param path: Relative path
    :return: Absolute path
    """
    return os.path.abspath(path)


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
