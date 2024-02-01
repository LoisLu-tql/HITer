# Create our main menu surface
import os
import sys
from time import sleep

import pygame
from .. import setup, functions
from .. import tools
from .. import constants as c
from ..components import info, sound


class MainMenu:
    def __init__(self):
        self.setup_background()
        self.setup_cursor()
        self.info = info.Info('main_menu')
        self.finished = False
        self.bgm = sound.theme
        self.bgm.play(-1)

    # u can change bg and the caption
    def setup_background(self):
        self.background = setup.graphics['menu_bg']
        self.background_rect = self.background.get_rect()
        self.background = pygame.transform.scale(self.background, (int(self.background_rect.width * c.BG_SCALE),
                                                 int(self.background_rect.height * c.BG_SCALE)))
        self.viewport = setup.screen.get_rect()
        self.caption = tools.get_graphic(setup.graphics['menu_caption'], 0, 0, 742, 240, (0, 0, 0), 1)

    # u can change the cursor
    def setup_cursor(self):
        self.cursor = pygame.sprite.Sprite()
        self.cursor.image = tools.get_graphic(setup.graphics['menu_cursor'],
                                              0, 0, 200, 200, (0, 0, 0), c.BG_CURSOR_SCALE)
        rect = self.cursor.image.get_rect()
        rect.x = 580
        rect.y = 363
        self.cursor.rect = rect
        self.cursor.state = 0

    # change the cursor's pos
    def update_cursor(self, keys, press, surface):
        if keys[pygame.K_UP] and press:
            if self.cursor.state > 0:
                sound.click.play()
                self.cursor.state -= 1
                self.cursor.rect.y -= 60
        elif keys[pygame.K_DOWN] and press:
            if self.cursor.state < 3:
                sound.click.play()
                self.cursor.state += 1
                self.cursor.rect.y += 60
        elif keys[pygame.K_RETURN] and press:
            sound.click.play()
            sleep(0.2)
            if self.cursor.state == 0:
                file_name = 'state_now.txt'
                file_path = os.path.join('source/memory', file_name)
                with open(file_path, 'r') as f:
                    state_now = f.read()
                if state_now == 'choose_character':
                    self.finished = True
                    self.bgm.fadeout(1000)
                    self.next = 'choose_character'
                else:
                    self.finished = True
                    self.bgm.fadeout(1000)
                    self.next = 'sure'

            elif self.cursor.state == 1:
                file_name = 'state_now.txt'
                file_path = os.path.join('source/memory', file_name)
                with open(file_path, 'r') as f:
                    state_now = f.read()
                self.finished = True
                self.bgm.fadeout(1000)
                self.next = state_now
            elif self.cursor.state == 2:
                self.finished = True
                self.bgm.fadeout(1000)
                self.next = 'view_note'
            elif self.cursor.state == 3:
                pygame.quit()
                sys.exit()

    def update(self, surface, keys, press):
        # Draw..
        self.update_cursor(keys, press, surface)

        surface.blit(self.background, self.viewport)
        surface.blit(self.caption, (250, 100))
        surface.blit(self.cursor.image, self.cursor.rect)

        self.info.update()
        self.info.draw(surface)
