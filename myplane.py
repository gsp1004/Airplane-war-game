import pygame
# from pygame.locals import *
# import sys
# import traceback


# 此类型初始化需要传入一个参数bg_size:屏幕大小
class Myplane(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)
        # 图片
        self.image1 = pygame.image.load(r'Images\hero\fly\hero1.png').convert_alpha()
        self.image2 = pygame.image.load(r'Images\hero\fly\hero2.png').convert_alpha()
        self.image_god = pygame.image.load(r'Images\hero\fly\hero_god.png').convert_alpha()
        self.image_destroy = []
        self.image_destroy.extend([\
            pygame.image.load(r'Images\hero\down\hero_blowup_n1.png').convert_alpha(),\
            pygame.image.load(r'Images\hero\down\hero_blowup_n2.png').convert_alpha(),\
            pygame.image.load(r'Images\hero\down\hero_blowup_n3.png').convert_alpha(),\
            pygame.image.load(r'Images\hero\down\hero_blowup_n4.png').convert_alpha()\
            ])
        # 背景大小
        self.bg_width, self.bg_height = bg_size[0], bg_size[1]
        # 图片应该显示的位置信息和大小
        self.rect = self.image1.get_rect()
        self.rect.left = (self.bg_width - self.rect.width) // 2
        self.rect.top = self.bg_height - self.rect.height - 60
        # 飞机控制时候移动速度
        self.speed = 10
        # 飞机是否存活
        self.active = True
        # 完美碰撞检测的mask
        self.mask = pygame.mask.from_surface(self.image1)
        self.god = False

    def moveUp(self):
        if self.rect.top > 0:
            self.rect.top -= self.speed
        else:
            self.rect.top =0

    def moveDown(self):
        if self.rect.bottom < self.bg_height - 60:
            self.rect.top += self.speed
        else:
            self.rect.bottom = self.bg_height - 60

    def moveLeft(self):
        if self.rect.left > 0:
            self.rect.left -= self.speed
        else:
            self.rect.left =0

    def moveRight(self):
        if self.rect.right < self.bg_width:
            self.rect.left += self.speed
        else:
            self.rect.right = self.bg_width

    def reset(self):
        self.active = True
        self.rect.left = (self.bg_width - self.rect.width) // 2
        self.rect.top = self.bg_height - self.rect.height - 60    
        self.god = True
