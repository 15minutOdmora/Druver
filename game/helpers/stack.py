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
            raise ValueError("Stack.take: The stack is empty.")
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


class Pointer:
    """
    Pointer used to store data that points on specific data. Pointer can point to anything.
    """
    def __init__(self, to: any):
        """
        :param to: any object the instance will point to
        """
        self.to = to

    def __str__(self) -> str:
        """
        String representation of stack object
        """
        return f"<Pointer: to -> {self.to}>"


class UniqueStack(Stack):
    """
    UniqueStack extends Stack by adding pointer elements for eliminating duplicate element types inside stack.
    Every element inside stack is either unique (in type of object) or is a pointer pointing to an already existent
    object instance of the same type.
    No initial data can be added to Unique stack.
    """
    def __init__(self):
        super().__init__()
        # For saving already added object types and their positions inside the self._data
        self._element_types = {}  # Dictionary type(object): index in self._data

    @property
    def cache(self):
        return self._element_types.keys()

    def push(self, element):
        """
        Method adds element to stack, if element type already inside self -> adds a pointer object pointing to it.
        :param element: any element to add to stack
        """
        if type(element) in self._element_types.keys():  # If element already inside stack, remove from position
            at_index = self._element_types[type(element)]  # Get index of this type
            super(UniqueStack, self).push(Pointer(at_index))  # Add pointer to that index
        else:
            self._element_types[type(element)] = len(self._data)  # Save type and its index in list
            super(UniqueStack, self).push(element)

    def peak(self) -> any:
        """
        Method returns the top element of the stack. Does not change the stack.
        :return: element
        """
        if self.empty():
            raise ValueError("UniqueStack.peak: The stack is empty.")
        if isinstance(self._data[-1], Pointer):
            pointer = self._data[-1]
            return self._data[pointer.to]
        return self._data[-1]

    def take(self) -> any:
        """
        Method returns the top element from the stack while also removing it.
        :return:
        """
        if self.empty():
            raise ValueError("UniqueStack.take: The stack is empty.")
        element = self._data[-1]
        self._data.pop()
        self._counter -= 1
        if isinstance(element, Pointer):
            return self._data[element.to]
        else:
            del self._element_types[type(element)]
            return element

    def back_to(self, to_class: any) -> None:
        """
        Method removes elements from stack until it encounters an element of the same type as to_class.
        :param to_class: any class
        """
        print(self._element_types.keys(), to_class)
        if to_class in self._element_types.keys():
            while len(self._data) > 1:
                if self.peak() == to_class:
                    self.pop()
                    return
                else:
                    if self.take() not in self._element_types.keys():
                        pass
                    else:
                        del self._element_types[type(self.take())]
        else:
            raise ValueError(f"UniqueStack.back_to: Backing to {to_class} type {to_class} would empty stack.")
