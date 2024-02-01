# Create words information here

import pygame
from .. import constants as c

pygame.font.init()

class Info:
    def __init__(self, state):
        self.state = state
        self.create_state_labels()  # state words info
        self.create_basic_labels()  # basic words info

    # You can write word label and its position in different states here
    def create_state_labels(self):
        self.state_labels = []
        if self.state == 'main_menu':
            self.state_labels.append((self.create_label('重新入学'), (630, 350)))
            self.state_labels.append((self.create_label('继续学习'), (630, 410)))
            self.state_labels.append((self.create_label('查看笔记'), (630, 470)))
            self.state_labels.append((self.create_label('退学申请'), (630, 530)))
        elif self.state == 'choose_character':
            self.state_labels.append((self.create_label("Press '->' to view", size=30), (30, 20)))
            self.state_labels.append((self.create_label('Press Enter to choose', size=30), (30, 50)))
        elif self.state == 'view_note':
            self.state_labels.append((self.create_label("按Esc返回主菜单", size=20), (30, 20)))
        else:
            pass

    # You can write word label and its position that appears in the whole game here
    def create_basic_labels(self):
        self.info_labels = []

    # create word label
    def create_label(self, label, size=c.DEFAULT_SIZE, width_scale=c.WIDTH_SCALE, height_scale=c.HEIGHT_SCALE):
        font = pygame.font.Font(c.FONT, size)
        label_image = font.render(label, 1, (255, 255, 255))
        rect = label_image.get_rect()
        label_image = pygame.transform.scale(label_image, (int(rect.width * width_scale),
                                                           int(rect.height * height_scale)))
        return label_image

    def update(self):
        pass

    # draw word label
    def draw(self, surface):
        # surface.blit(self.create_label(' uuu'), (510, 350))
        for label in self.state_labels:
            surface.blit(label[0], label[1])
        for label in self.info_labels:
            surface.blit(label[0], label[1])