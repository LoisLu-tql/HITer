# Game entrance
import sys

import pygame
from source.components import shop, sound
from source.states import a_state_dictionary as sd
from source import constants as c


class Game:
    def __init__(self, state_dict, start_state):
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.keys = pygame.key.get_pressed()
        self.press = False
        self.state_dict = state_dict
        self.state = self.state_dict[start_state]
        self.shop = shop.Shop()
        self.run_game = True

    def update(self):
        if self.state.finished:
            next_state = self.state.next
            self.state.finished = False
            self.state = self.state_dict[next_state]
        self.state.update(self.screen, self.keys, self.press)

    def run(self):
        while True:
            while self.run_game:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.display.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        self.press = True
                        self.keys = pygame.key.get_pressed()
                    elif event.type == pygame.KEYUP:
                        self.press = False
                        self.keys = pygame.key.get_pressed()
                self.update()
                pygame.display.update()
                self.clock.tick(c.FRAMES)

                if self.keys[pygame.K_i]:
                    sound.click.play()
                    self.run_game = False

            while not self.run_game:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.display.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        self.press = True
                        self.keys = pygame.key.get_pressed()
                    elif event.type == pygame.KEYUP:
                        self.press = False
                        self.keys = pygame.key.get_pressed()

                pygame.display.update()
                self.clock.tick(c.FRAMES)

                open_shop = self.shop.shop_open(self.screen, self.clock)

                if not open_shop:
                    self.run_game = True


def main():
    # Get state dictionary
    state_dict = sd.state_dict
    # Get a Game class and run it
    game = Game(state_dict, 'main_menu')
    game.run()


if __name__ == '__main__':
    main()
