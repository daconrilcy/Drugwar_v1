from pygame import Surface, mouse, MOUSEBUTTONUP, MOUSEBUTTONDOWN, event
from tools.draw import PtLine, DrawLine
from tools.editor_path.interface import InterfaceEditor


class EditorPath:
    def __init__(self, surface: Surface, marge=20):
        self.surface = surface
        self.marge = marge
        self.lines = []
        self.statut = "off"
        self.line_encours = None
        self.is_clicked = False
        self.mouse_pos = None
        self.delay_ini = 50
        self.delay = self.delay_ini
        self.points = []
        self.interface = None
        self.color_bt = (125, 125, 125)

        self.create_interface()

    def add_line(self):
        print("add")
        self.lines.append(
            DrawLine(self.surface, self.mouse_pos.x, self.mouse_pos.y)
        )
        self.line_encours = len(self.lines) - 1

    def del_line(self, n):
        self.lines.remove(n)

    def update_line_n(self):
        self.lines[self.line_encours].change_end(self.mouse_pos)

    def handle_event(self, ev: event):
        ms_p = mouse.get_pos()
        self.mouse_pos = PtLine(ms_p[0], ms_p[1])
        if ev.type == MOUSEBUTTONDOWN:
            self.button_down()
        elif ev.type == MOUSEBUTTONUP:
            pass

    def button_down(self):
        if self.statut == "off":
            line = self.check_click_online_n()
            if line == -1:
                self.statut = "create"
            else:
                self.statut = "edit"
        elif self.statut == "edit":
            self.statut = "off"
            self.line_encours = None

    def check_click_online_n(self):
        result = -1
        if len(self.lines) > 0:
            for n in range(len(self.lines)):
                if self.lines[n].pt_is_inline(self.mouse_pos, self.marge):
                    result = n
                    self.line_encours = n
                    print("click on line : " + str(n))
                    break
        if result == -1:
            self.line_encours = None
        return result

    def update(self):
        if self.statut == "create":
            self.add_line()
            self.statut = "edit"
        elif self.statut == "edit":
            self.update_line_n()
        for line in self.lines:
            line.update()

        self.interface.update()

    def create_interface(self):
        self.interface = InterfaceEditor(self.surface)
        self.interface.add_button(0, 0, 60, heigh=None, color=self.color_bt,
                                  path_image='C:\\Users\86010478\PycharmProjects\pythonProject\Drugwar_v1\\tools\editor_path\img\\bt_courbe.png')
        self.interface.add_button(0, 60, 60)
        self.interface.add_button(0, 120, 60)
        self.interface.add_button(0, 1800, 60)
