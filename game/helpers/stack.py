"""
Stack class implementation of the data type.
"""


class Stack:
    def __init__(self, initial_data: iter = None):
        self._data = []
        self._counter = 0
        if initial_data:
            for elt in initial_data:
                self.push(elt)

    def empty(self) -> bool:
        """
        Function checks if stack is empty
        :return: True/False
        """
        return self._counter == 0

    def push(self, element) -> None:
        """
        Method adds element to the stack
        """
        self._data.append(element)
        self._counter += 1

    def pop(self) -> None:
        """
        Method removes the top element from the stack.
        :return: None
        """
        if self.empty():
            raise ValueError("pop: The stack is already empty.")
        self._data.pop()
        self._counter -= 1

    def peak(self) -> any:
        """
        Method returns the top element of the stack. Does not change the stack.
        :return: element
        """
        if self.empty():
            raise ValueError("peak: The stack is empty.")
        return self._data[-1]

    def take(self) -> any:
        """
        Method returns the top element from the stack while also removing it.
        :return:
        """
        if self.empty():
            raise ValueError("take: The stack is empty.")
        el = self._data[-1]
        self._data.pop()
        self._counter -= 1
        return el

    def __len__(self) -> int:
        """
        Length method for stack, returns number of elements.
        :return: int
        """
        return self._counter

    def __iter__(self) -> iter:
        """
        Iter method for stack, creates an iterable from items.
        :return: list
        """
        return iter(self._data)

    def __str__(self) -> str:
        """
        String representation of stack object
        :return:
        """
        bt = "Bottom"
        for elt in self._data:
            bt += " : " + str(elt)
        return bt + " : Top"