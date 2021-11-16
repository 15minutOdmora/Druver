"""
Module containing loading classes for threaded loading of assets.
"""

from typing import Callable
from queue import Queue
from threading import Thread

from game.helpers.helpers import check_function_arguments


class Loading:
    """
    Class for multi-threaded loading, used for asset loading.
    Consumer (usually pages) has to be added at initialization, producers, which produce data from one thread
    can be added later.
    """
    # https://riptutorial.com/python/example/4691/communicating-between-threads
    def __init__(self, consumer: Callable, **kwargs):
        """
        :param consumer: Callable function that will accept data from other threads
        :param kwargs: Kwargs can either accept producer=Callable or producers=iter[Callable] to add to producers list
        """
        self.consumer: Callable = check_function(consumer, "queue")
        self.producers = []  # List of callable
        # Go through kwargs
        if "producer" in kwargs:
            self.add_producer(kwargs["producer"])
        elif "producers" in kwargs:
            for producer in kwargs["producers"]:
                self.add_producer(producer)

    def add_producer(self, producer: Callable) -> None:
        """
        Method adds producer function to self as callable, all producers must accept a queue parameter for sending
        data between threads.
        :param producer: Callable function with argument queue
        """
        # Check that producer accepts queue argument
        self.producers.append(check_function(producer, "queue"))

    def producer(self, queue: Queue) -> None:
        """
        Method calls all producer functions passing the threading queue.
        :param queue: Queue for passing data between threads.
        """
        for producer in self.producers:
            producer(queue)  # Call function

    def load(self) -> None:
        """
        Method execute both the consumer and producer threads, passing one Queue object to both.
        """
        queue = Queue()
        consumer_thread = Thread(target=self.consumer, args=(queue,))
        producer_thread = Thread(target=self.producer, args=(queue,))
        consumer_thread.start()
        producer_thread.start()
        return
