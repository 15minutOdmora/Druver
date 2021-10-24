"""
Module containing various helper functions that don't belong in specific files.
Functions and or objects should be written in pure Python.
"""

from typing import Callable


def create_callable(func: Callable, *args, **kwargs):
    """
    Function creates a callable function where the called function gets passed as an argument along with its
    args and kwargs.

    :param func: Function to be called
    :param args: Args passed to passed function
    :param kwargs: Kwargs passed to passed function
    :return: Callable: Function that executes passed function when called.
    """
    def callable_func():
        return func(*args, **kwargs)
    return callable_func
