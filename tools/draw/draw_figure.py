import math

from pygame import draw, Color
from pygame import Surface, MOUSEBUTTONDOWN, MOUSEBUTTONUP


class DrawFigure:
    def __init__(self, surface: Surface, x: float, y: float,
                 color_base: tuple = (255, 100, 100), color_overed: tuple = (50, 255, 50), color_selected=(255, 0, 0),
                 ep_base: int = 2, ep_survol: int = 4, ep_selected: int = 4,
                 marge: int = 10, rayon_pts: int = 2, pas: int = 32):

        self.surface = surface

        self.color_ini = Color(color_base[0], color_base[1], color_base[2])
        self.color = self.color_ini
        self.color_overed = Color(color_overed[0], color_overed[1], color_overed[2])
        self.color_selected = Color(color_selected[0], color_selected[1], color_selected[2])

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

        self.pas = pas
        self.grided = False

        self.prev_clic = None
        self.clicked = False

    def test_clic(self):
        self.clicked = False
        if (self.prev_clic == MOUSEBUTTONDOWN) & (self.mouse_statut == MOUSEBUTTONUP):
            self.clicked = True

    def create(self):
        self.under_creation = True
        if self.clicked:
            self.n_clic += 1

        if self.n_clic == 0:
            draw.circle(self.surface, color=self.color_ini, center=self.mouse_pos, radius=5)
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
        self.selected = True

    def get_pt2(self):
        return 0, 0

    def modif(self, pt: tuple):
        pass

    def modif_point_to(self, n_pt: int, pt: tuple):
        if self.grided:
            x, y = round(pt[0]/self.pas, 0)*self.pas, round(pt[1]/self.pas, 0)*self.pas
        else:
            x, y = pt[0], pt[1]
        self.points[n_pt] = x, y
        self.update_formula()

    def update_formula(self):
        self.define_min_max()

    def update(self, mouse_pos: tuple, mouse_statut):
        self.mouse_pos = mouse_pos
        self.mouse_statut = mouse_statut
        self.test_clic()
        if not self.under_creation:
            self.overhead_selected_behaviour()

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
            pt2 = self.get_pt2()
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
                    if self.grided:
                        a = round(a/self.pas, 0)*self.pas
                        b = round(a/self.pas, 0)*self.pas
                    self.points[n] = a, b
                self.update_formula()
                self.old_mouse_pos = self.mouse_pos

    def button_up(self):
        if self.mouse_statut == MOUSEBUTTONUP:
            self.pt_move = -1
            self.old_mouse_pos = None

    def move_point_to(self):
        if self.pt_move > -1:
            if not self.grided:
                x, y = self.mouse_pos
            else:
                x = round(self.mouse_pos[0]/self.pas, 0)*self.pas
                y = round(self.mouse_pos[1]/self.pas, 0)*self.pas

            self.points[self.pt_move] = x, y
            self.update_formula()

    def is_mouse_in_zone(self):
        return self.pt_is_in_zone(self.mouse_pos)
    
    def pt_is_in_zone(self, pt):
        if (pt[0] <= self.max_x) & (pt[0] >= self.min_x):
            if (pt[1] <= self.max_y) & (pt[1] >= self.min_y):
                return True
        return False

    def define_min_max(self):
        self.min_x = self.points[0][0]
        self.max_x = self.points[1][0]
        self.min_y = self.points[0][1]
        self.max_y = self.points[1][1]
        for point in self.points:
            if point[0] > self.max_x:
                self.max_x = point[0]
            if point[0] < self.min_x:
                self.min_x = point[0]
            if point[1] > self.max_y:
                self.max_y = point[1]
            if point[1] < self.min_y:
                self.min_y = point[1]

    def overhead_selected_behaviour(self):
        self._ep = self._ep_ini
        self.color = self.color_ini
        color_pt = self.color_ini
        r = self._ep / 2
        pt = self.points[0]
        if self.pt_selected > -1:
            color_pt = self.color_selected
            r = self._ep_selected
            pt = self.points[self.pt_selected]
        elif self.selected:
            self.color = self.color_selected
            self._ep = self._ep_selected
        elif self.pt_survol > -1:
            color_pt = self.color_overed
            r = self._ep_overed
            pt = self.points[self.pt_survol]
        if self.overed & (self.pt_survol == -1) & (not self.selected):
            self._ep = self._ep_overed
            self.color = self.color_overed
        if (self.pt_survol > -1) | (self.pt_selected > -1):
            draw.circle(surface=self.surface, color=color_pt,
                        center=(pt[0], pt[1]),
                        radius=r)
