import pygame
from tools.draw import PtLine, DrawLine


class EditorPath:
    def __init__(self, surface: pygame.surface, marge=20):
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

    def handle_event(self, event: pygame.event):
        ms_p = pygame.mouse.get_pos()
        self.mouse_pos = PtLine(ms_p[0],ms_p[1])
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.button_down()
        elif event.type == pygame.MOUSEBUTTONUP:
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
        if len(self.lines)> 0:
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

