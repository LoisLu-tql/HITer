# Origin Start Settings
import os

import pygame
import win32api
import win32con
from pygame.sprite import Group

from . import constants as c
from . import tools

pc_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
pc_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)

os.environ['SDL_VIDEO_WINDOW_POS'] = '%d, %d' % (pc_width / 2 - c.SCREEN_WIDTH / 2,
                                                 pc_height / 2 - c.SCREEN_HEIGHT / 2)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
pygame.display.set_caption("Hiter")



# Load all graphics that will use
graphics = tools.load_graphics('resource/graphics')

game_icon = graphics['icon']
pygame.display.set_icon(game_icon)
