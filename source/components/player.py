import pygame
import json
import os

from source import setup, tools
from . import sound
from .. import constants as c
from .. import functions


class Player(pygame.sprite.Sprite):
    # Initial player settings here
    def __init__(self, name):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.face = 'right'
        self.load_data()
        self.setup_states()
        self.setup_velocity()
        self.setup_timers()
        self.load_images()

    # Load player basic data from the json file
    # You can add some parameters in the file named player.json
    # Use the rigour same format
    # Three characters' parameters need to be modified at the same time
    def load_data(self):
        file_name = 'player.json'
        file_path = os.path.join('source/data/chars', file_name)
        with open(file_path) as f:
            self.player_data = json.load(f)

        self.person = self.player_data[self.name]
        self.origin_health_point = self.person['health_point']
        self.health_point = self.person['health_point']
        self.vel = self.person['vel']
        self.damage = self.person['damage']

    # Normal states for now
    def setup_states(self):
        pass

    def setup_velocity(self):
        self.x_vel = 0
        self.y_vel = 0

    def setup_timers(self):
        self.walking_timer = 0
        self.die_timer = 0

    # Load the images and animations
    def load_images(self):
        frames = self.player_data['image_frames']

        self.die_sheet = setup.graphics[self.name + '_die']
        self.die_frames = []

        self.sheet = setup.graphics[self.name + '_walk']
        count = 0
        self.down_frames = []
        self.left_frames = []
        self.right_frames = []
        self.up_frames = []

        for group, group_frames in frames.items():
            for frame in group_frames:
                if group == 'walk':
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
                if group == 'die':
                    self.die_frames.append((frame['x'], frame['y'], frame['width'], frame['height']))

        self.frames = self.right_frames
        self.frame_index = 0
        self.image = tools.get_graphic(self.sheet, *self.frames[self.frame_index], (0, 0, 0), 1)
        self.rect = self.image.get_rect()

    # Show player's die animation
    def show_die_animation(self, surface):
        self.die_current = pygame.time.get_ticks()
        index = 0
        if self.die_current - self.die_timer > 1000:
            index = (self.frame_index + 1) % 3
        die_image = tools.get_graphic(self.die_sheet, *self.die_frames[index], (0, 0, 0), 1)
        surface.blit(die_image, self.rect)

    def update(self, keys, press):
        self.current = pygame.time.get_ticks()
        # Move
        if keys[pygame.K_d] and press:
            self.x_vel = self.vel
            self.y_vel = 0
            self.face = 'right'
            self.frames = self.right_frames
        if keys[pygame.K_a] and press:
            self.x_vel = -1 * self.vel
            self.y_vel = 0
            self.face = 'left'
            self.frames = self.left_frames
        if keys[pygame.K_w] and press:
            self.x_vel = 0
            self.y_vel = -1 * self.vel
            self.face = 'up'
            self.frames = self.up_frames
        if keys[pygame.K_s] and press:
            self.x_vel = 0
            self.y_vel = self.vel
            self.face = 'down'
            self.frames = self.down_frames

        if not press:
            self.x_vel = 0
            self.y_vel = 0

        # Imitate walking animation
        if (self.current - self.walking_timer > 100 and press) and (keys[pygame.K_d] or keys[pygame.K_a]
                                                                    or keys[pygame.K_w] or keys[pygame.K_s]):
            self.frame_index = (self.frame_index + 1) % 3
        self.image = tools.get_graphic(self.sheet, *self.frames[self.frame_index], (0, 0, 0), 1)
