from pygame import Surface, Rect
from pygame import draw
from math import pi, atan, cos, sin
from tools.draw.draw_figure import DrawFigure


class _Circle:
    def __init__(self, center_x: float = 0, center_y: float = 0, rayon: float = 0, color: tuple = (255, 0, 0)):
        self.center_x = center_x
        self.center_y = center_y
        self.rayon = rayon
        self.color = color


class _Line:
    def __init__(self, surface: Surface, start: tuple = (0, 0), end: tuple = (0, 0), color: tuple = (0, 0, 255),
                 ep: int = 1):
        self.surface = surface
        self.start = start
        self.end = end
        self.color = color
        self.ep = ep
        self.a = 0
        self.b = 0
        self.angle = 0

    def draw(self):
        draw.line(self.surface, self.color, (self.start[0], self.start[1]), (self.end[0], self.end[1]), self.ep)

    def formula(self):
        self.a, self.b = _define_formula_droite_2_points(self.start, self.end)


class _Point:
    def __init__(self, surface: Surface, center: tuple = (0, 0), rayon: int = 5, color: tuple = (0, 0, 255)):
        self.surface = surface
        self.center = center
        self.color = color
        self.rayon = rayon

    def draw(self):
        draw.circle(surface=self.surface, color=self.color, center=self.center, radius=self.rayon)


