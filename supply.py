import pygame
import random
# import sys
# import traceback

class SupplyBomb(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)
        self.bg_width, self.bg_height = bg_size
        self.image = pygame.image.load(r'Images/supply/supply_boom.png').convert_alpha()
        self.speed = 5
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.bottom = random.randint(0, self.bg_width - self.rect.width), 0
        self.mask = pygame.mask.from_surface(self.image)
        self.active = True

    def move(self):
        if self.rect.top < self.bg_height:
            self.rect.top += self.speed
        else:
            self.active = False

    def reset(self):
        self.active = True
        self.rect.left, self.rect.bottom = random.randint(0, self.bg_width - self.rect.width), 0

class SupplyBullet(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)
        self.bg_width, self.bg_height = bg_size
        self.image = pygame.image.load(r'Images/supply/supply_bullet.png').convert_alpha()
        self.speed = 5
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.bottom = random.randint(0, self.bg_width - self.rect.width), 0
        self.mask = pygame.mask.from_surface(self.image)
        self.active = True

    def move(self):
        if self.rect.top < self.bg_height:
            self.rect.top += self.speed
        else:
            self.active = False

    def reset(self):
        self.active = True
        self.rect.left, self.rect.bottom = random.randint(0, self.bg_width - self.rect.width), 0