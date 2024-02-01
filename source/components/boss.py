import random

import pygame

from source import setup, tools
from .. import constants as c

class Boss1(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.setup_timers()
        self.load_data()

    def setup_timers(self):
        self.animation_timer = 0

    def load_data(self):
        # load image
        self.sheet = setup.graphics['Boss']
        self.frames = [(0, 96, 96, 96),
                       (96, 96, 96, 96),
                       (192, 96, 96, 96)]
        self.frame_index = 0
        self.image = tools.get_graphic(self.sheet, *self.frames[self.frame_index], (0, 0, 0), 1)
        self.rect = self.image.get_rect()
        self.rect.x = self.pos_x
        self.rect.y = self.pos_y

        # load parameters
        self.origin_health_point = 150
        self.health_point = 150

    def draw_blood_bar(self, surface):
        blood = self.health_point / self.origin_health_point * c.BOSS_WIDTH_1
        pygame.draw.rect(surface, c.BLOOD_BACKGROUND, (self.rect.centerx - c.BOSS_WIDTH_1 / 2, self.rect.y - 10,
                                                       c.BOSS_WIDTH_1, c.BOSS_HEIGHT_1), 0)
        pygame.draw.rect(surface, c.BLOOD_COLOR, (self.rect.centerx - c.BOSS_WIDTH_1 / 2, self.rect.y - 10,
                                                  blood, c.BOSS_HEIGHT_1), 0)

    def update(self):
        self.current = pygame.time.get_ticks()
        if self.current - self.animation_timer > 100:
            self.frame_index = (self.frame_index + 1) % 3
        self.image = tools.get_graphic(self.sheet, *self.frames[self.frame_index], (0, 0, 0), 1)


class Boss1Weapon(pygame.sprite.Sprite):
    def __init__(self, player, pos_x, pos_y):
        super().__init__()
        self.player = player
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.x_vel = 0
        self.y_vel = 0
        self.load_data()

    def load_data(self):
        self.sheet = setup.graphics['animation_items2']
        self.frame_index = 0
        self.frames = [(432, 192, 48, 48),
                       (432, 240, 48, 48),
                       (432, 288, 48, 48),
                       (432, 336, 48, 48)]
        self.image = tools.get_graphic(self.sheet, *self.frames[self.frame_index], (0, 0, 0), 1)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.pos_x
        self.rect.centery = self.pos_y

        self.animation_timer = 0
        self.damage = 1
        self.vel = 20

    def update(self):
        x_distance = self.rect.x - self.player.rect.x
        y_distance = self.rect.y - self.player.rect.y
        if abs(x_distance) >= abs(y_distance) and x_distance < 0:
            self.x_vel = self.vel
            self.y_vel = 0
        if abs(x_distance) >= abs(y_distance) and x_distance >= 0:
            self.x_vel = -1 * self.vel
            self.y_vel = 0
        if abs(x_distance) < abs(y_distance) and y_distance < 0:
            self.x_vel = 0
            self.y_vel = self.vel
        if abs(x_distance) < abs(y_distance) and y_distance >= 0:
            self.x_vel = 0
            self.y_vel = -1 * self.vel
        self.current = pygame.time.get_ticks()
        if self.current - self.animation_timer > 100:
            self.frame_index = (self.frame_index + 1) % 4
        self.image = tools.get_graphic(self.sheet, *self.frames[self.frame_index], (0, 0, 0), 1)


class Boss2(Boss1):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x=pos_x, pos_y=pos_y)
        self.setup_timers()
        self.load_data()

    def load_data(self):
        # load image
        self.sheet = setup.graphics['Boss']
        self.frames = [(0, 0, 96, 96),
                       (96, 0, 96, 96),
                       (192, 0, 96, 96)]
        self.frame_index = 0
        self.image = tools.get_graphic(self.sheet, *self.frames[self.frame_index], (0, 0, 0), 1)
        self.rect = self.image.get_rect()
        self.rect.x = self.pos_x
        self.rect.y = self.pos_y

        # load parameters
        self.origin_health_point = 200
        self.health_point = 200


