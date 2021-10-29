from pygame import Surface, MOUSEBUTTONDOWN, MOUSEBUTTONUP
from tools.draw.draw_line import DrawLine
from tools.draw.draw_arc import DrawArc


class Forms:
    def __init__(self, surface: Surface):
        self.surface = surface
        self.figures = []
        self.mouse_pos = None
        self.mouse_bt = None
        self.act_figure = None
        self.n_act_figure = -1
        self.n_figures = 0
        self.grided = False
        self.selected_points = []
        self.joined_points = []
        self.act_point_selected = None
        self.joint_points_selected = None
        self.old_mouse_pos = self.mouse_pos
        self.vec_move_mouse = 0, 0
        self.act_point_selected_old_pos = None
        self.prev_act_points = None

    def add(self, type_forms: str = "line", pas: int = 32):
        create = False
        if type_forms == "line":
            self.figures.append(
                DrawLine(surface=self.surface, x=self.mouse_pos[0], y=self.mouse_pos[1], pas=pas)
            )
            create = True
        elif type_forms == "arc":
            self.figures.append(
                DrawArc(surface=self.surface, x=self.mouse_pos[0], y=self.mouse_pos[1], pas=pas)
            )
            create = True

        if create:
            self.n_figures += 1
            self.act_figure = self.n_figures - 1
            self.figures[self.act_figure].create()

    def edit(self, type_edit: str = "invert curve"):
        if type_edit == "invert curve":
            self.act_figure.reverse_curve()

    def delete(self):
        if self.act_figure is not None:
            self.update_sup_joint()
            self.figures.pop(self.n_act_figure)
            self.n_act_figure = -1
            self.act_figure = None
            self.n_figures -= 1

    def update(self, mouse_pos, mouse_bt):
        self.mouse_bt = mouse_bt
        self.mouse_pos = mouse_pos
        self.vec_move_mouse = self.get_vec_mouse()
        self.n_act_figure = -1
        self.act_figure = None
        for n in range(self.n_figures):
            self.figures[n].update(mouse_pos, mouse_bt)
            self.figures[n].grided = self.grided
            if self.figures[n].selected:
                self.act_figure = self.figures[n]
                self.n_act_figure = n
        self.select_joined_point()
        self.move_joined_points()

    def get_selected_points(self, selected_point):
        self.selected_points = selected_point

    def join_points(self):
        if len(self.selected_points) > 0:
            self.joined_points.append(self.selected_points)
        self.selected_points = []

    def select_joined_point(self):
        self.joint_points_selected = None
        for n_f in range(len(self.figures)):
            if self.figures[n_f].pt_selected > -1:
                pt_s = self.figures[n_f].pt_selected
                self.act_point_selected = [n_f, pt_s]
                if self.act_point_selected != self.prev_act_points:
                    self.act_point_selected_old_pos = self.figures[n_f].points[pt_s]
                for joined_group in self.joined_points:
                    for item in joined_group:
                        if (item[0] == n_f) & (item[1] == pt_s):
                            self.set_joined_selected(joined_group)
                            break

    def set_joined_selected(self, joined_group: list):
        n_fo = self.act_point_selected[0]
        n_fp = self.act_point_selected[1]
        for item in joined_group:
            n_f = item[0]
            n_p = item[1]
            self.figures[n_f].pt_selected = n_p
            self.joint_points_selected = joined_group

    def move_joined_points(self):
        if self.mouse_bt == MOUSEBUTTONDOWN:
            if self.old_mouse_pos is None:
                self.old_mouse_pos = self.mouse_pos
            if self.act_point_selected is not None:
                n_fo = self.act_point_selected[0]
                n_fp = self.act_point_selected[1]
                if self.joint_points_selected is not None:
                    pt_sel = self.figures[n_fo].points[n_fp]
                    vec_move = self.vec_move_mouse
                    pas = self.figures[n_fo].pas
                    if self.grided:
                        x_move = round((pt_sel[0] - self.act_point_selected_old_pos[0]) / pas, 0) * pas
                        y_move = round((pt_sel[1] - self.act_point_selected_old_pos[1]) / pas, 0) * pas
                        vec_move = x_move, y_move
                        if vec_move != (0, 0):
                            print(vec_move)

                    for gpe in self.joint_points_selected:
                        sel_point = self.figures[gpe[0]].pt_selected
                        new_point = _add_vec(self.figures[gpe[0]].points[sel_point], vec_move)
                        self.figures[gpe[0]].modif_point_to(sel_point, new_point)
                    self.old_mouse_pos = self.mouse_pos
                    dif_x = self.figures[n_fo].points[n_fp][0] - self.act_point_selected_old_pos[0]
                    dif_y = self.figures[n_fo].points[n_fp][1] - self.act_point_selected_old_pos[1]
                    self.act_point_selected_old_pos = self.figures[n_fo].points[n_fp]
        else:
            self.old_mouse_pos = None

    def get_vec_mouse(self):
        if self.old_mouse_pos is None:
            return 0, 0
        else:
            return _calc_vec_move(self.old_mouse_pos, self.mouse_pos)

    def update_sup_joint(self):
        # verifie les points joints de la figure à supprimer:
        for joined_group in self.joined_points:
            for n in range(len(joined_group)):
                if n < len(joined_group):
                    if joined_group[n][0] == self.n_act_figure:
                        joined_group.pop(n)

        # re index les joints group:
        for joined_group in self.joined_points:
            for n in range(len(joined_group)):
                if joined_group[n][0] > self.n_act_figure:
                    new_n_fig = joined_group[n][0] -1
                    joined_group[n][0] = new_n_fig


def _calc_vec_move(t1: tuple, t2: tuple):
    if t1 is None:
        return t2
    if t2 is None:
        return t1

    return t2[0]-t1[0], t2[1]-t1[1]


def _add_vec(t1: tuple, t2: tuple):
    a = t1[0] + t2[0]
    b = t1[1] + t2[1]
    return a, b
