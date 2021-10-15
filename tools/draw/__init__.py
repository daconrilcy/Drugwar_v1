import pygame
from tools.draw.dashed_line import DashedLine
from math import dist


class DrawFigure:
    def __init__(self, surface: pygame.Surface, x: float, y: float, color_base: tuple = (180, 180, 180),
                 ep_base: int = 4, ep_survol: int = 8, marge: int = 10, rayon_pts: int = 2):
        self.surface = surface
        self.color_ini = color_base
        self.color = (0, 255, 0)
        self.form = None
        self.statut = "created"
        self._ep = ep_base
        self._ep_overed = ep_survol
        self.overed = False
        self.mouse_pos = 0, 0
        self.marge = marge
        self.points = [(x, y), (x, y)]
        self.pt_survol = -1
        self.rayon_pts = rayon_pts

    def create(self, *args):
        pass

    def modif(self, pt: tuple):
        pass

    def modif_point_to(self, pt: int, coord: tuple):
        pass

    def update(self):
        self.draw()
        pass

    def draw(self):
        pass

    def is_overed(self, *args):
        pass


class DrawPoint:
    def __init__(self, x, y, r=10, surface: pygame.Surface = None, color: pygame.Color = pygame.Color(255, 0, 0)):
        self.surface = surface
        self.center = (x, y)
        self.rayon = r
        self.color = color
        self.active = True
        self.form = None

    def update(self):
        self.form = pygame.draw.circle(surface=self.surface,
                                       center=(self.center[0], self.center[1]), radius=self.rayon,
                                       color=self.color)


class DrawLine(DrawFigure):

    def __init__(self, surface: pygame.Surface, x: float, y: float, marge: int = 10):
        super().__init__(surface=surface, x=x, y=y, marge=marge)
        self.a = 0
        self.b = 0

    def modif(self, npt: int):
        self.points[npt] = self.mouse_pos
        self.statut = "modified"

    def modif_point_to(self, npt: int, coord: tuple):
        self.points[npt] = coord
        self.statut = "modified"

    def update(self):

        self.udpdate_formula()
        self.is_overed()
        self.is_overed_point()
        self.draw()

    def draw(self):
        ep = self._ep
        if self.overed:
            ep = self._ep_overed
        pygame.draw.line(self.surface, self.color,
                         (self.points[0][0], self.points[0][1]), (self.points[1][0], self.points[1][1]), ep)

        for n in range(len(self.points)):
            pt = self.points[n]
            r = self.rayon_pts
            if n == self.pt_survol:
                r = self._ep_overed
            pygame.draw.circle(self.surface, self.color, [pt[0], pt[1]], r)

    def udpdate_formula(self):
        if self.points[0][0] != self.points[1][0]:
            self.a = (self.points[0][1] - self.points[1][1]) / (self.points[0][0] - self.points[1][0])
        else:
            self.a = 0
        self.b = self.points[0][1] - self.a * self.points[0][0]
        self.statut = "ok"

    def get_y(self, x: float):
        return self.a * x + self.b

    def is_overed(self):
        y2 = self.get_y(self.mouse_pos[0])
        if (y2 >= self.mouse_pos[1] - self.marge) & (y2 <= self.mouse_pos[1] + self.marge):
            self.overed = True
        else:
            self.overed = False

    def is_overed_point(self):
        self.pt_survol = -1
        for n in range(len(self.points)):
            pt = self.points[n]
            d = dist(self.mouse_pos, pt)
            if d <= self.marge:
                self.pt_survol = n
                self.overed = True
                break

