import pygame


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


class DrawLine:
    def __init__(self, surface: pygame.Surface, x, y):
        self.surface = surface
        self.origine = PtLine(x, y)
        self.end = PtLine(x, y)
        self.color = (0, 255, 0)
        self.line = None
        self.statut = "created"
        self.a = 0
        self.b = 0
        self._ep = 4

        self.update()

    def update(self):
        self.line = pygame.draw.line(self.surface, self.color,
                                     (self.origine.x, self.origine.y), (self.end.x, self.end.y), self._ep)

    def change_end(self, pt: PtLine):
        if pt is not None:
            self.end = pt
            self.udpdate_formula()

    def udpdate_formula(self):
        if self.origine.x != self.end.x:
            self.a =(self.origine.y-self.end.y) / (self.origine.x - self.end.x)
        else:
            self.a = 0
        self.b = self.origine.y - self.a * self.origine.x

    def get_y(self, x: float):
        print("self.origine : " + str(self.origine.parse()),)
        print("self.end : " + str(self.end.parse()))
        print("ax + b : " + str(self.a) + " x " + str(x) + " + " + str(self.b))
        return self.a * x + self.b

    def pt_is_inline(self, pt: PtLine, marge=0):
        print(pt.x)
        y2 = self.get_y(pt.x)
        print("y :" + str(pt.y))
        print("y2 :" + str(y2))
        if (y2 >= pt.y - marge) & (y2 <= pt.y + marge):
            return True
        else:
            return False


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
