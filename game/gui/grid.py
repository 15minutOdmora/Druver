"""
Module contains the grid class.
"""

import pygame

from game.gui.item import StaticItem
from game.constants import SCREEN_SIZE
from game.constants import BaseColors


class Cell(StaticItem):
    """
    Class Cell defines a single cell inside the Grid object.
    Items can be added to each cell and aligned against its borders.
    """
    def __init__(self, position, size, align="left top", item=None, padding=None):
        """
        Args:
            position (tuple[int]): Position of cell
            size (tuple[int]): Size of cell
            align (str): Alignment string where each alignment is separated by space
            padding (str): Padding string where each padding is separated with ','
            and a value is passed ex.: 'top 0, left 0'
            item (Item): Item inside cell
        """
        super().__init__(position, size)

        self.item = item  # TODO: Update to items

        self._align = ["top", "left"]  # Initial alignment if it doesn't get set
        self.align = align
        # Possible alignments
        self.alignments = {
            "left": self._left,
            "right": self._right,
            "top": self._top,
            "bottom": self._bottom,
            "centre": self._centre,
            None: self._centre
        }
        # Possible paddings
        self._padding = {
            "top": 0,
            "bottom": 0,
            "left": 0,
            "right": 0
        }
        self.padding = padding  # Sets self._padding in the setter

        self._align_items()

    @property
    def align(self):
        return self._align

    @align.setter
    def align(self, alignment):
        if alignment is not None:
            self._align = alignment.split(" ")

    @property
    def padding(self):
        return self._padding

    @padding.setter
    def padding(self, padding):
        if padding is not None:
            pad = padding.split(", ")  # ['top 5', 'left 8']
            for p in pad:
                line = p.split(" ")  # ['top', '5']
                key, value = line[0], line[1]
                if key in self._padding.keys():
                    try:  # Try converting to intiger
                        self._padding[key] += int(value)
                    except ValueError:
                        print(f"Padding value incorrect: {value}")
                else:
                    print(f"Padding {key} is not yet implemented :(")

    def _align_items(self) -> None:
        """
        Method aligns all items attached to itself based on the defined alignment.
        """
        # Do alignments
        if self.item is not None:
            for alignment in self.align:
                if alignment in self.alignments.keys():  # Only do if alignment exists
                    self.alignments[alignment]()  # Call alignment function
                else:  # Print error
                    print(f"Cell: Alignment type {alignment} does not exist.")
            # Apply padding
            padding_value_multipliers = {"top": 1, "bottom": -1, "left": 1, "right": -1}
            for pad_type, value in self._padding.items():
                if pad_type in ["left", "right"]:
                    x_pos = self.item.position[0] + padding_value_multipliers[pad_type] * value
                else:
                    x_pos = self.item.position[0]
                if pad_type in ["top", "bottom"]:
                    y_pos = self.item.position[1] + padding_value_multipliers[pad_type] * value
                else:
                    y_pos = self.item.position[1]
                self.item.position = (x_pos, y_pos)

    def _left(self) -> None:
        """
        Method aligns item to the left side of cell.
        """
        self.item.position = (self.position[0], self.item.position[1])

    def _right(self) -> None:
        """
        Method aligns item to the right side of cell.
        """
        # Set right cell border to match item right side
        diff = (self.width - self.item.width) if self.width > self.item.width else 0
        # Set new x position
        self.item.position = (self.position[0] + diff, self.item.position[1])

    def _top(self) -> None:
        """
        Method aligns item to the top side of cell.
        """
        # Set top borders to match
        self.item.position = (self.item.position[0], self.position[1])

    def _bottom(self) -> None:
        """
        Method aligns item to the bottom side of cell.
        """
        # Set bottom cell border to match item bottom
        diff = (self.height - self.item.height) if self.height > self.item.height else 0
        self.item.position = (self.item.position[0], self.position[1] + diff)

    def _centre(self) -> None:
        """
        Method aligns item so its centre mathces the cells centre.
        """
        # Item centre is at cell centre
        centered_x = self.position[0] + ((self.width - self.item.width) // 2)
        centered_y = self.position[1] + ((self.height - self.item.height) // 2)
        self.item.position = (centered_x, centered_y)

    def update(self) -> None:
        """
        Method updates all items inside cell by aligning them to the set alignments.
        """
        self._align_items()

    def draw(self):
        """
        Method draws cell onto screen.
        """
        pass

    def __str__(self):
        """
        String representation of cell.
        """
        out = f"Cell:\n    {self.position=}\n    {self.size=}\n    {self.align=}"
        return out


class Row:
    """
    Class defines a single row on the grid.
    Has height property wich can get changed either by procentage to screen size or an actual size in px.
    """
    def __init__(self, grid, position: int, height: int, visible: bool = False):
        self.grid: "Grid" = grid
        self.position: tuple[int] = position
        self.visible: bool = visible
        self._height: int = height

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, new_height):
        # New height can be int as px size, or float < 1 as percentage of grid size
        if type(new_height) is int:
            self._height = new_height
        elif type(new_height) is float:
            grid_height = self.grid.size[1]
            self._height = int(grid_height * new_height)
        self.grid.update()


class Col:
    """
    Class defines a single column on the grid.
    Has width property wich can get changed either by procentage to screen size or an actual size in px.
    """
    def __init__(self, grid, position: int, width: int, visible: bool = False):
        self.grid: "Grid" = grid
        self.position: tuple[int] = position
        self.visible: bool = visible
        self._width: int = width

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, new_width):
        # New width can be int as px size, or float < 1 as percentage of grid size
        if type(new_width) is int:
            self._width = new_width
        elif type(new_width) is float:
            grid_width = self.grid.size[0]
            self._width = int(grid_width * new_width)
        self.grid.update()