class Boss2Weapon(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.random_birth()
        self.load_data()

    def load_data(self):
        self.sheet = setup.graphics['Enemys2']
        self.frame_index = 0
        self.image = tools.get_graphic(self.sheet, *self.frames[self.frame_index], (0, 0, 0), 1)
        self.rect = self.image.get_rect()
        self.rect.x = self.pos_x
        self.rect.y = self.pos_y

        self.animation_timer = 0
        self.vel = 30
        self.damage = 25

    def random_birth(self):
        self.side = random.randint(1, 4)
        if self.side == 1:  # face down
            self.frames = [(288, 0, 48, 48),
                           (336, 0, 48, 48),
                           (384, 0, 48, 48)]
            self.pos_x = random.randint(0, c.SCREEN_WIDTH-48)
            self.pos_y = 0
        elif self.side == 2:  # face left
            self.frames = [(288, 48, 48, 48),
                           (336, 48, 48, 48),
                           (384, 48, 48, 48)]
            self.pos_x = c.SCREEN_WIDTH-48
            self.pos_y = random.randint(0, c.SCREEN_HEIGHT-48)
        elif self.side == 3:  # face right
            self.frames = [(288, 96, 48, 48),
                           (336, 96, 48, 48),
                           (384, 96, 48, 48)]
            self.pos_x = 0
            self.pos_y = random.randint(0, c.SCREEN_HEIGHT - 48)
        elif self.side == 4: # face up
            self.frames = [(288, 144, 48, 48),
                           (336, 144, 48, 48),
                           (384, 144, 48, 48)]
            self.pos_x = random.randint(0, c.SCREEN_WIDTH-48)
            self.pos_y = c.SCREEN_HEIGHT-48

    def update(self):
        self.current = pygame.time.get_ticks()
        if self.current - self.animation_timer > 100:
            self.frame_index = (self.frame_index + 1) % 3
        self.image = tools.get_graphic(self.sheet, *self.frames[self.frame_index], (0, 0, 0), 1)


class Boss3(Boss1):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x=pos_x, pos_y=pos_y)
        self.setup_timers()
        self.load_data()

    def load_data(self):
        # load image
        self.sheet = setup.graphics['Boss']
        self.frames = [(0, 192, 96, 96),
                       (96, 192, 96, 96),
                       (192, 192, 96, 96)]
        self.frame_index = 0
        self.image = tools.get_graphic(self.sheet, *self.frames[self.frame_index], (0, 0, 0), 1)
        self.rect = self.image.get_rect()
        self.rect.x = self.pos_x
        self.rect.y = self.pos_y

        # load parameters
        self.origin_health_point = 170
        self.health_point = 170
        self.damage = 1


class Boss4(Boss1):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x=pos_x, pos_y=pos_y)
        self.life = 1
        self.setup_timers()
        self.load_data()

    def load_data(self):
        # load image
        self.sheet = setup.graphics['Boss']
        self.frames = [(0, 288, 96, 96),
                       (96, 288, 96, 96),
                       (192, 288, 96, 96)]
        self.frame_index = 0
        self.image = tools.get_graphic(self.sheet, *self.frames[self.frame_index], (0, 0, 0), 1)
        self.rect = self.image.get_rect()
        self.rect.x = self.pos_x
        self.rect.y = self.pos_y

        # load parameters
        self.origin_health_point = 50
        self.health_point = 50


class Boss4Weapon(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, toward):
        super().__init__()
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.toward = toward
        self.load_data()

    def load_data(self):
        self.sheet = setup.graphics['animation_items']
        self.frames = [(432, 0, 48, 96),
                       (480, 0, 48, 96),
                       (528, 0, 48, 96)]
        self.frame_index = 0
        self.image = tools.get_graphic(self.sheet, *self.frames[self.frame_index], (0, 0, 0), 1)
        self.rect = self.image.get_rect()
        self.rect.x = self.pos_x
        self.rect.y = self.pos_y

        self.animation_timer = 0
        self.vel = 30
        self.damage = 45

    def update(self):
        self.current = pygame.time.get_ticks()
        if self.current - self.animation_timer > 100:
            self.frame_index = (self.frame_index + 1) % 3
        if self.toward == 'down':
            self.image = tools.get_graphic(self.sheet, *self.frames[self.frame_index], (0, 0, 0), 1)
        elif self.toward == 'up':
            self.image = pygame.transform.rotate(
                tools.get_graphic(self.sheet, *self.frames[self.frame_index], (0, 0, 0), 1), 180)
        elif self.toward == 'left':
            self.image = pygame.transform.rotate(
                tools.get_graphic(self.sheet, *self.frames[self.frame_index], (0, 0, 0), 1), 270)
        elif self.toward == 'right':
            self.image = pygame.transform.rotate(
                tools.get_graphic(self.sheet, *self.frames[self.frame_index], (0, 0, 0), 1), 90)


class BossFinal(Boss1):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x=pos_x, pos_y=pos_y)
        self.setup_timers()
        self.load_data()

    def load_data(self):
        # load image
        self.sheet = setup.graphics['Boss2']
        self.frames = [(0, 120, 120, 120),
                       (120, 120, 120, 120),
                       (240, 120, 120, 120)]
        self.frame_index = 0
        self.image = tools.get_graphic(self.sheet, *self.frames[self.frame_index], (0, 0, 0), 1)
        self.rect = self.image.get_rect()
        self.rect.x = self.pos_x
        self.rect.y = self.pos_y

        # load parameters
        self.origin_health_point = 600
        self.health_point = 600

    def draw_blood_bar(self, surface):
        blood = self.health_point / self.origin_health_point * c.BOSS_WIDTH_2
        pygame.draw.rect(surface, c.BLOOD_BACKGROUND, (self.rect.centerx - c.BOSS_WIDTH_2 / 2, self.rect.y - 15,
                                                       c.BOSS_WIDTH_2, c.BOSS_HEIGHT_2), 0)
        pygame.draw.rect(surface, c.BLOOD_COLOR, (self.rect.centerx - c.BOSS_WIDTH_2 / 2, self.rect.y - 15,
                                                  blood, c.BOSS_HEIGHT_2), 0)