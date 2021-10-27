import math

import pygame.draw
from pygame import Surface, MOUSEBUTTONDOWN, MOUSEBUTTONUP


class DrawFigure:
    def __init__(self, surface: Surface, x: float, y: float,
                 color_base: tuple = (180, 180, 180), color_overed: tuple = (200, 200, 200), color_selected=(255, 0, 0),
                 ep_base: int = 4, ep_survol: int = 6, ep_selected: int = 6,
                 marge: int = 10, rayon_pts: int = 2):

        self.surface = surface

        self.color_ini = color_base
        self.color = color_base
        self.color_overed = color_overed
        self.color_selected = color_selected

        self._ep_ini = ep_base
        self._ep = ep_base
        self._ep_overed = ep_survol
        self._ep_selected = ep_selected

        self.under_creation = False
        self.under_modif = False
        self.under_deplacement = False
        self.created = False

        self.overed = False
        self.selected = False

        self.pt_survol: int = -1
        self.pt_selected: int = -1
        self.pt_move: int = -1

        self.mouse_pos = x, y
        self.mouse_statut = None
        self.old_mouse_pos = x, y
        self.n_clic: int = 0

        self.marge = marge
        self.points = [(x, y), (x, y)]
        self.n_points = int(len(self.points))
        self.rayon_pts = rayon_pts

        self.max_x = 0
        self.min_x = 0
        self.max_y = 0
        self.min_y = 0

        self.active = False

        self.prev_clic = None
        self.clicked = False

    def test_clic(self):
        self.clicked = False
        if (self.prev_clic == MOUSEBUTTONDOWN) & (self.mouse_statut == MOUSEBUTTONUP):
            self.clicked = True

    def create(self, *args):
        self.under_creation = True
        if self.clicked:
            self.n_clic += 1

        if self.n_clic == 0:
            pygame.draw.circle(self.surface, color=self.color_ini, center=self.mouse_pos, radius=5)
            self.modif_point_to(0, self.mouse_pos)
            self.modif_point_to(1, self.mouse_pos)
        elif self.n_clic == 1:
            self.modif_point_to(1, self.mouse_pos)
            self.active = True
        elif self.n_clic == 2:
            self.n_clic = 0
            self.active = True
            self.created = True
            self.under_creation = False

        self.pt_selected = -1
        self.pt_survol = -1

    def get_y(self, x: float):
        pass

    def modif(self, pt: tuple):
        pass

    def modif_point_to(self, n_pt: int, pt: tuple):
        self.points[n_pt] = pt
        self.update_formula()

    def update_formula(self):
        pass

    def update(self, mouse_pos: tuple, mouse_statut):
        self.mouse_pos = mouse_pos
        self.mouse_statut = mouse_statut
        self.test_clic()

        if self.under_creation:
            self.create()
            self.draw()
        elif self.active:
            self.is_overed()
            self.is_point_overed()
            self.is_selected()
            self.is_point_selected()
            self.button_up()
            self.move_fig_to()
            self.move_point_to()
            self.draw()

        self.prev_clic = self.mouse_statut

    def draw(self):
        pass

    def is_overed(self):
        self.overed = False
        if self.is_mouse_in_zone():
            y2 = self.get_y(self.mouse_pos[0])
            pt2 = self.mouse_pos[0], y2
            if math.dist(self.mouse_pos, pt2) <= self.marge:
                self.overed = True

    def is_point_overed(self):
        self.pt_survol = -1
        for n in range(self.n_points):
            dist = math.dist(self.points[n], self.mouse_pos)
            if dist <= self.marge:
                self.pt_survol = n
                break

    def is_selected(self):
        if self.pt_selected == -1 & self.pt_move == -1:
            if self.mouse_statut == MOUSEBUTTONDOWN:
                if not self.selected:
                    if self.overed:
                        self.selected = True
                    else:
                        self.selected = False
            elif self.clicked:
                self.selected = False
                if self.overed:
                    self.selected = True
                    self.old_mouse_pos = self.mouse_pos
            else:
                self.old_mouse_pos = None

    def is_point_selected(self):
        if self.clicked:
            if self.pt_survol > -1:
                self.selected = False
                self.pt_selected = self.pt_survol
                self.pt_move = -1
                self.old_mouse_pos = None
            else:
                self.pt_selected = -1
                self.pt_move = -1
        elif self.mouse_statut == MOUSEBUTTONDOWN:
            if self.pt_survol > -1:
                self.pt_selected = self.pt_survol
                self.pt_move = self.pt_selected
                self.old_mouse_pos = None
            else:
                self.pt_selected = -1

    def move_fig_to(self):
        if self.selected & (self.mouse_statut == MOUSEBUTTONDOWN):
            if self.old_mouse_pos is None:
                self.old_mouse_pos = self.mouse_pos
            else:
                vec = self.mouse_pos[0] - self.old_mouse_pos[0], self.mouse_pos[1] - self.old_mouse_pos[1]
                for n in range(self.n_points):
                    a = self.points[n][0] + vec[0]
                    b = self.points[n][1] + vec[1]
                    self.points[n] = a, b
                self.update_formula()
                self.old_mouse_pos = self.mouse_pos

    def button_up(self):
        if self.mouse_statut == MOUSEBUTTONUP:
            self.pt_move = -1
            self.old_mouse_pos = None

    def move_point_to(self):
        if self.pt_move > -1:
            self.points[self.pt_move] = self.mouse_pos
            self.update_formula()

    def is_mouse_in_zone(self):
        if (self.mouse_pos[0] <= self.max_x) & (self.mouse_pos[0] >= self.min_x):
            if (self.mouse_pos[1] <= self.max_y) & (self.mouse_pos[1] >= self.min_y):
                print("In Zone")
                return True

        print("Hors Zone")
        return False

    def define_min_max(self):
        self.min_x = self.points[0][0]
        self.max_x = self.points[0][0]
        self.min_y = self.points[0][1]
        self.max_y = self.points[0][1]
        for point in self.points:
            if point[0] > self.max_x:
                self.max_x = point[0]
            if point[0] < self.min_x:
                self.min_x = point[0]
            if point[1] > self.max_y:
                self.max_y = point[1]
            if point[1] < self.min_y:
                self.min_y = point[1]
