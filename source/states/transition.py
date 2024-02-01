# For transition class
import sys
from time import sleep

import pygame

from source import setup, tools, functions
from source.components import sound
from .. import constants as c


class GameOver:
    def __init__(self):
        self.setup_background()
        self.finished = False
        self.next = 'main_menu'
        self.timer = 0

    def setup_background(self):
        self.background = setup.graphics['game_over']
        self.background_rect = self.background.get_rect()
        self.background = pygame.transform.scale(self.background, (int(self.background_rect.width * 1.29),
                                                                   int(self.background_rect.height * 1.29)))
        self.viewport = setup.screen.get_rect()

    def update(self, surface, keys, press):
        if keys[pygame.K_ESCAPE] and press:
            sound.click.play()
            self.finished = True
            self.next = 'main_menu'
        surface.blit(self.background, self.viewport)
        if self.timer == 0:
            self.timer = pygame.time.get_ticks()
            sound.game_over.play()
        # Let the 'GAME OVER' appears for 7 sec
        elif pygame.time.get_ticks() - self.timer > 7000:
            sound.game_over.stop()
            self.finished = True
            self.timer = 0


class Win:
    def __init__(self):
        self.setup_background()
        self.finished = False
        self.next = 'main_menu'
        self.timer = 0

    def setup_background(self):
        self.background = setup.graphics['win']
        self.background_rect = self.background.get_rect()
        self.background = pygame.transform.scale(self.background, (int(self.background_rect.width * 0.794),
                                                                   int(self.background_rect.height * 0.9)))
        self.viewport = setup.screen.get_rect()

    def update(self, surface, keys, press):
        surface.blit(self.background, self.viewport)
        if self.timer == 0:
            self.timer = pygame.time.get_ticks()
            sound.win.play()
        # Let the 'Win' appears for 5 sec
        elif pygame.time.get_ticks() - self.timer > 5000:
            self.finished = True
            self.timer = 0


class Sure:
    def __init__(self):
        self.finished = False
        self.next = None

    def update(self, surface, keys, press):
        surface.fill([0, 0, 0])
        surface.blit(functions.create_label('确定重新开始吗?', size=25),
                     (230, 350))
        surface.blit(functions.create_label('按 Enter 后重新进入游戏以重置噢!(Enter/Esc)', size=25),
                     (230, 375))
        sleep(0.2)
        if keys[pygame.K_RETURN] and press:
            functions.update_state_now('choose_character')
            pygame.display.quit()
            sys.exit()
        elif keys[pygame.K_ESCAPE] and press:
            self.finished = True
            self.next = 'main_menu'
