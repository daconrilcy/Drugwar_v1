from pygame import Surface, MOUSEBUTTONDOWN, MOUSEBUTTONUP, KEYUP, KEYDOWN, K_l, K_a, event, mouse, draw
from tools.draw import DrawLine
from tools.draw.arc import Arc


class ActionEdithPath:
    def __init__(self, surface: Surface, marge: int = 10):
        self.surface = surface
        self.mouse_pos = 0, 0
        self.mouse_bt = None
        self.key_pos = None
        self.key = None
        self.forms = []
        self.form_overed = None
        self.pt_form_overed = -1
        self.form_selected = None
        self.pt = 0
        self.statut = ""
        self.under_modif = False
        self.type_crea = ""
        self.rond_crea_rayon = 5
        self.rond_crea_color = (0, 255, 0)
        self.marge = marge
        self.mouse_old_pos = 0, 0
        self.nb_points_form = 2

    def action_to_do(self):
        if self.key_pos == KEYUP:
            if self.key == K_l:
                if self.statut == "prepare":
                    self.statut = ""
                    self.type_crea = ""
                else:
                    self.key = None
                    self.statut = "prepare"
                    self.type_crea = "line"
                    self.under_modif = False
                    self.nb_points_form = 2
            elif self.key == K_a:
                if self.statut == "prepare":
                    self.statut = ""
                    self.type_crea = ""
                else:
                    self.key = None
                    self.statut = "prepare"
                    self.type_crea = "arc"
                    self.under_modif = False
                    self.nb_points_form = 2
                    print("crea arc")
        if self.mouse_bt == MOUSEBUTTONUP:
            if self.statut == "prepare":
                self.statut = "crea"
                self.pt = 1
                self.mouse_bt = None
                self.add_form()
                self.under_modif = True

            elif self.statut == "crea":
                self.pt += 1
                if self.pt < self.nb_points_form:
                    self.mouse_bt = None
                    self.under_modif = True
                else:
                    self.pt = 0
                    self.statut = ""
                    self.mouse_bt = None
                    self.form_selected.under_modif = False
                    self.form_selected = None

        if self.form_overed is not None:
            if self.statut == "":
                if self.mouse_bt == MOUSEBUTTONDOWN:
                    self.mouse_old_pos = self.mouse_pos
                    self.form_selected = self.form_overed
                    self.pt = self.pt_form_overed
                    self.pt_form_overed = None
                    self.form_overed = None
                    self.statut = "modif"
                    self.modif_form()

        if (self.statut == "modif") | (self.statut == "deplacement"):
            if self.mouse_bt == MOUSEBUTTONUP:
                self.form_selected = None
                self.statut = ""

    def update_form(self):
        if (self.statut == "modif") | (self.statut == "crea"):
            self.modif_point_form()
        if self.statut == "deplacement":
            self.modif_form_deplacement()

        for form in self.forms:
            form.update()

    def update(self):
        self.action_to_do()
        self.update_form()
        self.check_overed()
        self.rond_crea()

    def handle(self, ev: event):
        self.mouse_pos = mouse.get_pos()
        if (ev.type == MOUSEBUTTONUP) | (ev.type == MOUSEBUTTONDOWN):
            self.mouse_bt = ev.type
        elif (ev.type == KEYUP) | (ev.type == KEYDOWN):
            self.key_pos = ev.type
            self.key = ev.key
        else:
            self.mouse_bt = None
            self.key_pos = None
            self.key = None

    def add_form(self):
        if self.type_crea == "line":
            self.forms.append(
                DrawLine(surface=self.surface, x=self.mouse_pos[0], y=self.mouse_pos[1], marge=self.marge)
            )
            self.form_selected = self.forms[len(self.forms)-1]
            self.form_selected.under_modif = True
        elif self.type_crea == "arc":
            self.forms.append(
                Arc(surface=self.surface, x=self.mouse_pos[0], y=self.mouse_pos[1], marge=self.marge)
            )
            self.form_selected = self.forms[len(self.forms)-1]
            self.form_selected.under_modif = True

    def modif_point_form(self):
        self.form_selected.modif_point_to(self.pt, self.mouse_pos)

    def check_overed(self):
        self.form_overed = None
        for form in self.forms:
            form.mouse_pos = self.mouse_pos
            if form.overed:
                self.form_overed = form
                self.pt_form_overed = self.form_overed.pt_survol
                break

    def modif_form(self):
        if self.pt > -1:
            self.under_modif = True
        else:
            self.statut = "deplacement"

    def modif_form_deplacement(self):
        dif_x = self.mouse_pos[0] - self.mouse_old_pos[0]
        dif_y = self.mouse_pos[1] - self.mouse_old_pos[1]
        for n in range(len(self.form_selected.points)):
            x = self.form_selected.points[n][0] + dif_x
            y = self.form_selected.points[n][1] + dif_y
            self.form_selected.points[n] = (x, y)

        self.mouse_old_pos = self.mouse_pos

    def rond_crea(self):
        if self.statut == "prepare":
            draw.circle(self.surface, self.rond_crea_color,
                        (self.mouse_pos[0], self.mouse_pos[1]), self.rond_crea_rayon)
