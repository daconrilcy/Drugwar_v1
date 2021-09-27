import pygame


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
        self.feet_position = pygame.Rect(0, 0, 32, 32)
        self.old_position = self.position.copy()

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

    def move(self, direction: int):
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
        self.rect.center = self.position
        self.feet_position.midbottom = self.rect.midbottom

    def move_back(self):
        self.position = self.old_position
        self.rect.center = self.position
        self.feet_position.midbottom = self.rect.midbottom
