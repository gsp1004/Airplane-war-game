import pygame
# from pygame.locals import *
import random
# import sys
# import traceback


# 此类型初始化需要传入一个参数bg_size:屏幕大小
class SmallEnemy(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)
        # 图片
        self.image_fly = pygame.image.load(r'Images\smallEnemy\fly\enemy1.png').convert_alpha()
        self.image_destroy = []
        self.image_destroy.extend([\
                        pygame.image.load(r'Images\smallEnemy\down\enemy1_down1.png').convert_alpha(),\
                        pygame.image.load(r'Images\smallEnemy\down\enemy1_down2.png').convert_alpha(),\
                        pygame.image.load(r'Images\smallEnemy\down\enemy1_down3.png').convert_alpha(),\
                        pygame.image.load(r'Images\smallEnemy\down\enemy1_down4.png').convert_alpha()\
        ])

        # 背景大小
        self.bg_width, self.bg_height = bg_size[0], bg_size[1]
        
        # 图片应该显示的位置信息和大小
        self.rect = self.image_fly.get_rect()
        
        self.rect.left = random.randint(0, self.bg_width - self.rect.width)
        self.rect.top  = random.randint(-5 * self.bg_height, 0)
        
        # 飞机控制时候移动速度
        self.speed = 2
        # 飞机是否存活
        self.active = True
        # 完美碰撞检测的mask
        self.mask = pygame.mask.from_surface(self.image_fly)

    def move(self):
        if self.rect.top < self.bg_height:
            self.rect.top += self.speed
        else:
            self.reset()  # 我觉得应该把自己删除就好了，不应该重置位子

    def reset(self):
        self.active = True
        self.rect.left = random.randint(0, self.bg_width - self.rect.width)
        self.rect.top = random.randint(-5 * self.bg_height, 0)


class MidEnemy(pygame.sprite.Sprite):
    energy = 8

    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)
        # 图片
        self.image_fly   = pygame.image.load(r'Images\midEnemy\fly\MidEnemy.png').convert_alpha()
        self.image_hit = pygame.image.load(r'Images\midEnemy\underattack\MidEnemyUnderattack.png').convert_alpha()
        self.image_destroy = []
        self.image_destroy.extend([\
                    pygame.image.load(r'Images\midEnemy\down\MidEnemyDown_1.png').convert_alpha(),\
                    pygame.image.load(r'Images\midEnemy\down\MidEnemyDown_2.png').convert_alpha(),\
                    pygame.image.load(r'Images\midEnemy\down\MidEnemyDown_3.png').convert_alpha(),\
                    pygame.image.load(r'Images\midEnemy\down\MidEnemyDown_4.png').convert_alpha()\
        ])

        # 背景大小
        self.bg_width, self.bg_height = bg_size[0], bg_size[1]
        
        # 图片应该显示的位置信息和大小
        self.rect = self.image_fly.get_rect()
        
        self.rect.left = random.randint(0, self.bg_width - self.rect.width)
        self.rect.top  = random.randint(-5 * self.bg_height, -self.bg_height)
        
        # 飞机控制时候移动速度
        self.speed = 1
        # 飞机是否存活
        self.active = True
        # 完美碰撞检测的mask
        self.mask = pygame.mask.from_surface(self.image_fly)
        self.energy = MidEnemy.energy
        self.hit = False
        
    def move(self):
        if self.rect.top < self.bg_height:
            self.rect.top += self.speed
        else:
            self.reset()  # 我觉得应该把自己删除就好了，不应该重置位子

    def reset(self):
        self.energy = MidEnemy.energy
        self.active = True
        self.rect.left = random.randint(0, self.bg_width - self.rect.width)
        self.rect.top  = random.randint(-5 * self.bg_height, -self.bg_height)


class BigEnemy(pygame.sprite.Sprite):
    energy = 20

    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)
        # 图片
        self.image_fly1 = pygame.image.load(r'Images\bigEnemy\fly\BigEnemy_1.png').convert_alpha()
        self.image_fly2 = pygame.image.load(r'Images\bigEnemy\fly\BigEnemy_2.png').convert_alpha()
        self.image_hit = pygame.image.load(r'Images\bigEnemy\underattack\BigEnemyUnderattack.png').convert_alpha()
        self.image_destroy = []
        self.image_destroy.extend([\
                    pygame.image.load(r'Images\bigEnemy\down\BigEnemyDown_1.png').convert_alpha(),\
                    pygame.image.load(r'Images\bigEnemy\down\BigEnemyDown_2.png').convert_alpha(),\
                    pygame.image.load(r'Images\bigEnemy\down\BigEnemyDown_3.png').convert_alpha(),\
                    pygame.image.load(r'Images\bigEnemy\down\BigEnemyDown_4.png').convert_alpha(),\
                    pygame.image.load(r'Images\bigEnemy\down\BigEnemyDown_5.png').convert_alpha(),\
                    pygame.image.load(r'Images\bigEnemy\down\BigEnemyDown_6.png').convert_alpha()\
        ])

        # 背景大小
        self.bg_width, self.bg_height = bg_size[0], bg_size[1]
        
        # 图片应该显示的位置信息和大小
        self.rect = self.image_fly1.get_rect()
        
        self.rect.left = random.randint(0, self.bg_width - self.rect.width)
        self.rect.top  = random.randint(-15 * self.bg_height, -5 * self.bg_height)
        
        # 飞机控制时候移动速度
        self.speed = 1
        # 飞机是否存活
        self.active = True
        # 完美碰撞检测的mask
        self.mask = pygame.mask.from_surface(self.image_fly1)
        self.energy = BigEnemy.energy
        self.hit = False
        
    def move(self):
        if self.rect.top < self.bg_height:
            self.rect.top += self.speed
        else:
            self.reset()  # 我觉得应该把自己删除就好了，不应该重置位子

    def reset(self):
        self.energy = BigEnemy.energy
        self.active = True
        self.rect.left = random.randint(0, self.bg_width - self.rect.width)
        self.rect.top  = random.randint(-15 * self.bg_height, -5 * self.bg_height)


