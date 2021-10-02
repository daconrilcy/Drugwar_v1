import pygame
from math import sqrt

class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super(Player, self).__init__()
        self.sprite_sheet = pygame.image.load(
            'D:\Python\pythonProject\Drugwar_v1\gamelib\inteface\player\player_simple.png')
        self.image = self.get_image(0, 0)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.speed_move = 2
        self.feet_position = pygame.Rect(0, 0, self.rect.width * 0.3, 5)
        self.old_position = self.position.copy()
        self.is_moving = False
        self.target_move = None
        self.delta_x = 0
        self.delta_y = 0
        self.cos_di = 0
        self.sin_di = 0
        self.images = {
            "down": self.get_image(32, 0),
            "up": self.get_image(32, 96),
            "left": self.get_image(32, 32),
            "right": self.get_image(32, 64)
        }

    def save_location(self):
        self.old_position = self.position.copy()

    def get_image(self, x, y):
        image = pygame.Surface([32, 32])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))
        return image

    def change_animation(self, name: str):
        self.image = self.images[name]
        self.image.set_colorkey([0, 0, 0])

    def move_to(self, x, y):
        self.is_moving = True
        self.target_move = (x, y)
        self.delta_x = x - self.position[0]
        self.delta_y = y - self.position[1]

        dist = sqrt(self.delta_x ** 2 + self.delta_y ** 2)
        if dist != 0:
            self.sin_di = self.delta_y/dist
            self.cos_di = self.delta_x/dist
        else:
            self.sin_di = 0
            self.cos_di = 0

    def __auto_move(self):
        delta_x = self.target_move[0] - self.position[0]
        delta_y = self.target_move[1] - self.position[1]
        if abs(delta_x) > self.speed_move:
            self.position[0] += self.speed_move * self.cos_di
            if self.position[0] < 0:
                self.position[0] = 0
        else:
            self.position[0] = self.target_move[0]

        if abs(delta_y) > self.speed_move:
            self.position[1] += self.speed_move * self.sin_di
            if self.position[1] < 0:
                self.position[1] = 0
        else:
            self.position[1] = self.target_move[1]

        if self.position == self.target_move:
            self.is_moving = False

    def move(self, direction: int):
        self.is_moving = False
        if direction == 0:
            self.position[1] -= self.speed_move
            self.change_animation('up')
        elif direction == 1:
            self.position[1] += self.speed_move
            self.change_animation('down')
        elif direction == 2:
            self.position[0] -= self.speed_move
            self.change_animation('left')
        elif direction == 3:
            self.position[0] += self.speed_move
            self.change_animation('right')
        if self.position[0] < 0:
            self.position[0] = 0
        if self.position[1] < 0:
            self.position[1] = 0

    def update(self):
        if self.is_moving:
            self.__auto_move()
        self.rect.center = self.position
        self.feet_position.midbottom = self.rect.midbottom

    def move_back(self):
        self.is_moving = False
        self.position = self.old_position
        self.rect.center = self.position
        self.feet_position.midbottom = self.rect.midbottom


