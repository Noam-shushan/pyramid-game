"""
This module contains the PyramidGame class. and the main execution code of the game.
implement the game flow with pygame.

:author: Noam Shushan
"""

import pygame
from pygame.locals import *

from pyramid_game_rules import *

# colors
colors = {
    'pink': (255, 200, 200),
    'blue': (0, 210, 255),
    'yellow': (252, 254, 145),
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'red': (255, 0, 0)
}

# constants
size = width, height = (900, 500)  # define the size of the screen
border_size = 5  # define the border size
font_size = 20  # define the font size
gap = 2  # define the gap between cells
time_to_wait_before_after_round = 3000  # define the time to wait between the user click and the computer move


class PyramidGame:
    """
    Pyramid Game running flow
    """

    def __init__(self):
        """
        Initialize the game and set the screen
        """
        self.pyramid = Pyramid()
        self.pyramid.create()

        # initialize the screen
        pygame.init()
        self.screen = pygame.display.set_mode(size)
        # set the background color to white
        self.screen.fill(colors['white'])
        # set the title of the screen
        pygame.display.set_caption("Pyramid Game")

        # draw the border of the pyramid
        pygame.draw.rect(self.screen,
                         colors['black'],
                         (0, 0, width, height),
                         border_size)

        # define the size of each cell in the pyramid
        self.cell_size = (width - border_size) // self.pyramid.columns - 1.5 * gap

    def run(self):
        """
        Run the game.
        Every 3 seconds check if the pyramid is valid, if not, try to fix and draw the pyramid again
        """
        is_running = True  # define if the game is running

        # draw the pyramid at the first time
        self.draw_pyramid()
        pygame.display.update()

        time_elapsed_since_last_round = 0
        clock = pygame.time.Clock()
        while is_running:
            for event in pygame.event.get():
                if event.type == QUIT:  # if the user clicks on the close button
                    is_running = False  # stop the game

            if not self.pyramid.is_valid():  # check if the pyramid is valid
                dt = clock.tick()
                time_elapsed_since_last_round += dt
                # every 3 seconds we will try to fix the pyramid
                if time_elapsed_since_last_round > time_to_wait_before_after_round:
                    self.pyramid.fix_invalid_cells()  # fix the invalid cells
                    self.draw_pyramid()  # draw the pyramid again

                    pygame.display.update()  # update the screen
                    time_elapsed_since_last_round = 0  # reset the time
        pygame.quit()

    def draw_pyramid(self):
        """
        draw the pyramid on the screen
        validate the pyramid
        """
        self.pyramid.validate()  # validate the pyramid

        for row in self.pyramid.pyramid:
            for cell in row:
                r, c = cell.position
                x = (c - 1) * (self.cell_size + gap) + border_size + gap
                y = (r - 1) * (self.cell_size + gap) + border_size + gap
                pygame.draw.rect(self.screen,
                                 colors[cell.color],
                                 (x + 1.5 * gap, y, self.cell_size, self.cell_size))

                # draw a black border around the the edges of the pyramid
                self.draw_pyramid_border_line(cell, row, x, y)

                # mark the invalid cells with red cross
                if cell.is_violate:
                    self.mark_invalid_cells(x, y)

    def draw_pyramid_border_line(self, cell, row, x, y):
        """
        draw a black border around the the edges of the pyramid
        :param cell: the current cell to draw around
        :param row: the current row of the cell
        :param x: horizontal position in the screen
        :param y: vertical position in the screen
        """
        if cell == row[0] and cell == row[-1]:
            self.draw_line((x, y), (x, y + self.cell_size))
            self.draw_line((x, y + self.cell_size), (x - self.cell_size - 2 * gap, y + self.cell_size))
            self.draw_line((x + self.cell_size, y), (x + self.cell_size, y + self.cell_size))
            self.draw_line((x + self.cell_size, y + self.cell_size),
                           (x + 2 * self.cell_size + 2 * gap, y + self.cell_size))
        elif cell == row[0]:
            self.draw_line((x, y), (x, y + self.cell_size))
            self.draw_line((x, y + self.cell_size), (x - self.cell_size - 2 * gap, y + self.cell_size))
        elif cell == row[-1]:
            self.draw_line((x + self.cell_size, y), (x + self.cell_size, y + self.cell_size))
            self.draw_line((x + self.cell_size, y + self.cell_size),
                           (x + 2 * self.cell_size + 2 * gap, y + self.cell_size))

    def mark_invalid_cells(self, x, y):
        """
        mark invalid cells with a red cross
        :param x: horizontal position in the screen
        :param y: vertical position in the screen
        """
        # define the font and the text for invalid cells in the pyramid
        font = pygame.font.Font('freesansbold.ttf', font_size)
        text = font.render('X', True, colors['red'])
        cell_center = (self.cell_size // 2) - (font_size // 2)
        text_position = (x + cell_center, y + cell_center)
        self.screen.blit(text, text_position)

    def draw_line(self, start, end):
        """
        draw a horizontal line in the given position
        :param start: stating point of the line
        :param end: ending point of the line
        """
        pygame.draw.line(self.screen, colors['black'], start, end, border_size)


if __name__ == '__main__':
    game = PyramidGame()
    game.run()
