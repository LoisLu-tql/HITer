import pygame
pygame.mixer.init()

sound_path = './resource/music/'

theme = pygame.mixer.Sound(sound_path + 'theme.wav')

enemies_attack = pygame.mixer.Sound(sound_path + 'enemies_attack.wav')

obstacle_stop_player = pygame.mixer.Sound(sound_path + 'obstacle_stop_player.wav')

start_fire = pygame.mixer.Sound(sound_path + 'start_fire.wav')

pick_up_gear = pygame.mixer.Sound(sound_path + 'pick_up_gear.wav')

pick_up_hp = pygame.mixer.Sound(sound_path + 'pick_up_hp.wav')

player_hit = pygame.mixer.Sound(sound_path + 'player_hit.wav')

game_over = pygame.mixer.Sound(sound_path + 'game_over.wav')

click = pygame.mixer.Sound(sound_path + 'click.wav')

win = pygame.mixer.Sound(sound_path + 'win.wav')

touch_boss = pygame.mixer.Sound(sound_path + 'touch_boss.wav')

boss = pygame.mixer.Sound(sound_path + 'boss.wav')

boss_final = pygame.mixer.Sound(sound_path + 'boss_final.wav')

buy = pygame.mixer.Sound(sound_path + 'buy.wav')
