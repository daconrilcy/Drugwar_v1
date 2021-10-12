import pygame
from math import pi, cos, sin, sqrt, atan
import numpy as np


class PtLine:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def get_tuple(self):
        return self.x, self.y

    def set(self, x: float, y: float):
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


class Arc:
    def __init__(self, surface: pygame.Surface, x, y):
        self.surface = surface
        self.ep = 5
        self.ep_survol = 10
        self.ep_encours = self.ep
        self.origine = x, y
        self.new_origine = x, y
        self.end = x, y
        self.center = x, y
        self.color = pygame.Color(255, 255, 255)
        self.form = None
        self.width = 0
        self.new_width = 0
        self.new_height = 0
        self.height = 0
        self.new_rect = pygame.Rect(0, 0, 0, 0)
        self.angle_start = 0
        self.angle_end = pi/2
        self.angle_mouse = 0
        self.orientation = 0
        self.first_mouse_pos = 0, 0

        self.is_active = False
        self.is_modif = False
        self.is_create_new = False

        self.mouse_pos = x, y

        self.delai_affich_ini = 500
        self.delai_affich = self.delai_affich_ini
        self.marge = 10
        self.l_p = None
        self.center_to_mouse = 0
        self.point_mouse_projete = 0, 0

        self.affiche_projection = False
        self.affiche_donnee = False
        self.survol = False

    def reset(self):
        self.origine = 0, 0
        self.new_origine = 0, 0
        self.end = 0, 0
        self.center = 0, 0
        self.width = 0
        self.new_width = 0
        self.new_height = 0
        self.height = 0
        self.new_rect = pygame.Rect(0, 0, 0, 0)
        self.is_active = False
        self.delai_affich = self.delai_affich_ini
        self.l_p = None
        self.affiche_projection = False

    def update(self):

        if self.is_modif:
            self.draw_rect()

        if self.is_active:
            self.point_projete()
            self.mouse_is_on_arc()

        self.comportement_survol()
        if self.is_active | self.is_modif:
            self.form = pygame.draw.arc(self.surface, self.color,  self.new_rect,
                                        self.angle_start, self.angle_end,
                                        self.ep_encours)
        self.check_orientation()
        self.affich()

    def affich(self):
        if self.affiche_donnee:
            self.delai_affich -= 1
            if self.delai_affich < self.delai_affich_ini:
                print(self.orientation)
                self.delai_affich = self.delai_affich_ini

    def create_new(self):
        self.is_create_new = True
        self.reset()

    def pos_end(self, x, y):
        self.end = x, y
        self.width = abs(self.end[0] - self.origine[0])
        self.height = abs(self.end[1] - self.origine[1])

    def draw_rect(self):
        # l'arc est crée à partir d'un rect. Cependant pygame, le crée en fonction de l'angle de départ de fin.
        # du coup, dans le cadre d'un angle d'un quart de cercle (0->pi/2), il faut recalculer la taille du rectangle
        # pour qu'il suive le pointeur de la souris.
        if self.orientation == 0:
            self.angle_start = 0
            self.angle_end = pi/2
            self.new_origine = self.origine[0] - self.width, self.origine[1]
            self.new_width = self.width * 2
            self.new_height = self.height * 2
            self.center = self.origine[0], self.origine[1] + self.height
            self.new_rect = pygame.Rect(self.new_origine[0], self.new_origine[1], self.new_width, self.new_height)
            pygame.draw.rect(self.surface, (50, 50, 50), [self.origine[0], self.origine[1], self.width, self.height], 1)
            pygame.draw.rect(self.surface, (50, 20, 20), self.new_rect, 1)
        elif self.orientation == 1:
            self.angle_start = pi/2
            self.angle_end = pi
            self.new_origine = self.end[0], self.origine[1]
            self.new_width = self.width * 2
            self.new_height = self.height * 2
            self.center = self.origine[0], self.origine[1] + self.height
            self.new_rect = pygame.Rect(self.new_origine[0], self.new_origine[1], self.new_width, self.new_height)
            pygame.draw.rect(self.surface, (50, 50, 50), [self.new_origine[0], self.new_origine[1], 
                                                          self.width, self.height], 1)
            pygame.draw.rect(self.surface, (50, 20, 20), self.new_rect, 1)
        elif self.orientation == 2:
            self.angle_start = pi
            self.angle_end = 3*pi/2
            self.new_origine = self.end[0], self.end[1]-self.height
            self.new_width = self.width * 2
            self.new_height = self.height * 2
            self.center = self.origine[0], self.origine[1] - self.height
            self.new_rect = pygame.Rect(self.new_origine[0], self.new_origine[1], self.new_width, self.new_height)
            pygame.draw.rect(self.surface, (50, 50, 50),
                             [self.new_origine[0], self.origine[1]-self.height, self.width, self.height], 1)
            pygame.draw.rect(self.surface, (50, 20, 20), self.new_rect, 1)
        elif self.orientation == 3:
            self.angle_start = 3*pi/2
            self.angle_end = 2 * pi
            self.new_origine = self.origine[0]-self.width, self.end[1]-self.height
            self.new_width = self.width * 2
            self.new_height = self.height * 2
            self.center = self.origine[0], self.origine[1] - self.height
            self.new_rect = pygame.Rect(self.new_origine[0], self.new_origine[1], self.new_width, self.new_height)
            pygame.draw.rect(self.surface, (50, 50, 50),
                             [self.origine[0], self.origine[1]-self.height, self.width, self.height], 1)
            pygame.draw.rect(self.surface, (50, 20, 20), self.new_rect, 1)

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
            pygame.draw.circle(self.surface, (255, 0, 0), self.center, self.width, 1)
            pygame.draw.circle(self.surface, (0, 255, 0), self.center, self.height, 1)

            self.draw_point(self.mouse_pos, (0, 0, 255))
            self.draw_point(pt_A, (255, 0, 0,))
            self.draw_point(pt_B, (0, 255, 0,))

            self.draw_point(pt_P, (125, 125, 125))
            self.draw_point(pt_D, (125, 125, 125))

            self.draw_point(pt_AA, (255, 0, 0))
            self.draw_point(pt_BB, (0, 255, 0))
            self.draw_point(self.point_mouse_projete)

            self.draw_line(self.center, self.mouse_pos, (0, 0, 255))
            self.draw_line_dashed(start_pos=self.center, end_pos=pt_SS, color=(0, 0, 255))
            self.draw_line(pt_P, pt_B, (0, 125, 0))
            self.draw_line_dashed(start_pos=pt_P, end_pos=pt_A, color=(125, 0, 0))
            self.draw_line_dashed(start_pos=pt_D, end_pos=pt_B, color=(0, 125, 0))
            self.draw_line_dashed(start_pos=pt_D, end_pos=pt_A, color=(125, 0, 0))
            self.draw_line_dashed(start_pos=self.point_mouse_projete, end_pos=pt_BB, color=(0, 125, 0))
            self.draw_line_dashed(start_pos=self.point_mouse_projete, end_pos=pt_AA, color=(125, 0, 0))

    def draw_point(self, xy: tuple, c=(255, 255, 255), d=5):
        pygame.draw.circle(self.surface, c, xy, d)

    def draw_line(self, pt_A, pt_B, color=(255, 255, 255), ep=1):
        pygame.draw.line(self.surface, color, pt_A, pt_B, ep)

    def draw_line_dashed(self, color=(255, 255, 255), start_pos=(0, 0), end_pos=(0, 0), width=1, dash_length=4,
                         exclude_corners=True):
        # Code copié à partir du web :
        # https://codereview.stackexchange.com/questions/70143/drawing-a-dashed-line-with-pygame

        # convert tuples to numpy arrays
        start_pos = np.array(start_pos)
        end_pos = np.array(end_pos)

        # get euclidian distance between start_pos and end_pos
        length = np.linalg.norm(end_pos - start_pos)

        # get amount of pieces that line will be split up in (half of it are amount of dashes)
        dash_amount = int(length / dash_length)

        # x-y-value-pairs of where dashes start (and on next, will end)
        dash_knots = np.array([np.linspace(start_pos[i], end_pos[i], dash_amount) for i in range(2)]).transpose()

        [pygame.draw.line(self.surface, color, tuple(dash_knots[n]), tuple(dash_knots[n + 1]), width)
         for n in range(int(exclude_corners), dash_amount - int(exclude_corners), 2)]

    def action_click(self, position, mouse_pos):
        if self.is_create_new:
            if position == "down":
                self.is_active = False
                self.is_modif = True
                self.first_mouse_pos = mouse_pos
                self.origine = mouse_pos[0], mouse_pos[1]
                self.pos_end(mouse_pos[0], mouse_pos[1])

            elif position == "up":
                self.pos_end(mouse_pos[0], mouse_pos[1])
                self.is_modif = False
                self.is_active = True
                self.is_create_new = False

    def check_orientation(self):
        if self.mouse_pos[1] > self.first_mouse_pos[1]:
            if self.mouse_pos[0] > self.first_mouse_pos[0]:
                self.orientation = 0
            else:
                self.orientation = 1
        else:
            if self.mouse_pos[0] > self.first_mouse_pos[0]:
                self.orientation = 3
            else:
                self.orientation = 2

    def action_is_moving(self, mouse_pos):
        if self.is_modif:
            self.pos_end(mouse_pos[0], mouse_pos[1])

        self.mouse_pos = mouse_pos
        self.center_to_mouse = sqrt((mouse_pos[0] - self.center[0]) ** 2 + (mouse_pos[1] - self.center[1]) ** 2)

    def mouse_is_on_arc(self):
        angle = 2 * pi - self.angle_mouse
        if (angle >= self.angle_start) & (angle <= self.angle_end):
            if (self.point_mouse_projete[0]-self.marge < self.mouse_pos[0]) & (
                    self.point_mouse_projete[0] + self.marge > self.mouse_pos[0]) & (
                self.point_mouse_projete[1] - self.marge < self.mouse_pos[1]) & (
                    self.point_mouse_projete[1] + self.marge > self.mouse_pos[1]):
                self.survol = True
            else:
                self.survol = False
        else:
            self.survol = False

    def comportement_survol(self):
        if self.survol:
            self.ep_encours = self.ep_survol
        else:
            self.ep_encours = self.ep


class DrawPoint:
    def __init__(self, x, y, r=10, surface: pygame.Surface = None, color: pygame.Color = pygame.Color(255, 0, 0)):
        self.surface = surface
        self.center = PtLine(x, y)
        self.rayon = r
        self.color = color
        self.active = True
        self.form = None

    def update(self):
        self.form = pygame.draw.circle(surface=self.surface,
                                       center=(self.center.x, self.center.y), radius=self.rayon,
                                       color=self.color)


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