class DrawArc(DrawFigure):
    def __init__(self, surface: Surface, x: float, y: float, marge: int = 8):
        super().__init__(surface=surface, x=x, y=y, marge=marge)
        self.angle_ini = pi / 2
        self.angle = self.angle_ini
        self.angle_start = 0
        self.angle_end = self.angle_start + self.angle

        self.origine_rect_mouse: tuple = (0, 0)
        self.rect_mouse: Rect = Rect(self.origine_rect_mouse[0], self.origine_rect_mouse[1], 0, 0)
        self.width_rect_m = 0
        self.height_rect_m = 0

        self.origine_rect_draw: tuple = (0, 0)
        self.rect_draw = self.rect_mouse
        self.width_rect_d = 0
        self.height_rect_d = 0

        self.cadre = 0

        self.circle_A = _Circle()
        self.circle_B = _Circle(color=(0, 255, 0))

        self.line_cent_mou = _Line(surface=surface, ep=self._ep)

        self.reversed = False

        self.draw_construction = False
        self.draw_rect_create = False

        self.interesect_A: _Point = _Point(surface=surface, color=(255, 0, 0))
        self.interesect_B: _Point = _Point(surface=surface, color=(0, 255, 0))
        self.interesect_C: _Point = _Point(surface=surface, color=(150, 150, 150))
        self.projete_C: _Point = _Point(surface=surface, color=(180, 180, 180))
        self.interesect_E: _Point = _Point(surface=surface, color=(255, 0, 0))
        self.interesect_F: _Point = _Point(surface=surface, color=(0, 255, 0))
        self.interesect_G: _Point = _Point(surface=surface, color=(0, 0, 255))
        self.angle_mouse = 0

    def update_formula(self):
        self.define_rect_mouse()
        self.define_rect_draw()
        self.define_angles()
        self.define_circles()
        self.define_min_max()

    def get_pt2(self):
        return self.interesect_G.center

    def define_rect_mouse(self):
        self.origine_rect_mouse = self.points[0]
        self.cadre = 0
        if self.points[0][0] > self.points[1][0]:
            if self.points[0][1] > self.points[1][1]:
                self.origine_rect_mouse = self.points[1]
                self.cadre = 2
            else:
                self.origine_rect_mouse = self.points[1][0], self.points[0][1]
                self.cadre = 3
        else:
            if self.points[0][1] > self.points[1][1]:
                self.origine_rect_mouse = self.points[0][0], self.points[1][1]
                self.cadre = 1

        self.width_rect_m = abs(self.points[1][0] - self.points[0][0])
        self.height_rect_m = abs(self.points[1][1] - self.points[0][1])

        self.rect_mouse = Rect(self.origine_rect_mouse[0], self.origine_rect_mouse[1],
                               self.width_rect_m, self.height_rect_m)

    def define_rect_draw(self):
        self.width_rect_d = self.width_rect_m * 2
        self.height_rect_d = self.height_rect_m * 2

        if not self.reversed:
            if (self.cadre == 0) | (self.cadre == 2):
                self.origine_rect_draw = self.origine_rect_mouse[0] - self.width_rect_m, self.origine_rect_mouse[1]
            elif (self.cadre == 1) | (self.cadre == 3):
                self.origine_rect_draw = self.origine_rect_mouse
        else:
            if (self.cadre == 0) | (self.cadre == 2):
                self.origine_rect_draw = self.origine_rect_mouse[0], self.origine_rect_mouse[1]-self.height_rect_m
            elif (self.cadre == 1) | (self.cadre == 3):
                self.origine_rect_draw = self.origine_rect_mouse[0] - self.width_rect_m, \
                                         self.origine_rect_mouse[1] - self.height_rect_m

        self.rect_draw = Rect(self.origine_rect_draw[0], self.origine_rect_draw[1],
                              self.width_rect_d, self.height_rect_d)

    def define_angles(self):
        if (self.cadre == 0) | (self.cadre == 2):
            self.angle_start = 0
        elif (self.cadre == 1) | (self.cadre == 3):
            self.angle_start = pi / 2

        if self.reversed:
            self.angle_start += pi

        self.angle_end = self.angle_start + self.angle

    def draw_rect(self):
        draw.rect(self.surface, (0, 0, 0), self.rect_mouse, self._ep)
        draw.rect(self.surface, (255, 0, 0), self.rect_draw, self._ep)

    def define_circles(self):
        self.circle_A.center_x = self.origine_rect_draw[0] + self.width_rect_d / 2
        self.circle_A.center_y = self.origine_rect_draw[1] + self.height_rect_d / 2
        self.circle_A.rayon = self.width_rect_d / 2

        self.circle_B.center_x = self.circle_A.center_x
        self.circle_B.center_y = self.circle_A.center_y
        self.circle_B.rayon = self.height_rect_d / 2

    def draw_circles(self):
        draw.circle(self.surface, self.circle_A.color,
                    (self.circle_A.center_x, self.circle_A.center_y), self.circle_A.rayon, self._ep)
        draw.circle(self.surface, self.circle_B.color,
                    (self.circle_B.center_x, self.circle_B.center_y), self.circle_B.rayon, self._ep)

    def define_lines(self):
        self.line_cent_mou.start = self.circle_A.center_x, self.circle_A.center_y
        self.line_cent_mou.end = self.mouse_pos

    def draw_lines(self):
        self.line_cent_mou.draw()

    def define_intersect(self):
        self.angle_mouse = _angle_droite((self.circle_A.center_x, self.circle_A.center_y), self.mouse_pos)
        r = self.interesect_A.rayon / 2
        self.interesect_A.center = ((self.circle_A.rayon - r) * cos(self.angle_mouse) + self.circle_A.center_x,
                                    (self.circle_A.rayon - r) * sin(self.angle_mouse) + self.circle_A.center_y)

        self.interesect_B.center = ((self.circle_B.rayon - r) * cos(self.angle_mouse) + self.circle_B.center_x,
                                    (self.circle_B.rayon - r) * sin(self.angle_mouse) + self.circle_B.center_y)

        self.interesect_C.center = self.interesect_A.center[0], self.interesect_B.center[1]

        self.projete_C.center = self.interesect_B.center[0], self.interesect_A.center[1]

        angle_nv_droite = _angle_droite((self.circle_A.center_x, self.circle_A.center_y), self.projete_C.center)

        self.interesect_E.center = (self.circle_A.rayon * cos(angle_nv_droite) + self.circle_A.center_x,
                                    self.circle_A.rayon * sin(angle_nv_droite) + self.circle_A.center_y)

        self.interesect_F.center = (self.circle_B.rayon * cos(angle_nv_droite) + self.circle_B.center_x,
                                    self.circle_B.rayon * sin(angle_nv_droite) + self.circle_B.center_y)

        self.interesect_G.center = (self.interesect_E.center[0], self.interesect_F.center[1])

    def draw_point(self):
        self.interesect_A.draw()
        self.interesect_B.draw()
        self.interesect_C.draw()
        self.projete_C.draw()
        self.interesect_E.draw()
        self.interesect_F.draw()
        self.interesect_G.draw()

    def draw(self):
        self.define_lines()
        self.define_intersect()

        draw.arc(self.surface, self.color, self.rect_draw, self.angle_start, self.angle_end, self._ep)

        if self.draw_rect_create:
            self.draw_rect()
        if self.draw_construction:
            self.draw_circles()
            self.draw_lines()
            self.draw_point()

    def define_min_max(self):
        self.min_x = self.rect_mouse.left
        self.max_x = self.rect_mouse.left + self.rect_mouse.width
        self.min_y = self.rect_mouse.top
        self.max_y = self.rect_mouse.top + self.rect_mouse.height

    def reverse_curve(self):
        if self.reversed:
            self.reversed = False
        else:
            self.reversed = True
        self.update_formula()


def _angle_droite(c, s):
    angle = 0

    if c[0] != s[0]:
        atan_angle = abs(s[1] - c[1]) / (s[0] - c[0])
        angle = atan(atan_angle)

        if s[0] < c[0]:
            if s[1] < c[1]:
                angle += pi
            else:
                angle = pi - angle
        else:
            if s[1] > c[1]:
                angle = 2 * pi - angle

    return 2 * pi - angle


def _define_formula_droite_2_points(pt_a, pt_b):
    a = 0
    if pt_a[0] != pt_b[0]:
        a = (pt_a[1] - pt_b[1]) / (pt_a[0] - pt_b[0])

    b = pt_a[1] - a * pt_a[0]

    return a, b
