from pygame import Surface, Rect
import pygame.draw


class ButtonInterface:
    def __init__(self, surface: Surface, left, top, width=40, height=None, color=(125, 125, 125), img_path: str = None):
        print(img_path)
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
        self.image = None
        if img_path is not None:
            self.image = pygame.transform.scale(pygame.image.load(img_path).convert_alpha(), (self.width, self.height))

    def update(self):
        self.update_points()
        self.update_lines()
        self.mouse_is_over()
        self.fill_color_update()
        self.update_fill_rect()
        if self.image is not None:
            self.surface.blit(self.image, (self.left, self.top))

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

        pygame.draw.rect(self.surface, color, (self.left + self.ep, self.top + self.ep, self.width - self.ep,
                                               self.height - self.ep))

    def mouse_is_over(self):
        mouse_pos = pygame.mouse.get_pos()
        if (mouse_pos[0] > self.left) & (mouse_pos[0] < self.left + self.width) & (
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