class Grid(StaticItem):
    """
    Grid class defines a mesh consisted of rows and columns, where each 'rectangle'(intersection of rows and columns)
    is defined as a cell that can have items on it.
    Number of rows and columns are defined with initialization of class and cannot be changed.
    Column width and Row height can be later modified by changing the row/col property of object.
    Col/Row size can be passed either as an int or as a float, if float gets passed it acts as a percentage size of the grid.
    Items get added to the grid by the add_item() method.
    """
    def __init__(self,
                 rows: int = 1,
                 columns: int = 1,
                 position: tuple[int] = (0, 0),
                 size: tuple[int] = SCREEN_SIZE):
        """
        Args:
            rows (int): Number of rows, Default = 1
            columns (int): Number of columns, Default = 1
            visible (bool): If grid should be visible, used for testing, Default = False
            position (tuple[int]): Position of screen, Default = (0, 0)
            size (tuple[int]): Size of grid in px, Default = SCREEN_SIZE
        """
        super().__init__(position, size)
        self.visible = False
        # Rows and columns can be passed as lists of sizes, although not recomended
        self.num_rows: int = rows if (type(rows) is int) else len(rows)
        self.num_columns: int = columns if (type(columns) is int) else len(columns)
        self.row: list[int] = []
        self.col: list[int] = []
        self._grid: list[list[Cell]] = [[None for j in range(self.num_columns)] for i in
                                        range(self.num_rows)]  # Contains all cells
        self.__init_grid()

    def __init_grid(self):
        """
        Method constructs grid rows and columns while also creating cells.
        """
        # TODO: Optimize
        row_height = self.size[1] // self.num_rows
        column_width = self.size[0] // self.num_columns
        for i in range(self.num_rows):
            row_pos = (0, i * row_height)
            self.row.append(
                Row(
                    grid=self,
                    position=row_pos,
                    height=row_height,
                    visible=self.visible
                )
            )
        for j in range(self.num_columns):
            col_pos = (j * column_width, 0)
            self.col.append(
                Col(
                    grid=self,
                    position=col_pos,
                    width=column_width,
                    visible=self.visible
                )
            )
        for i in range(len(self.row)):
            for j in range(len(self.col)):
                cell_position = (self.col[j].position[0], self.row[i].position[1])
                cell_size = (self.col[j].width, self.row[i].height)
                # Get that cell, and update its properties
                cell = Cell(
                    position=cell_position,
                    size=cell_size
                )
                self._grid[i][j] = cell
        # Create cell at positions of rows and columns
        self.update_cells()

    def update_cells(self) -> None:
        """
        Method updates every cells items position.
        """
        for i in range(len(self.row)):
            for j in range(len(self.col)):
                cell_position = (self.col[j].position[0], self.row[i].position[1])
                cell_size = (self.col[j].width, self.row[i].height)
                # Get that cell, and update its properties
                cell = self._grid[i][j]
                cell.position = cell_position
                cell.size = cell_size

    def add_item(self, row: int, col: int, item, align: str = None, padding: str = None) -> None:
        """
        Method adds item to grid on i-th row and j-th column, with the defined alignment align.

        Args:
            row (int): Index of row to be added on
            col (int): Index of col to be added on
            item (Item): Item to be added to cell
            align (str): Alignment string where alignemnts are separated by space
                Alignments: top, bottom, right, left, centre
        """
        self._grid[row][col].item = item
        self._grid[row][col].align = align
        self._grid[row][col].padding = padding
        self._grid[row][col].update()  # Update that cell
        self._grid[row][col].item.update()
        self.items.append(item)
        self.update_cells()

    def change_item(self, row: int, col: int, new_item) -> None:
        """
        Method changes the item on specified row-column.

        Args:
            row (int): Index of row to be added on
            col (int): Index of col to be added on
            new_item (Item): Item to be added to cell
        """
        self._grid[row][col].item = new_item
        # Update in items list, this might be error prone idk did not test
        index = self.items.index(self._grid[row][col].item)
        self.items[index] = new_item
        self.update_cells()

    def update(self) -> None:
        """
        Method updates all items attached to self.
        """
        # Update every item
        for item in self.items:
            item.update()

    def draw(self) -> None:
        """
        Method draws every item attached to a cell in the grid.
        """
        # Draw each row and column
        for i in range(self.num_rows):
            for j in range(self.num_columns):
                if self._grid[i][j].item is not None:
                    #       cell     item
                    self._grid[i][j].item.draw()

        if self.visible:  # Draw the grid, development purpose
            for row in self.row:
                row_rect = (row.position[0], row.position[1], self.width, row.height)
                pygame.draw.rect(
                    self.screen,
                    BaseColors.items,
                    pygame.Rect(row_rect),
                    width=1
                )
            for col in self.col:
                col_rect = (col.position[0], col.position[1], col.width, self.height)
                pygame.draw.rect(
                    self.screen,
                    BaseColors.items,
                    pygame.Rect(col_rect),
                    width=1
                )
