import pygame
from math import pi as PI

class PtLine:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def get_tuple(self):
        return self.x, self.y

    def set(self, x:float, y:float):
        self.x = x
        self.y = y

    def is_merged_to(self, pt, marge: float = 0):
        if (pt.x >= self.x - marge) & (pt.x <= self.x + marge):
            if (pt.y >= self.y - marge) & (pt.y <= self.y + marge):
                return True

        return False

    def parse(self):
        return str(self.x) + ", " + str(self.y)


class DrawFigure:
    def __init__(self, surface: pygame.Surface, x: float, y: float):
        self.surface = surface
        self.origine = PtLine(x, y)
        self.end = PtLine(x, y)
        self.color = (0, 255, 0)
        self.form = None
        self.statut = "created"
        self.a = 0
        self.b = 0
        self._ep = 4

        self.update()

    def update(self):
        pass

    def change_end(self, pt: PtLine):
        if pt is not None:
            self.end = pt
            self.udpdate_formula()

    def udpdate_formula(self):
        pass

    def get_y(self, x: float):
        pass

    def pt_is_inline(self, pt: PtLine, marge=0):
        pass


class DrawLine(DrawFigure):

    def update(self):
        self.form = pygame.draw.line(self.surface, self.color,
                                     (self.origine.x, self.origine.y), (self.end.x, self.end.y), self._ep)

    def udpdate_formula(self):
        if self.origine.x != self.end.x:
            self.a = (self.origine.y-self.end.y) / (self.origine.x - self.end.x)
        else:
            self.a = 0
        self.b = self.origine.y - self.a * self.origine.x

    def get_y(self, x: float):
        return self.a * x + self.b

    def pt_is_inline(self, pt: PtLine, marge=0):
        print(pt.x)
        y2 = self.get_y(pt.x)
        if (y2 >= pt.y - marge) & (y2 <= pt.y + marge):
            return True
        else:
            return False


class DrawCurve(DrawFigure):
    start_angle = 0
    stop_angle = PI/2

    def update(self):
        self.form = pygame.draw.arc(self.surface, self.color,
                                    pygame.Rect(self.origine.x, self.origine.y, self.end.x, self.end.y),
                                    self.start_angle, self.stop_angle, self._ep)

    def udpdate_formula(self):
        if self.origine.x != self.end.x:
            self.a = (self.origine.y - self.end.y) / (self.origine.x - self.end.x)
        else:
            self.a = 0
        self.b = self.origine.y - self.a * self.origine.x

    def get_y(self, x: float):
        return self.a * x + self.b

    def pt_is_inline(self, pt: PtLine, marge=0):
        x_min = self.origine.x
        x_max = self.end.x
        y_min = self.origine.y
        y_max = self.end.y

        if self.origine.x > self.end.x:
            x_min = self.end.x
            x_max = self.origine.x
        if self.origine.y > self.end.y:
            y_min = self.end.y
            y_max = self.origine.y

        if (pt.x < x_min - marge) | (pt.x > x_max + marge) | (pt.y < y_min - marge) | (pt.y > y_max + marge):
            return False
        angle = PI - abs(pt.y/pt.x)


class DrawPoint:
    def __init__(self, x, y, r=10, surface: pygame.Surface = None, color: pygame.Color = pygame.Color(255, 0, 0)):
        self.surface = surface
        self.center = PtLine(x,y)
        self.rayon = r
        self.color = color
        self.active = True
        self.form = None

    def update(self):
        self.form = pygame.draw.circle(surface=self.surface,
                                       center=(self.center.x, self.center.y), radius=self.rayon,
                                       color=self.color)
