import json
import os
import random
import pygame

from source import tools, setup
from .. import constants as c


class Enemy(pygame.sprite.Sprite):
    # Initial the enemy settings
    def __init__(self, name, player):
        super().__init__()
        self.name = name
        self.player = player
        self.load_data()
        self.setup_timers()
        self.x_vel = 0
        self.y_vel = 0

    # Load enemy's basic data from the json file
    # You can add other enemies info in the file named enemy.json
    # PLUS: the format of data storing must be the same
    def load_data(self):
        file_name = 'enemy.json'
        file_path = os.path.join('source/data/chars', file_name)
        with open(file_path) as f:
            self.enemies_data = json.load(f)

        # load basic parameter
        self.enemy_data = self.enemies_data[self.name]
        self.vel = self.enemy_data['vel']
        self.origin_health_point = self.enemy_data['health_point']
        self.health_point = self.enemy_data['health_point']
        self.damage = self.enemy_data['damage']

        # load image and animations
        frames = self.enemy_data['image_frames']
        die_frames = frames['die']
        self.die_sheet = setup.graphics[die_frames['image_source']]
        self.die_frames_save = []
        for frame in die_frames['pos']:
            self.die_frames_save.append((frame['x'], frame['y'], frame['width'], frame['height']))

        walk_frames = frames['walk']
        self.sheet = setup.graphics[walk_frames['image_source']]
        count = 0
        self.down_frames = []
        self.left_frames = []
        self.right_frames = []
        self.up_frames = []
        for frame in walk_frames['pos']:
            if count < 3:
                self.down_frames.append((frame['x'], frame['y'], frame['width'], frame['height']))
                count += 1
            elif count < 6:
                self.left_frames.append((frame['x'], frame['y'], frame['width'], frame['height']))
                count += 1
            elif count < 9:
                self.right_frames.append((frame['x'], frame['y'], frame['width'], frame['height']))
                count += 1
            elif count < 12:
                self.up_frames.append((frame['x'], frame['y'], frame['width'], frame['height']))
                count += 1
        self.frames = self.right_frames
        self.frame_index = 0
        self.image = tools.get_graphic(self.sheet, *self.frames[self.frame_index], (0, 0, 0), 1)
        self.rect = self.image.get_rect()

    # Set up different timers (obviously)
    def setup_timers(self):
        self.walking_timer = 0
        self.die_timer = 0

    # Set up the enemy's birth position
    # NEED TO IMPROVE
    def setup_enemy_pos(self, pos):
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        # print(self.rect.x, self.rect.y)

    # Show enemy's death animation
    def show_die_animation(self, surface):
        self.die_current = pygame.time.get_ticks()
        index = 0
        if self.die_current - self.die_timer > 1000:
            index = (self.frame_index + 1) % 3
        die_image = tools.get_graphic(self.die_sheet, *self.die_frames_save[index], (0, 0, 0), 1)
        surface.blit(die_image, self.rect)

    def draw_blood_bar(self, surface):
        blood = self.health_point / self.origin_health_point * c.EBLOODBAR_WIDTH
        pygame.draw.rect(surface, c.BLOOD_BACKGROUND, (self.rect.centerx - c.EBLOODBAR_WIDTH / 2, self.rect.y - 5,
                                                       c.EBLOODBAR_WIDTH, c.EBLOODBAR_HEIGHT), 0)
        pygame.draw.rect(surface, c.BLOOD_COLOR, (self.rect.centerx - c.EBLOODBAR_WIDTH / 2, self.rect.y - 5,
                                                  blood, c.EBLOODBAR_HEIGHT), 0)

    def update(self):
        if self.name == 'LAB_robot_B':
            self.vel = random.randint(3, 13)
        elif self.name == 'LAB_robot_R':
            self.damage = random.randint(9, 15)
        elif self.name == 'LAB_robot_W' and self.health_point < self.origin_health_point:
            self.health_point += 1

        self.current = pygame.time.get_ticks()
        x_distance = self.rect.x - self.player.rect.x
        y_distance = self.rect.y - self.player.rect.y

        # make player be enemy's target
        # NEED TO IMPROVE
        if abs(x_distance) >= abs(y_distance) and x_distance < 0:
            self.x_vel = self.vel
            self.y_vel = 0
            self.frames = self.right_frames
            self.face = 'right'
        if abs(x_distance) >= abs(y_distance) and x_distance >= 0:
            self.x_vel = -1 * self.vel
            self.y_vel = 0
            self.frames = self.left_frames
            self.face = 'left'
        if abs(x_distance) < abs(y_distance) and y_distance < 0:
            self.x_vel = 0
            self.y_vel = self.vel
            self.frames = self.down_frames
            self.face = 'down'
        if abs(x_distance) < abs(y_distance) and y_distance >= 0:
            self.x_vel = 0
            self.y_vel = -1 * self.vel
            self.frames = self.up_frames
            self.face = 'up'

        # Change frames to imitate walking animations
        if self.current - self.walking_timer > 100:
            self.frame_index = (self.frame_index + 1) % 3
        self.image = tools.get_graphic(self.sheet, *self.frames[self.frame_index], (0, 0, 0), 1)