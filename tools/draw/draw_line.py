import pygame
from tools.draw.draw_figure import DrawFigure


class DrawLine(DrawFigure):
    def __init__(self, surface: pygame.Surface, x: float, y: float, marge: int = 8, pas: int = 32):
        super().__init__(surface=surface, x=x, y=y, marge=marge, pas=pas)
        self.a = 0
        self.b = 0

    def draw(self):
        ep = self._ep
        color = self.color
        color_pt = self.color
        r = ep/2
        pt = self.points[0]
        if self.pt_selected > -1:
            color_pt = self.color_selected
            r = self._ep_selected
            pt = self.points[self.pt_selected]
        elif self.selected:
            color = self.color_selected
            ep = self._ep_selected
        elif self.pt_survol > -1:
            color_pt = self.color_overed
            r = self._ep_overed
            pt = self.points[self.pt_survol]
        if self.overed & (self.pt_survol == -1) & (not self.selected):
            ep = self._ep_overed
            color = self.color_overed
        if (self.pt_survol > -1) | (self.pt_selected > -1):
            pygame.draw.circle(surface=self.surface, color=color_pt,
                               center=(pt[0], pt[1]),
                               radius=r)

        pygame.draw.line(self.surface, color,
                         (self.points[0][0], self.points[0][1]), (self.points[1][0], self.points[1][1]), ep)

    def update_formula(self):
        if self.points[0][0] != self.points[1][0]:
            self.a = (self.points[0][1] - self.points[1][1]) / (self.points[0][0] - self.points[1][0])
        else:
            self.a = 0
        self.b = self.points[0][1] - self.a * self.points[0][0]
        self.define_min_max()

    def get_pt2(self):
        return self.mouse_pos[0], self.a * self.mouse_pos[0] + self.b
