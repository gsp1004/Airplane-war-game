# 需要改善的地方
'''
1.所有的计时器都需要获取剩余时间，否则暂停会引起很多问题 bug
2.飞机无敌期间显示应该是闪烁的， 解决了

'''
import pygame
from pygame.locals import *
import sys
import traceback
import random
import os

import myplane
import enemy
import bullet
import supply
pygame.init()
pygame.mixer.init()

#颜色宏定义
BLACK = (0,  0,  0)
GREEN = (0,  255,  0)
RED = (255,  0,  0)
WHITE = (255, 255, 255)

# 加载背景图片
background = pygame.image.load(r'images\surface\background.png')
temp = background.get_rect()
bg_size = width,  height = temp.width, temp.height

# 设置界面
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption('plane')

# 加载音乐
# BGM
pygame.mixer.music.load(r'sound\bgm\bgm.mp3')
pygame.mixer.music.set_volume(0.2)

# 炸弹音效
bombSound = pygame.mixer.Sound(r'sound\bomb\bomb.wav')
bombSound.set_volume(0.2)

# 子弹射击音效
bulletSound = pygame.mixer.Sound(r'sound\bullet\bullet.wav')
bulletSound.set_volume(0.1)

# 大型敌方飞机
bigEnemyFlySound = pygame.mixer.Sound(r'sound\enemy\BigEnemyOut.wav')
bigEnemyFlySound.set_volume(0.2)

bigEnemyDownSound = pygame.mixer.Sound(r'sound\enemy\BigEnemyDown.wav')
bigEnemyDownSound.set_volume(0.2)

# 中型敌方飞机
midEnemyFlySound = pygame.mixer.Sound(r'sound\enemy\MidEnemyOut.wav')
midEnemyFlySound.set_volume(0.2)

midEnemyDownSound = pygame.mixer.Sound(r'sound\enemy\MidEnemyDown.wav')
midEnemyDownSound.set_volume(0.2)

# 小飞机
smallEnemyDownSound = pygame.mixer.Sound(r'sound\enemy\SmallEnemyDown.wav')
smallEnemyDownSound.set_volume(0.2)

# 主角坠毁音效
heroDownSound = pygame.mixer.Sound(r'sound\hero\hero_down.wav')
heroDownSound.set_volume(0.2)

# 补给音效
supplyBombSound = pygame.mixer.Sound(r'sound\supply\supply_bomb.wav')
supplyBombSound.set_volume(0.2)

supplyBulletSound = pygame.mixer.Sound(r'sound\supply\supply_bullet.wav')
supplyBulletSound.set_volume(0.2)


def add_small_enemies(group, group_all, num):
    for i in range(num):
        e1 = enemy.SmallEnemy(bg_size)
        group_all.add(e1)
        group.add(e1)


def add_mid_enemies(group, group_all, num):
    for i in range(num):
        e1 = enemy.MidEnemy(bg_size)
        group_all.add(e1)
        group.add(e1)


def add_big_enemies(group, group_all, num):
    for i in range(num):
        e1 = enemy.BigEnemy(bg_size)
        group_all.add(e1)
        group.add(e1)


def speed_up(target, increase):
    for each in target:
        each.speed += increase


