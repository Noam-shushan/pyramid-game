"""
This module PyramidCell class and the Pyramid class.
Implementation of the game rules and the game logic.

:author: Noam Shushan
"""

from random import choice
from typing import Tuple, List


class PyramidCell:
    """
    Pyramid Cell
    contains the position and the color of the cell
    """

    def __init__(self, position: Tuple[int, int], color: str):
        self.position = position
        self.color = color
        self.is_violate = False  # define if the cell is violate the rules of the pyramid

    def __repr__(self):
        return f'PyramidCell({self.position}, {self.color})'

    def __str__(self):
        return f'color: {self.color}, position: {self.position}, is violate: {self.is_violate}'

    def __eq__(self, other):
        if not isinstance(other, PyramidCell) or other is None:
            return False
        return self.position == other.position


class Pyramid:
    """
    Pyramid class
    Implantation of the pyramid game rules and logic
    """
    rows = 5
    columns = 9
    colors = ['pink', 'blue', 'yellow']
    MAX_YELLOW_CELLS_IN_ROW = 4

    def __init__(self):
        self.pyramid: List[List[PyramidCell]] = []

    def create(self):
        """
        Create a pyramid with random colors
        the pyramid is a list of lists of PyramidCell
        the first list contains 1 element, the second list contains 2 elements
        until the last that contains 9 elements.
        each PyramidCell has a random position and a color
        """
        for row in range(self.rows):
            row_cells = []
            for cell in range((2 * row) + 1):
                color = choice(self.colors)
                position = (row + 1, self.rows - row + cell)
                row_cells.append(PyramidCell(position, color))
            self.pyramid.append(row_cells)

    def validate(self):
        """
        rules:
        1 - blue cell can not be in the border of the pyramid (left or right or top or bottom)
        2 - pink cell can not be adjacent to blue cell
        3 - row can not contain more than 4 cells of the yellow color
        """
        for row in self.pyramid:
            count_yellow = 0
            for cell in row:
                # rule 1:
                if cell.color == 'blue':
                    if cell == row[0] or cell == row[-1]:
                        cell.is_violate = True
                # rule 2:
                elif cell.color == 'pink':
                    for c in self.get_cells_around(cell):
                        if c.color == 'blue':
                            cell.is_violate = True
                            break  # no need to check the other cells around
                # rule 3:
                elif cell.color == 'yellow':
                    count_yellow += 1
                    if count_yellow > self.MAX_YELLOW_CELLS_IN_ROW:
                        for c in row:
                            c.is_violate = True
                        break  # no need to check the rest of the row

    def is_valid(self) -> bool:
        """
        check if the pyramid is valid
        :return: True if the pyramid is valid, False otherwise
        """
        for row in self.pyramid:
            for cell in row:
                if cell.is_violate:
                    return False
        return True

    def fix_invalid_cells(self):
        """
        Fix invalid cells, change the color of the cell to a random color
        """
        for row in self.pyramid:
            for cell in row:
                if cell.is_violate:
                    cell.color = choice(self.colors)
                    cell.is_violate = False

    def find_by_position(self, position: Tuple[int, int]) -> PyramidCell:
        """
        find a cell by position
        :param position: tuple of (row, column)
        :return: the PyramidCell that in the given position, None if not found
        """
        for row in self.pyramid:
            for cell in row:
                if cell.position == position:
                    return cell

    def get_cells_around(self, cell: PyramidCell) -> List[PyramidCell]:
        """
        get cells around a cell
        :param cell: PyramidCell
        :return: list of PyramidCell [top, bottom, left, right] if the cell as those neighbors
        """
        x, y = cell.position
        top = self.find_by_position((x - 1, y))
        bottom = self.find_by_position((x + 1, y))
        left = self.find_by_position((x, y - 1))
        right = self.find_by_position((x, y + 1))
        return [c for c in [top, bottom, left, right] if c is not None]
