"""
Module containing various helper functions that don't belong in specific files.
Functions and or objects should be written in pure Python.
"""

from typing import Callable


def create_callable(func: Callable, *args, **kwargs) -> Callable:
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


def check_function_arguments(func: Callable, *args) -> Callable:
    """
    Function checks that the passed function func accepts arguments passed through args.
    :param func: Callable function to perform check on.
    :param args: Arguments passed to check presence in passed function.
    :return: Passed function check passed, otherwise error gets raised.
    """
    var_names = func.__code__.co_varnames
    for i, arg in enumerate(args):
        if var_names[i] != arg:
            error_msg = f"check_function_arguments: Function {func} " \
                        f"does not have the argument {arg} in the right position."
            raise ValueError(error_msg)
    return func


def create_object_repr(instance) -> str:
    """
    Function creates an object representation string by reading its class name and all attributes.
    Formatted: ClassName(attr1=val1, attr2=val2, ... , attrN=valN)
    :param instance: Object instance
    :return: str representation of object
    """
    # Get class name
    class_name = instance.__class__.__name__
    # Get attributes and its values, format into string "attr=value, attr=value, ... "
    attr_str = ", ".join([f"{attribute}={value}" for attribute, value in instance.__dict__.items()])
    return f"{class_name}({attr_str})"
