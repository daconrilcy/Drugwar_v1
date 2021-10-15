import pygame.draw
from tools.draw import DrawFigure
from pygame import Surface, Rect, Color
from math import pi, cos, sin, sqrt, atan
from tools.draw.dashed_line import DashedLine


class Arc(DrawFigure):
    def __init__(self, surface: Surface, x, y, marge: int = 10):
        super().__init__(surface=surface, x=x, y=y, marge=marge)
        self.surface = surface
        self.points = [(x, y), (x, y)]
        self.center = x, y
        self.color = Color(0, 255, 0)
        self.width = 0
        self.new_width = 0
        self.new_height = 0
        self.height = 0
        self.new_rect = Rect(0, 0, 0, 0)
        self.angle_start = 0
        self.angle_end = pi / 2
        self.angle_mouse = 0
        self.orientation = 0
        self.first_mouse_pos = 0, 0

        self.is_active = False
        self.under_modif = False

        self.mouse_pos = x, y

        self.delai_affich_ini = 500
        self.delai_affich = self.delai_affich_ini
        self.marge = 10
        self.l_p = None
        self.center_to_mouse = 0
        self.point_mouse_projete = 0, 0

        self.affiche_projection = False
        self.affiche_donnee = False
        self.overed = False

    def reset(self):
        self.points[0] = 0, 0
        self.points[1] = 0, 0
        self.center = 0, 0
        self.width = 0
        self.new_width = 0
        self.new_height = 0
        self.height = 0
        self.new_rect = Rect(0, 0, 0, 0)
        self.is_active = False
        self.delai_affich = self.delai_affich_ini
        self.l_p = None
        self.affiche_projection = False

    def update(self):
        ep = self._ep
        self.check_orientation()
        if self.under_modif:
            self.draw_rect()

        if self.is_active:
            self.point_projete()
            self.is_overed()

        if self.overed:
            ep = self._ep_overed

        if self.is_active | self.under_modif:
            pygame.draw.arc(self.surface, self.color, self.new_rect,
                            self.angle_start, self.angle_end, ep)

        pygame.draw.line(self.surface, self.color, (self.points[0][0], self.points[0][1]),
                         (self.points[1][0], self.points[1][1]), ep)
        #pygame.draw.arc(self.surface, (255, 0, 0), self.new_rect, self.angle_start, self.angle_end, ep)

    def pos_end(self, x, y):
        self.points[1] = x, y
        self.width = abs(self.points[1][0] - self.points[0][0])
        self.height = abs(self.points[1][1] - self.points[0][1])

    def draw_rect(self):
        # l'arc est crée à partir d'un rect. Cependant pygame, le crée en fonction de l'angle de départ de fin.
        # du coup, dans le cadre d'un angle d'un quart de cercle (0->pi/2), il faut recalculer la taille du rectangle
        # pour qu'il suive le pointeur de la souris.
        self.new_width = self.width * 2
        self.new_height = self.height * 2
        xo, yo = self.points[0][0], self.points[0][1]
        self.angle_start = 0
        self.angle_start = pi/2
        new_origine = self.points[0]
        if self.orientation == 0:
            self.angle_start = pi / 2
            self.angle_end = pi
            self.center = self.points[0][0], self.points[0][1] - self.height

        elif self.orientation == 1:
            self.angle_start = 0
            self.angle_end = pi/2
            self.center = self.points[1][0] - self.width, self.points[1][1]
            xo, yo = new_origine[0], new_origine[1]

        elif self.orientation == 2:
            self.angle_start = 3 * pi/2
            self.angle_end = 2 * pi
            self.center = self.points[1][0]-self.width, self.points[0][1] - self.height
            xo, yo = new_origine[0], self.points[0][1] - self.height

        elif self.orientation == 3:
            self.angle_start = pi
            self.angle_end = 3 * pi/2
            self.center = self.points[0][0], self.points[0][1] - self.height
            xo, yo = self.points[0][0], self.points[0][1] - self.height

        self.new_rect = Rect(self.center[0], self.center[1], self.new_width, self.new_height)
        pygame.draw.rect(self.surface, (50, 20, 20), self.new_rect, 1)
        pygame.draw.rect(self.surface, (50, 50, 50), [xo, yo, self.width, self.height], 1)

    def point_projete(self):
        # calcul d'angle entre la droite centre-souris (CS) et l'horizontal
        self.angle_mouse = angle_droite(self.center, self.mouse_pos)

        # coordonnées du point A d'intersection avec le cercle rouge (C1) et la droite CS
        x = self.width * cos(self.angle_mouse) + self.center[0]
        y = self.width * sin(self.angle_mouse) + self.center[1]
        pt_A = x, y

        # coordonnées du point B d'intersection avec le cercle vert (C2) et la droite CS
        x2 = self.height * cos(self.angle_mouse) + self.center[0]
        y2 = self.height * sin(self.angle_mouse) + self.center[1]

        pt_B = x2, y2

        # le point projete P sur l'ellipse à partir des deux cercles et de la droite CS
        pt_P = x, y2

        # coordonnées du point D symetrique au point P par rapport à CS
        pt_D = x2, y

        # calcul de l'angle de la droite CS' passant par les points centre (C) et P'
        angle2 = angle_droite(self.center, (x2, y))

        # Calcul des coordonnées du point A' à l'intersection de C1 et de CS'
        x3 = self.width * cos(angle2) + self.center[0]
        y3 = self.width * sin(angle2) + self.center[1]
        pt_AA = x3, y3

        # Calcul des coordonnées du point B' à l'intersection de C2 et de CS'
        x4 = self.height * cos(angle2) + self.center[0]
        y4 = self.height * sin(angle2) + self.center[1]
        pt_BB = x4, y4

        # coordonnées du point P' point à l'intersection de la droite CS et de l'ellipse:
        self.point_mouse_projete = x3, y4

        # point equidistant avec la souris et le centre pour creer la deuxieme droite bleu
        x5 = self.center_to_mouse * cos(angle2) + self.center[0]
        y5 = self.center_to_mouse * sin(angle2) + self.center[1]
        pt_SS = x5, y5

        if self.affiche_projection:
            # Dessin des cerlces de supports de l'ellipse
            pts_circle = [[self.center, self.width, (255, 0, 0)], [self.center, self.height, (0, 255, 0)]]
            for pt in pts_circle:
                pygame.draw.circle(self.surface, pt[2], pt[0], pt[1], 1)

            pts_Point = [[self.mouse_pos, (0, 0, 255)], [pt_A, (255, 0, 0)], [pt_B, (0, 255, 0)],
                         [pt_P, (125, 125, 125)], [pt_D, (125, 125, 125)],
                         [pt_AA, (255, 0, 0)], [pt_BB, (0, 255, 0)], [self.point_mouse_projete, (255, 255, 255)]]
            for pt in pts_Point:
                self.draw_point(pt[0], pt[1])

            line_pts = [[self.center, self.mouse_pos, (0, 0, 255)], [pt_P, pt_B, (0, 125, 0)]]
            for pt in line_pts:
                self.draw_line(pt[0], pt[1], pt[2])

            dash_pts = [[self.center, pt_SS, (0, 0, 255)], [pt_P, pt_A, (255, 0, 0)], [pt_D, pt_B, (0, 255, 0)],
                        [pt_D, pt_A, (255, 0, 0)],
                        [self.point_mouse_projete, pt_B, (0, 255, 0)], [self.point_mouse_projete, pt_AA, (0, 0, 255)]]
            for dp in dash_pts:
                self.draw_line(dp[0], dp[1], dp[2], 1, True, 4)

    def draw_point(self, xy: tuple, c=(255, 255, 255), d=5):
        pygame.draw.circle(self.surface, c, xy, d)

    def draw_line(self, pt_A, pt_B, color=(255, 255, 255), ep=1, dash: bool = False, dash_len: int = 4):
        if not dash:
            pygame.draw.line(self.surface, color, pt_A, pt_B, ep)
        else:
            dl = DashedLine(self.surface, color, pt_A, pt_B, ep, dash_len)
            dl.update()

    def modif_point_to(self, npt: int, coord: tuple):
        if npt == 0:
            self.points[npt] = coord
        elif npt == 1:
            self.pos_end(coord[0], coord[1])
        self.statut = "modified"

    def check_orientation(self):
        if self.points[1][1] < self.points[0][1]:
            if self.points[1][0] > self.points[0][0]:
                self.orientation = 0
            else:
                self.orientation = 1
        else:
            if self.points[1][0] > self.points[0][0]:
                self.orientation = 3
            else:
                self.orientation = 2

    def action_is_moving(self, mouse_pos):
        if self.under_modif:
            self.pos_end(mouse_pos[0], mouse_pos[1])

        self.mouse_pos = mouse_pos
        self.center_to_mouse = sqrt((mouse_pos[0] - self.center[0]) ** 2 + (mouse_pos[1] - self.center[1]) ** 2)

    def is_overed(self):
        self.overed = False
        angle = 2 * pi - self.angle_mouse
        if (angle >= self.angle_start) & (angle <= self.angle_end):
            if (self.point_mouse_projete[0] - self.marge < self.mouse_pos[0]) & (
                    self.point_mouse_projete[0] + self.marge > self.mouse_pos[0]) & (
                    self.point_mouse_projete[1] - self.marge < self.mouse_pos[1]) & (
                    self.point_mouse_projete[1] + self.marge > self.mouse_pos[1]):
                self.overed = True


def angle_droite(c, s):
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
