import numpy as np
import pygame


class DashedLine:
    # Code copié à partir du web :
    # https://codereview.stackexchange.com/questions/70143/drawing-a-dashed-line-with-pygame
    def __init__(self, surface: pygame.Surface, color=(255, 255, 255),
                 start_pos: tuple = (0, 0), end_pos: tuple = (0, 0),
                 width=1, dash_length=4, exclude_corners=True):
        self.surface = surface
        self.color = color

        self.start_pos = self._change_pos(start_pos)
        self.end_pos = self._change_pos(end_pos)

        self.length = 0
        self.width = width

        self.dash_length = dash_length
        self.dash_knots = []
        self.dash_amount: int = 0

        self.exclude_corners = exclude_corners

    def _change_pos(self, x: (float, tuple), y: float = None):
        # convert tuples to numpy arrays
        if isinstance(x, tuple):
            x = x[0]
            y = x[1]
        return np.array((x, y))

    def change_start_pos(self, x: (float, tuple), y: float = None):
        self.start_pos = self._change_pos(x, y)

    def change_end_pos(self, x: (float, tuple), y: float = None):
        self.end_pos = self._change_pos(x, y)

    def _calc_length(self):
        # get euclidian distance between start_pos and end_pos
        self.length = np.linalg.norm(self.end_pos, self.start_pos)

    def _calc_dash(self):
        # get amount of pieces that line will be split up in (half of it are amount of dashes)
        self.dash_amount = int(self.length / self.dash_length)

        # x-y-value-pairs of where dashes start (and on next, will end)
        self.dash_knots = np.array(
            [np.linspace(self.start_pos[i], self.end_pos[i], self.dash_amount) for i in range(2)]).transpose()

    def draw(self):
        [pygame.draw.line(self.surface, self.color, tuple(self.dash_knots[n]), tuple(self.dash_knots[n + 1]),
                          self.width)
         for n in range(int(self.exclude_corners), self.dash_amount - int(self.exclude_corners), 2)]

    def update(self):
        self._calc_length()
        self._calc_dash()
        self.draw()
