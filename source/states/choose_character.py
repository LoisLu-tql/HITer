import os
from time import sleep

from ..components import info, sound
from .. import setup
from .. import tools
from .. import constants as c
from .. import functions
import pygame


class ChooseCharacter:
    def __init__(self):
        self.setup_background()
        self.info = info.Info('choose_character')
        self.finished = False
        self.load_characters()

    # You can change the bg
    def setup_background(self):
        self.background = setup.graphics['choose_char_bg']
        self.background_rect = self.background.get_rect()
        self.background = pygame.transform.scale(self.background, (int(self.background_rect.width * c.BG_SCALE),
                                                                   int(self.background_rect.height * c.BG_SCALE)))
        self.viewport = setup.screen.get_rect()

    # The origin order
    def load_characters(self):
        self.circle_queue = tools.CircleQueue(c.BASE_CHARACTERS_NUM)
        self.circle_queue.enter_queue([tools.get_graphic(setup.graphics['Will'],
                                                        0, 0, 144, 144, (123, 123, 123), 1), 'Will',
                                       functions.create_label("Will"), functions.create_label('"威海力量"', size=20),
                                       functions.create_label("自带伤害!", size=20)])
        self.circle_queue.enter_queue([tools.get_graphic(setup.graphics['Harry'],
                                                        0, 0, 144, 144, (123, 123, 123), 1), 'Harry',
                                       functions.create_label("Harry"), functions.create_label('"百岁老人"', size=20),
                                       functions.create_label("生命力提升!", size=20)])
        self.circle_queue.enter_queue([tools.get_graphic(setup.graphics['Sheeran'],
                                                        0, 0, 144, 144, (123, 123, 123), 1), 'Sheeran',
                                       functions.create_label("Sheeran"), functions.create_label('"深圳速度"', size=20),
                                       functions.create_label("移速增加!", size=20)])

    def choose_char(self, keys):
        # We can only press '->' because of the queue
        if keys[pygame.K_RIGHT]:
            sound.click.play()
            replace = self.circle_queue.out_queue()
            self.circle_queue.enter_queue(replace)
            sleep(0.2)
        elif keys[pygame.K_RETURN]:
            # remember the char
            sound.click.play()
            file_name = 'char.txt'
            file_path = os.path.join('source/memory', file_name)
            replace = self.circle_queue.out_queue()
            self.circle_queue.enter_queue(replace)
            choice = self.circle_queue.out_queue()
            if choice[1] == 'Harry':
                with open(file_path, 'w') as f:
                    f.write('Harry')
            elif choice[1] == 'Sheeran':
                with open(file_path, 'w') as f:
                    f.write('Sheeran')
            elif choice[1] == 'Will':
                with open(file_path, 'w') as f:
                    f.write('Will')
            functions.update_state_now('tip1')
            sleep(0.2)
            self.circle_queue.enter_queue(choice)
            self.finished = True
            self.next = 'tip1'

    def update(self, surface, keys, press):
        if keys[pygame.K_ESCAPE] and press:
            sound.click.play()
            self.finished = True
            self.next = 'main_menu'

        self.choose_char(keys)
        surface.blit(self.background, self.viewport)

        # Change the order
        replace = self.circle_queue.out_queue()
        surface.blit(replace[0], (170, 250))
        surface.blit(replace[2], (170, 400))
        surface.blit(replace[3], (170, 450))
        surface.blit(replace[4], (180, 470))
        self.circle_queue.enter_queue(replace)

        replace = self.circle_queue.out_queue()
        replace_copy = pygame.transform.scale(replace[0], (204, 204))
        surface.blit(replace_copy, (390, 230))
        surface.blit(replace[2], (390, 440))
        surface.blit(replace[3], (390, 490))
        surface.blit(replace[4], (400, 510))
        self.circle_queue.enter_queue(replace)

        replace = self.circle_queue.out_queue()
        surface.blit(replace[0], (670, 250))
        surface.blit(replace[2], (670, 400))
        surface.blit(replace[3], (670, 450))
        surface.blit(replace[4], (680, 470))
        self.circle_queue.enter_queue(replace)

        self.info.draw(surface)