def main():
    # 重新开始和结束游戏的图片
    image_restart = pygame.image.load(r'Images/surface/game_again.png').convert_alpha()
    image_restart_rect = image_restart.get_rect()
    image_restart_rect.center = (width // 2, height // 2 + 20)

    image_over = pygame.image.load(r'Images/surface/game_over.png').convert_alpha()
    image_over_rect = image_over.get_rect()
    image_over_rect.center = (width // 2, height // 2 + 80)

    # 控制帧率
    clock = pygame.time.Clock()

    while True:

        # 播放bgm
        pygame.mixer.music.play(-1)

        # 中弹图片索引值
        big_enemy_down_index = 0
        mid_enemy_down_index = 0
        small_enemy_down_index = 0
        hero_down_index = 0

        # 保存得分变量
        score = 0
        score_font = pygame.font.SysFont(name='方正舒体', size=50)

        # 标志是否暂停游戏
        pause = False
        pause_nor_image = pygame.image.load(r'Images/surface/game_pause_nor.png').convert_alpha()
        pause_pressed_image = pygame.image.load(r'Images/surface/game_pause_pressed.png').convert_alpha()
        resume_nor_image = pygame.image.load(r'Images/surface/game_resume_nor.png').convert_alpha()
        resume_pressed_image = pygame.image.load(r'Images/surface/game_resume_pressed.png').convert_alpha()
        pause_rect = pause_nor_image.get_rect()
        pause_rect.left, pause_rect.top = width - pause_rect.width - 10, 10
        pause_image = pause_nor_image

        # 用于限制重复打开记录文件
        is_recorded = False

        # 游戏难度级别
        level = 1

        # 全屏炸弹
        bomb_image = pygame.image.load(r'Images/bomb/bomb.png').convert_alpha()
        bomb_rect = bomb_image.get_rect()
        bomb_font = pygame.font.SysFont(name='方正舒体', size=60)
        bomb_num = 3

        # 每30s 提供一个补给包
        supply_bomb = supply.SupplyBomb(bg_size)
        supply_bullet = supply.SupplyBullet(bg_size)
        SUPPLY_TIMER = USEREVENT
        # supply_remain_time = 30 * 1000
        pygame.time.set_timer(SUPPLY_TIMER, 30 * 1000)
        # supply_timer_restart = pygame.time.get_ticks()

        # 超级子弹
        BULLET_SUPER_TIMER = USEREVENT + 1
        # 标志是否使用超级子弹
        is_bullet_super = False

        # 解除我方无敌计时器
        GOD_TIMER = USEREVENT + 2

        # 初始化我的飞机
        hero = myplane.Myplane(bg_size)

        # 生成普通子弹
        bullet_common = []
        bullet_common_index = 0
        BULLET_COMMON_NUM = 4
        for i in range(BULLET_COMMON_NUM):
            bullet_common.append(bullet.BulletCommon(hero.rect.midtop))

        # 生成超级子弹
        bullet_super = []
        bullet_super_index = 0
        BULLET_SUPER_NUM = 8
        for i in range(BULLET_SUPER_NUM // 2):
            bullet_super.append(bullet.BulletSuper((hero.rect.centerx - 33, hero.rect.centery)))
            bullet_super.append(bullet.BulletSuper((hero.rect.centerx + 30, hero.rect.centery)))

        # 生成敌方飞机，保存在这个组里面
        enemies = pygame.sprite.Group()

        # 初始生成小 15 中 4 大 2
        # 生成小飞机
        small_enemies = pygame.sprite.Group()
        add_small_enemies(small_enemies, enemies, 15)

        # 生成中型飞机
        mid_enemies = pygame.sprite.Group()
        add_mid_enemies(mid_enemies, enemies, 4)

        # 生成大型飞机
        big_enemies = pygame.sprite.Group()
        add_big_enemies(big_enemies, enemies, 2)

        # 屏幕中大型敌方飞机数量
        big_enemy_num = 0

        running = True
        count = 100
        switch_image = True  # 这个变量用于表现飞机喷气效果

        # 超级子弹剩余时间
        # super_bullet_remain_time = 0

        # 还有多少条命
        life_num = 3  # gsp@
        life_image = pygame.image.load(r'Images/hero/fly/hero_icon.png')
        life_rect = life_image.get_rect()

        while running:
            # 所有事件监测
            for event in pygame.event.get():
                # 检测退出
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                # 事件为鼠标按下按键
                elif event.type == MOUSEBUTTONDOWN:
                    # 响应用户点击暂停按键的事件，在图标区域内并且按下左键
                    if event.button == 1 and pause_rect.collidepoint(event.pos):
                        # 选择应该画的暂停图片
                        if pause:  # 如果当前状态是pause，那么用户按下后就应该继续游戏，图标应该是暂停的样式
                            pause_image = pause_pressed_image
                        else:
                            pause_image = resume_pressed_image

                        # 响应用户的按键操作
                        pause = not pause

                        # 暂停声音,停止计时器
                        if pause:
                            # 补给计时器停止
                            # supply_remain_time -= (pygame.time.get_ticks() - supply_timer_restart)
                            pygame.time.set_timer(SUPPLY_TIMER, 0)
                            '''
                            # 如果补给剩余时间为0或者负数，表示应该投放补给了
                            if supply_remain_time <= 0:
                                print('ATTENTION: supply_remain_time = %d' % supply_remain_time)
                                supply_remain_time = 1
                            '''

                            # 超级子弹计时器停止
                            if is_bullet_super:
                                pygame.time.set_timer(BULLET_SUPER_TIMER, 0)
                            '''
                            #   如果超级子弹还有时间，证明需要结算它的剩余时间
                            if super_bullet_remain_time:
                                pygame.time.set_timer(BULLET_SUPER_TIMER, 0)
                                super_bullet_remain_time -= (pygame.time.get_ticks() - super_bullet_timer_restart)
                                # 如果发现实际剩余时间为负数，表示已经没有超级时间了，需要取消超级子弹时间
                                if super_bullet_remain_time <= 0:
                                    print('ATTENTION: super_bullet_remain_time = %d' % super_bullet_remain_time)
                                    super_bullet_remain_time = 0
                                    is_bullet_super = False
                            '''
                            pygame.mixer.music.pause()
                            pygame.mixer.pause()

                        # 重启剩余，重启所有计时器
                        else:
                            # 重启补给包计时器
                            # supply_timer_restart = pygame.time.get_ticks()
                            # pygame.time.set_timer(SUPPLY_TIMER, supply_remain_time)
                            pygame.time.set_timer(SUPPLY_TIMER, 30 * 1000)

                            # 重启超级子弹计时器
                            if is_bullet_super:
                                pygame.time.set_timer(BULLET_SUPER_TIMER, 18 * 1000)
                            '''
                            if super_bullet_remain_time:
                                super_bullet_timer_restart = pygame.time.get_ticks()
                                pygame.time.set_timer(SUPPLY_TIMER, super_bullet_remain_time)
                            '''

                            pygame.mixer.music.unpause()
                            pygame.mixer.unpause()

                    # 关闭游戏
                    elif event.button == 1 and image_over_rect.collidepoint(event.pos):
                        pygame.quit()

                    elif event.button == 1 and image_restart_rect.collidepoint(event.pos):
                        running = False
                        break

                # 鼠标移动到暂停键哪里，需要变颜色
                elif event.type == MOUSEMOTION:
                    if pause_rect.collidepoint(event.pos):
                        if pause:
                            pause_image = resume_pressed_image
                        else:
                            pause_image = pause_pressed_image
                    else:
                        if pause:
                            pause_image = resume_nor_image
                        else:
                            pause_image = pause_nor_image

                # 按下空格丢炸弹
                elif event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        if bomb_num:
                            bomb_num -= 1
                            bombSound.play()
                            for each in enemies:
                                if each.rect.bottom > 0:
                                    each.active = False

                # 补给包投放定时器触发事件
                elif event.type == SUPPLY_TIMER:
                    # supply_timer_restart = pygame.time.get_ticks()
                    # supply_remain_time = 30 * 1000
                    # 播放补给包声音，待添加，gsp@
                    if random.choice([True, False]):
                        supply_bomb.reset()
                    else:
                        supply_bullet.reset()

                # 通知关闭超级子弹，18秒已过
                elif event.type == BULLET_SUPER_TIMER:
                    is_bullet_super = False
                    # super_bullet_remain_time = 0
                    # pygame.time.set_timer(BULLET_SUPER_TIMER, 0)

                elif event.type == GOD_TIMER:
                    hero.god = False
                    pygame.time.set_timer(GOD_TIMER, 0)

            # 等级难度设置
            # 难度2：增加3个小机，2个中飞机，1个大型机，小飞机加速1
            if level == 1 and score > 50000:
                level = 2
                #增加3个小机，2个中飞机，1个大型机
                add_small_enemies(small_enemies, enemies, 3)
                add_mid_enemies(mid_enemies, enemies, 2)
                add_big_enemies(big_enemies, enemies, 1)
                #提升小飞机速度
                speed_up(small_enemies,1)
            # 难度3：增加4个小机，3个中飞机，1个大型机，中飞机加速1
            elif level == 2 and score > 300000:
                level = 3
                # 增加4个小机，3个中飞机，1个大型机
                add_small_enemies(small_enemies, enemies, 4)
                add_mid_enemies(mid_enemies, enemies, 3)
                add_big_enemies(big_enemies, enemies, 1)
                # 提升中飞机速度
                speed_up(mid_enemies, 1)
            # 难度4：增加5个小机，3个中飞机，2个大型机，小飞机加速1
            elif level == 3 and score > 600000:
                level = 4
                #增加5个小机，3个中飞机，2个大型机
                add_small_enemies(small_enemies, enemies, 5)
                add_mid_enemies(mid_enemies, enemies, 3)
                add_big_enemies(big_enemies, enemies, 2)
                #提升小飞机速度
                speed_up(small_enemies, 1)
            # 难度5：增加5个小机，3个中飞机，2个大型机，小飞机加速1，中飞机加速1
            elif level == 4 and score > 1000000:
                level = 5
                #增加5个小机，3个中飞机，2个大型机
                add_small_enemies(small_enemies, enemies, 5)
                add_mid_enemies(mid_enemies, enemies, 3)
                add_big_enemies(big_enemies, enemies, 2)
                #提升小飞机速度
                speed_up(small_enemies, 1)
                speed_up(mid_enemies, 1)

            # 绘制背景
            screen.blit(background, (0, 0))

            if not pause and life_num:
                # 喷气效果切换变量转换部分
                if not (count % 5):
                    switch_image = not switch_image

                # 检测用户的键盘操作控制飞机
                key_pressed = pygame.key.get_pressed()  # 获取所有按键的序列，按下为True
                if key_pressed[K_w] or key_pressed[K_UP]:
                    hero.moveUp()
                if key_pressed[K_s] or key_pressed[K_DOWN]:
                    hero.moveDown()
                if key_pressed[K_a] or key_pressed[K_LEFT]:
                    hero.moveLeft()
                if key_pressed[K_d] or key_pressed[K_RIGHT]:
                    hero.moveRight()

                # 此处开始绘制所有的图 #####################################################################################
                # 绘制补给包并且检测飞机是否获得
                if supply_bomb.active:
                    supply_bomb.move()
                    screen.blit(supply_bomb.image, supply_bomb.rect)
                    # 碰撞检测
                    if pygame.sprite.collide_mask(supply_bomb, hero):
                        supply_bomb.active = False
                        # 播放获得补给声音 gsp@
                        if bomb_num < 3:
                            bomb_num += 1

                # 绘制补给包并且检测飞机是否获得
                if supply_bullet.active:
                    supply_bullet.move()
                    screen.blit(supply_bullet.image, supply_bullet.rect)
                    # 碰撞检测
                    if pygame.sprite.collide_mask(supply_bullet, hero):
                        supply_bullet.active = False
                        # 播放获得补给声音 gsp@
                        is_bullet_super = True
                        # super_bullet_remain_time = 18 * 1000
                        # pygame.time.set_timer(BULLET_SUPER_TIMER, 0)
                        pygame.time.set_timer(BULLET_SUPER_TIMER, 18 * 1000)
                        # super_bullet_timer_restart = pygame.time.get_ticks()

                # 每10帧绘制一个子弹
                if not (count % 10):
                    # 播放子弹声音
                    # 超级子弹
                    if is_bullet_super:
                        bullets = bullet_super
                        bullets[bullet_super_index].reset((hero.rect.centerx - 33, hero.rect.centery))
                        bullets[bullet_super_index + 1].reset((hero.rect.centerx + 30, hero.rect.centery))
                        bullet_super_index = (bullet_super_index + 2) % BULLET_SUPER_NUM

                    else:
                        bullets = bullet_common
                        bullets[bullet_common_index].reset(hero.rect.midtop)
                        bullet_common_index = (bullet_common_index + 1) % BULLET_COMMON_NUM

                # 检测子弹是否击中敌方飞机
                for b in bullets:
                    if b.active:
                        # bulletSound.play()
                        b.move()
                        screen.blit(b.image, b.rect)
                        enemy_hit = pygame.sprite.spritecollide(b, enemies, False, pygame.sprite.collide_mask)
                        if enemy_hit:
                            b.active = False
                            for e in enemy_hit:
                                if e in mid_enemies or e in big_enemies:
                                    e.hit = True
                                    e.energy -= 1
                                    if e.energy == 0:
                                        e.active = False
                                else:
                                    e.active = False

                # 绘制敌方大型机
                for each in big_enemies:
                    if each.active:
                        each.move()
                        if each.hit:
                            # 绘制hit特效
                            screen.blit(each.image_hit, each.rect)
                            each.hit = False
                        else:
                            # 喷气动画切换
                            if switch_image:
                                screen.blit(each.image_fly1, each.rect)
                            else:
                                screen.blit(each.image_fly2, each.rect)

                        # 绘制血槽, 黑色作为底槽
                        pygame.draw.line(screen, BLACK,\
                                         (each.rect.left, each.rect.top - 5),\
                                         (each.rect.right, each.rect.top - 5),\
                                         2)
                        # 生命值大于20%显示绿色
                        energy_ratio = each.energy/enemy.BigEnemy.energy
                        if energy_ratio > 0.2:
                            energy_color = GREEN
                        else:
                            energy_color = RED
                        pygame.draw.line(screen, energy_color,\
                                         (each.rect.left, each.rect.top - 5),\
                                         (each.rect.left + each.rect.width * energy_ratio, each.rect.top - 5),\
                                         2)

                        # 播放声音
                        if each.rect.bottom == - 50:
                            big_enemy_num += 1
                            print('1 create\t\t', big_enemy_num)
                            # 播放大型机到来声音
                            bigEnemyFlySound.play(-1)
                        # 停止播放飞机声音
                        elif each.rect.top == each.bg_height - 50:
                            big_enemy_num -= 1
                            print('2 ------\t\t', big_enemy_num)
                            if big_enemy_num == 0:
                                print('3 num==0\t\t', big_enemy_num)
                                bigEnemyFlySound.stop()
                    else:
                        # 毁灭
                        if not (count % 3):
                            if big_enemy_down_index == 0:
                                bigEnemyDownSound.play()
                                big_enemy_num -= 1
                                print('4 destroy\t\t', big_enemy_num)
                                if big_enemy_num == 0:
                                    bigEnemyFlySound.stop()
                            screen.blit(each.image_destroy[big_enemy_down_index], each.rect)
                            big_enemy_down_index = (big_enemy_down_index + 1) % 6
                            if big_enemy_down_index == 0:
                                score += 10000
                                each.reset()

                # 绘制敌方中型机
                for each in mid_enemies:
                    if each.active:
                        each.move()

                        if each.hit:
                            # 绘制hit特效
                            screen.blit(each.image_hit, each.rect)
                            each.hit = False
                        else:
                            screen.blit(each.image_fly, each.rect)

                        if each.rect.bottom == -50:
                            # 播放型机到来声音
                            midEnemyFlySound.play()

                        # 绘制血槽, 黑色作为底槽
                        pygame.draw.line(screen, BLACK,\
                                         (each.rect.left, each.rect.top - 5),\
                                         (each.rect.right, each.rect.top - 5),\
                                         2)
                        # 生命值大于20%显示绿色
                        energy_ratio = each.energy/enemy.MidEnemy.energy
                        if energy_ratio > 0.2:
                            energy_color = GREEN
                        else:
                            energy_color = RED
                        pygame.draw.line(screen, energy_color,\
                                         (each.rect.left, each.rect.top - 5),\
                                         (each.rect.left + each.rect.width * energy_ratio, each.rect.top - 5),\
                                         2)
                    else:
                        # 毁灭
                        if not (count % 3):
                            if mid_enemy_down_index == 0:
                                midEnemyDownSound.play()
                            screen.blit(each.image_destroy[mid_enemy_down_index], each.rect)
                            mid_enemy_down_index = (mid_enemy_down_index + 1) % 4
                            if mid_enemy_down_index == 0:
                                score += 4000
                                each.reset()

                # 绘制敌方小型机
                for each in small_enemies:
                    if each.active:
                        each.move()
                        screen.blit(each.image_fly, each.rect)
                    else:
                        # 毁灭
                        if not (count % 3):
                            if small_enemy_down_index == 0:
                                smallEnemyDownSound.play()
                            screen.blit(each.image_destroy[small_enemy_down_index], each.rect)
                            small_enemy_down_index = (small_enemy_down_index + 1) % 4
                            if small_enemy_down_index == 0:
                                score += 1000
                                each.reset()

                # 我们和敌机的碰撞检测
                enemies_down = pygame.sprite.spritecollide(hero, enemies, False, pygame.sprite.collide_mask)
                if enemies_down and not hero.god:
                    hero.active = False
                    for e in enemies_down:
                        e.active = False

                # 绘制我方飞机
                if hero.active:
                    if switch_image:
                        screen.blit(hero.image1, (hero.rect.left, hero.rect.top))
                    else:
                        if not hero.god:
                            screen.blit(hero.image2, (hero.rect.left, hero.rect.top))
                        else:
                            screen.blit(hero.image_god, (hero.rect.left, hero.rect.top))
                else:
                    # 毁灭
                    heroDownSound.play()
                    if not (count % 3):
                        screen.blit(hero.image_destroy[hero_down_index], hero.rect)
                        hero_down_index = (hero_down_index + 1) % 4
                        if hero_down_index == 0:
                            life_num -= 1
                            if not life_num:
                                # game over
                                pass
                            else:
                                hero.reset()
                                pygame.time.set_timer(GOD_TIMER, 3000)

                #左下角绘制炸弹
                bomb_text = bomb_font.render('X %d' % bomb_num, True, WHITE)
                screen.blit(bomb_image, (10, height - 5 - bomb_rect.height))
                screen.blit(bomb_text, (20 + bomb_rect.width, height - 15 - bomb_rect.height))

                # 右下角绘制剩余生命数量
                if life_num:
                    for i in range(life_num):
                        screen.blit(life_image,\
                                    (width - 10 - (i + 1) * life_rect.width,\
                                     height - 10 - life_rect.height)\
                                    )

                # count自减一和重置部分
                count -= 1
                if not count:
                    count = 100
            # game over
            elif life_num == 0:
                # 这里面的部分只执行一次
                if not is_recorded:
                    is_recorded = True

                    # 背景音乐停止
                    pygame.mixer.music.stop()
                    # 停止全部音效
                    pygame.mixer.stop()
                    # 停止发放补给
                    pygame.time.set_timer(SUPPLY_TIMER, 0)

                    # 获取历史最高分并且保存在record.txt 中
                    # 如果不存在，就创建，并且在里面存一个0
                    if not os.path.isfile('record.txt'):
                        with open('record.txt', 'w') as t:
                            t.write('0')
                            t.close()

                    with open('record.txt', 'r+') as f:
                        temp_score_str = f.read()

                        # 是否为十进制字符串
                        if temp_score_str.isdecimal():
                            highest_score = int(temp_score_str)
                        else:
                            print('ERROR:record.txt中的内容为：%s' % temp_score_str)
                            highest_score = 0

                        if score > highest_score:
                            highest_score = score
                            f.seek(0, 0)
                            f.write(str(highest_score))

                    # 屏幕显示历史最高分的资源图片生成
                    highest_score_font = pygame.font.SysFont(name='方正舒体', size=58)
                    highest_score_text = highest_score_font.render('Best : %s' % str(highest_score), True, WHITE)

                    # Your score 字体和此次得分的字体
                    now_score_font = pygame.font.SysFont(name='方正舒体', size=68)
                    # Your Score 的资源图片生成
                    your_score = now_score_font.render('Your Score', True, WHITE)
                    your_score_rect = your_score.get_rect()
                    your_score_rect.center = (width // 2, height // 2 - 150)
                    # 此次得分的资源图片生成
                    score_text = now_score_font.render('%s' % str(score), True, WHITE)
                    score_text_rect = score_text.get_rect()
                    score_text_rect.center = (width // 2, height // 2 - 70)

                # 绘制历史最高分
                screen.blit(highest_score_text, (50, 30))
                # 屏幕显示Your Score
                screen.blit(your_score, your_score_rect)
                # 显示此次得分
                screen.blit(score_text, score_text_rect)
                # 绘制从新开始和结束游戏
                screen.blit(image_restart, image_restart_rect)
                screen.blit(image_over, image_over_rect)

            if life_num:
                #绘制分数
                score_text = score_font.render('Score : %s' % str(score), True, WHITE)
                screen.blit(score_text, (10, 5))

                #绘制暂停按钮
                screen.blit(pause_image, pause_rect)

            pygame.display.flip()

            clock.tick(60)

if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()
