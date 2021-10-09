import pygame
from tools.draw import PtLine, DrawLine


class ButtonInterface:
    def __init__(self, surface: pygame.Surface, left, top, width, height=None, color=(125, 125, 125)):
        self.surface = surface
        self.width = width
        self.height = height
        if height is None:
            self.height = width
        self.top = top
        self.left = left
        self.rect_interieur: pygame.Rect
        self.bord_haut = None
        self.bord_droit = None
        self.bord_bas = None
        self.bord_gauche = None
        self.fill_color_default = color
        self.fill_color = color
        self.fill_selected = (100, 100, 100)
        self.p1 = left, top
        self.p2 = left + width, top
        self.p3 = left + width, top + height
        self.p4 = left, top + height
        self.ep = 1
        self.is_overed = False
        self.is_selected = False
        self.fill_overed = (180, 180, 180)

    def update(self):
        self.update_points()
        self.update_lines()
        self.mouse_is_over()
        self.fill_color_update()

        self.update_fill_rect()


    def update_points(self):
        self.p1 = self.left, self.top
        self.p2 = self.left + self.width, self.top
        self.p3 = self.left + self.width, self.top + self.height
        self.p4 = self.left, self.top + self.height

    def update_lines(self):
        self.bord_haut = self.update_line(self.p1, self.p2, (180, 180, 180))
        self.bord_droit = self.update_line(self.p2, self.p3, (180, 180, 180))
        self.bord_bas = self.update_line(self.p3, self.p4, (100, 100, 100))
        self.bord_gauche = self.update_line(self.p4, self.p1, (100, 100, 100))

    def update_line(self, p1: tuple, p2: tuple, color):
        return pygame.draw.line(self.surface, color, p1, p2, self.ep)

    def update_fill_rect(self, color=None):
        if color is None:
            color = self.fill_color

        pygame.draw.rect(self.surface, color, (self.left+self.ep, self.top+self.ep, self.width-self.ep,
                                               self.height-self.ep))

    def mouse_is_over(self):
        mouse_pos = pygame.mouse.get_pos()
        if (mouse_pos[0] > self.left) & (mouse_pos[0]< self.left + self.width) & (
                mouse_pos[1] > self.top) & (mouse_pos[1] < self.top + self.height):
            self.is_overed = True
        else:
            self.is_overed = False

    def fill_color_update(self):
        if self.is_overed:
            self.fill_color = self.fill_overed
        else:
            self.fill_color = self.fill_color_default
        if self.is_selected:
            self.fill_color = self.fill_selected


class InterfaceEditor:
    def __init__(self, surface: pygame.Surface):
        self.surface = surface
        self.buttons = []
        self.is_visible = True

    def update(self):
        if self.is_visible:
            self.update_buttons()

    def add_button(self, left, top, width, heigh=None, color=(125, 125, 125)):
        if heigh is None:
            heigh = width
        self.buttons.append(ButtonInterface(self.surface, left, top, width, heigh, color))

    def update_buttons(self):
        for button in self.buttons:
            button.update()


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
        self.interface = None

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

    def handle_event(self, event: pygame.event):
        ms_p = pygame.mouse.get_pos()
        self.mouse_pos = PtLine(ms_p[0], ms_p[1])
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
        self.interface.add_button(0, 0, 40)
        self.interface.add_button(0, 40, 40)
        self.interface.add_button(0, 80, 40)
        self.interface.add_button(0, 120, 40)

