# Game functions

import os
import random
import sys

import pygame

from source import setup, tools
from source.components import player, enemy, boss, sound
from source.components.ranged_weapons import RangedWeapons
from . import constants as c
from .components.drop_item import DropItem


# Create the chosen character and put him/her to the start position
# Need the player's start pos
def setup_player(start_x, start_y):
    file_name = 'char.txt'
    file_path = os.path.join('source/memory', file_name)
    with open(file_path, 'r') as f:
        choice = f.read()
    the_player = player.Player(choice)
    the_player.rect.x = start_x
    the_player.rect.y = start_y
    return the_player


# Using this function to set up enemies in every map
def setup_enemy(enemy_num, enemy_name, the_player, enemies, pos):
    for count in range(0, enemy_num):
        new_enemy = enemy.Enemy(enemy_name, the_player)
        new_enemy.setup_enemy_pos(pos[count])
        enemies.add(new_enemy)


def setup_boss(b_type, pos_x, pos_y):
    if b_type == 1:
        the_boss = boss.Boss1(pos_x, pos_y)
    elif b_type == 2:
        the_boss = boss.Boss2(pos_x, pos_y)
    elif b_type == 3:
        the_boss = boss.Boss3(pos_x, pos_y)
    elif b_type == 4:
        the_boss = boss.Boss4(pos_x, pos_y)
    else:
        the_boss = boss.BossFinal(pos_x, pos_y)
    return the_boss


def update_player_pos(the_player):
    the_player.rect.x += the_player.x_vel
    the_player.rect.y += the_player.y_vel


def update_enemy_pos(the_enemy):
    the_enemy.rect.x += the_enemy.x_vel
    the_enemy.rect.y += the_enemy.y_vel


def update_ranged_weapons_pos(ranged_weapon):
    ranged_weapon.rect.x += ranged_weapon.x_vel
    ranged_weapon.rect.y += ranged_weapon.y_vel


# the collisions check from pygame is not suitable
# Need surface and 3 groups
def check_weapon_enemy_collisions(weapons, enemies, surface, drop_items):
    # collisions = pygame.sprite.groupcollide(weapons, enemies, True, True)
    # for k, v in collisions.items():
    #     print(k.rect.x)
    #     print(k.rect.y)
    for weapon in weapons:
        for each_enemy in enemies:
            if each_enemy.rect.left < weapon.rect.centerx < each_enemy.rect.right and \
                    each_enemy.rect.top < weapon.rect.centery < each_enemy.rect.bottom:
                each_enemy.health_point -= weapon.damage
                weapons.remove(weapon)
                sound.player_hit.play()
                if each_enemy.health_point <= 0:
                    each_enemy.show_die_animation(surface)
                    new_drop = DropItem(each_enemy.rect.x, each_enemy.rect.y)
                    drop_items.add(new_drop)
                    enemies.remove(each_enemy)


#  the collisions check from pygame is not suitable
def check_player_enemy_collisions(the_player, enemies):
    for each_enemy in enemies:
        if each_enemy.rect.left < the_player.rect.centerx < each_enemy.rect.right and \
                each_enemy.rect.top < the_player.rect.centery < each_enemy.rect.bottom:
            the_player.health_point -= each_enemy.damage
            each_enemy.health_point -= the_player.damage
            if each_enemy.health_point <= 0:
                enemies.remove(each_enemy)
            sound.enemies_attack.play()


def if_player_die(the_player, surface):
    if the_player.health_point <= 0:
        the_player.show_die_animation(surface)
        return True


# check the fire
def start_fire_ranged_weapon(keys, the_player, weapon_name, ranged_weapons):
    if keys[pygame.K_j]:
        new = RangedWeapons(weapon_name, the_player)
        if len(ranged_weapons) < new.cartridge:
            sound.start_fire.play()
            ranged_weapons.add(new)


# remove the weapons that out of the screen to smooth the game running
def check_ranged_weapons_edge(ranged_weapons):
    for ranged_weapon in ranged_weapons.copy():
        if ranged_weapon.rect.bottom <= 0 or ranged_weapon.rect.right <= 0 \
                or ranged_weapon.rect.left >= c.SCREEN_WIDTH or ranged_weapon.rect.top >= c.SCREEN_HEIGHT:
            ranged_weapons.remove(ranged_weapon)


# the set and update of the blood bar
def set_blood_bar(surface, the_player):
    sheet = setup.graphics['items']
    blood_icon = tools.get_graphic(sheet, 128, 160, 32, 32, (0, 0, 0), 1)
    surface.blit(blood_icon, c.BLOODICON_POS)
    blood = the_player.health_point / the_player.origin_health_point * c.BLOODBAR_WIDTH
    pygame.draw.rect(surface, c.BLOOD_BACKGROUND, (c.BLOOD_BAR_POS[0], c.BLOOD_BAR_POS[1],
                                              c.BLOODBAR_WIDTH, c.BLOODBAR_HEIGHT), 0)
    pygame.draw.rect(surface, c.BLOOD_COLOR, (c.BLOOD_BAR_POS[0], c.BLOOD_BAR_POS[1],
                                              blood, c.BLOODBAR_HEIGHT), 0)
    surface.blit(create_label(str(the_player.health_point), size=30), c.BLOOD_NUM_POS)


# show the player's gears number
def show_gear_num(surface, icon_pos = c.GEARICON_POS, num_pos=c.GEARNUM_POS):
    sheet = setup.graphics['items']
    gear_icon = tools.get_graphic(sheet, 96, 160, 32, 32, (0, 0, 0), 1)
    surface.blit(gear_icon, icon_pos)
    file_name = 'gear_num.txt'
    file_path = os.path.join('source/memory', file_name)
    with open(file_path, 'r') as f:
        gear_num = f.read()
    gear_num_image = create_label(gear_num, size=30)
    surface.blit(gear_num_image, num_pos)


# Check if the player touches the obstacles or the screen edge
def check_player_obstacle_edge(ranges, the_player):
    for range in ranges:
        left = range[0]
        top = range[1]
        right = range[0] + range[2]
        bottom = range[1] + range[3]
        if left <= the_player.rect.centerx <= right and top <= the_player.rect.centery <= bottom\
                or the_player.rect.left < 0 or the_player.rect.right > c.SCREEN_WIDTH\
                or the_player.rect.top < 0 or the_player.rect.bottom > c.SCREEN_HEIGHT:
            if the_player.face == 'left':
                return 'from_right'
            elif the_player.face == 'right':
                return 'from_left'
            elif the_player.face == 'up':
                return 'from_down'
            elif the_player.face == 'down':
                return 'from_up'


# Keep the player out of the obstacles and stay in the screen
def obstacle_stop_player(player_obstacle_type, the_player):
    if player_obstacle_type == 'from_right':
        the_player.x_vel = 0
        the_player.y_vel = 0
        the_player.rect.centerx += the_player.vel
    elif player_obstacle_type == 'from_left':
        the_player.x_vel = 0
        the_player.y_vel = 0
        the_player.rect.centerx -= the_player.vel
    elif player_obstacle_type == 'from_down':
        the_player.x_vel = 0
        the_player.y_vel = 0
        the_player.rect.centery += the_player.vel
    elif player_obstacle_type == 'from_up':
        the_player.x_vel = 0
        the_player.y_vel = 0
        the_player.rect.centery -= the_player.vel
    sound.obstacle_stop_player.play()


# check if the player picks the drop item
def check_pick_up(keys, press, the_player, drop_items):
    for drop_item in drop_items.copy():
        if keys[pygame.K_k] and abs(the_player.rect.centerx - drop_item.center_x) < 20\
                and abs(the_player.rect.centery - drop_item.center_y) < 20 and press:
            drop_item.have_an_impact(the_player)
            drop_items.remove(drop_item)
        if drop_item.choice[0] == 'none':
            drop_items.remove(drop_item)


# check if the weapons and the obstacles have collisions
def check_weapon_obstacle_edge(ranges, ranged_weapons):
    for ranged_weapon in ranged_weapons.copy():
        for range in ranges:
            left = range[0]
            top = range[1]
            right = range[0] + range[2]
            bottom = range[1] + range[3]
            if left <= ranged_weapon.rect.centerx <= right and\
                    top <= ranged_weapon.rect.centery <= bottom:
                ranged_weapons.remove(ranged_weapon)


# enemies cannot walk over the obstacles either!
def check_enemy_obstacle_edge(ranges, enemies):
    for the_enemy in enemies:
        for range in ranges:
            left = range[0]
            top = range[1]
            right = range[0] + range[2]
            bottom = range[1] + range[3]
            if left <= the_enemy.rect.centerx <= right and top <= the_enemy.rect.centery <= bottom \
                    or the_enemy.rect.left < 0 or the_enemy.rect.right > c.SCREEN_WIDTH \
                    or the_enemy.rect.top < 0 or the_enemy.rect.bottom > c.SCREEN_HEIGHT:
                if the_enemy.face == 'left':
                    the_enemy.rect.centerx += the_enemy.vel
                elif the_enemy.face == 'right':
                    the_enemy.rect.centerx -= the_enemy.vel
                elif the_enemy.face == 'up':
                    the_enemy.rect.centery += the_enemy.vel
                elif the_enemy.face == 'down':
                    the_enemy.rect.centery -= the_enemy.vel


def create_label(label, size=c.DEFAULT_SIZE, width_scale=c.WIDTH_SCALE, height_scale=c.HEIGHT_SCALE,
                 font=c.FONT, color=c.DEFAULT_COLOR):
    font = pygame.font.Font(font, size)
    label_image = font.render(label, 1, color)
    rect = label_image.get_rect()
    label_image = pygame.transform.scale(label_image, (int(rect.width * width_scale),
                                                    int(rect.height * height_scale)))
    return label_image


def ranged_weapon_boss_collision(weapons, the_boss):
    for weapon in weapons:
        if the_boss.rect.left < weapon.rect.centerx < the_boss.rect.right and \
                the_boss.rect.top < weapon.rect.centery < the_boss.rect.bottom:
            the_boss.health_point -= weapon.damage
            weapons.remove(weapon)
            sound.player_hit.play()
            if the_boss.health_point <= 0:
                return True


def player_boss_collision(the_boss, the_player):
    if the_boss.rect.left < the_player.rect.centerx < the_boss.rect.right and \
            the_boss.rect.top < the_player.rect.centery < the_boss.rect.bottom:
        sound.touch_boss.play()
        the_player.health_point -= 99


# Boss1 related
def setup_boss1_weapon_pos(b1ws, the_player, pos_x, pos_y):
    new_b1w = boss.Boss1Weapon(the_player, pos_x, pos_y)
    b1ws.add(new_b1w)


def update_boss1_weapon_pos(b1w):
    b1w.rect.x += b1w.x_vel
    b1w.rect.y += b1w.y_vel


def b1w_player_collision(b1ws, the_player):
    for b1w in b1ws.copy():
        if the_player.rect.left < b1w.rect.centerx < the_player.rect.right and \
                the_player.rect.top < b1w.rect.centery < the_player.rect.bottom:
            the_player.health_point -= b1w.damage
            b1ws.remove(b1w)


# Boss2 related
def setup_boss2_weapon_pos(b2ws):
    new_b2w = boss.Boss2Weapon()
    b2ws.add(new_b2w)


def update_boss2_weapon_pos(b2w):
    if b2w.side == 1:
        b2w.rect.y += b2w.vel
    elif b2w.side == 2:
        b2w.rect.x -= b2w.vel
    elif b2w.side == 3:
        b2w.rect.x += b2w.vel
    elif b2w.side == 4:
        b2w.rect.y -= b2w.vel


def b2w_player_or_edge_collision(b2ws, the_player):
    for b2w in b2ws.copy():
        if the_player.rect.left < b2w.rect.centerx < the_player.rect.right and \
                the_player.rect.top < b2w.rect.centery < the_player.rect.bottom:
            the_player.health_point -= b2w.damage
            b2ws.remove(b2w)
        if b2w.rect.bottom < 0 or b2w.rect.top > c.SCREEN_HEIGHT or\
                b2w.rect.left > c.SCREEN_WIDTH or b2w.rect.right < 0:
            b2ws.remove(b2w)


# Boss3 related
def update_boss3_pos(the_boss):
    the_boss.rect.x = random.randint(100, c.SCREEN_WIDTH-100)
    the_boss.rect.y = random.randint(100, c.SCREEN_HEIGHT-100)


def boss3_hurt_player(the_boss, the_player):
    if the_boss.health_point > 0:
        the_player.health_point -= the_boss.damage


# Boss4 related
def setup_boss4_weapon_pos(b4ws, pos_x, pos_y):
    left = 0
    right = 0
    up = 0
    down = 0
    for b4w in b4ws:
        if b4w.toward == 'left':
            left += 1
        elif b4w.toward == 'right':
            right += 1
        elif b4w.toward == 'up':
            up += 1
        elif b4w.toward == 'down':
            down += 1
    min_toward = min(left, right, up, down)
    if min_toward == left:
        new_b4w = boss.Boss4Weapon(pos_x-24, pos_y-24, 'left')
        b4ws.add(new_b4w)
    elif min_toward == right:
        new_b4w = boss.Boss4Weapon(pos_x-24, pos_y-24, 'right')
        b4ws.add(new_b4w)
    elif min_toward == up:
        new_b4w = boss.Boss4Weapon(pos_x-24, pos_y-24, 'up')
        b4ws.add(new_b4w)
    elif min_toward == down:
        new_b4w = boss.Boss4Weapon(pos_x-24, pos_y-24, 'down')
        b4ws.add(new_b4w)


def update_boss4_weapon_pos(b4w):
    if b4w.toward == 'left':
        b4w.rect.x -= b4w.vel
    elif b4w.toward == 'right':
        b4w.rect.x += b4w.vel
    elif b4w.toward == 'up':
        b4w.rect.y -= b4w.vel
    elif b4w.toward == 'down':
        b4w.rect.y += b4w.vel


def b4w_player_or_edge_collision(b4ws, the_player):
    b2w_player_or_edge_collision(b4ws, the_player)


def boss4_reborn(the_boss, ranged_weapons):
    if ranged_weapon_boss_collision(ranged_weapons, the_boss) and the_boss.life < 8:
        the_boss.life += 1
        the_boss.health_point = the_boss.origin_health_point
        the_boss.pos_x = random.randint(100, c.SCREEN_WIDTH-100)
        the_boss.pos_y = random.randint(100, c.SCREEN_HEIGHT-100)
        the_boss.rect.x = the_boss.pos_x
        the_boss.rect.y = the_boss.pos_y


# BossFinal related
def summon_robots(the_player, enemies, enemies_pos):
    summon = random.randint(1, 8)
    if summon == 1:
        setup_enemy(3, 'PA_robot', the_player, enemies, enemies_pos)
    elif summon == 2:
        setup_enemy(3, 'PA_robot_R', the_player, enemies, enemies_pos)
    elif summon == 3:
        setup_enemy(3, 'PA_robot_O', the_player, enemies, enemies_pos)
    elif summon == 4:
        setup_enemy(3, 'PA_robot_G', the_player, enemies, enemies_pos)
    elif summon == 5:
        setup_enemy(3, 'LAB_robot_B', the_player, enemies, enemies_pos)
    elif summon == 6:
        setup_enemy(3, 'LAB_robot_R', the_player, enemies, enemies_pos)
    elif summon == 7:
        setup_enemy(3, 'LAB_robot_W', the_player, enemies, enemies_pos)
    elif summon == 8:
        setup_enemy(3, 'LAB_robot_G', the_player, enemies, enemies_pos)


# passageways related
def check_player_passageways_edge(ranges, the_player):
    for range in ranges:
        left = range[0]
        top = range[1]
        right = range[0] + range[2]
        bottom = range[1] + range[3]
        if left <= the_player.rect.centerx <= right and top <= the_player.rect.centery <= bottom\
                or the_player.rect.left < 0 or the_player.rect.right > c.SCREEN_WIDTH\
                or the_player.rect.top < 0 or the_player.rect.bottom > c.SCREEN_HEIGHT:
            if the_player.face == 'left':
                return 'go_left'
            elif the_player.face == 'right':
                return 'go_right'
            elif the_player.face == 'up':
                return 'go_up'
            elif the_player.face == 'down':
                return 'go_down'


def check_boss_passageways_edge(range, the_player):
    left = range[0]
    top = range[1]
    right = range[0] + range[2]
    bottom = range[1] + range[3]
    if left <= the_player.rect.centerx <= right and top <= the_player.rect.centery <= bottom \
            or the_player.rect.left < 0 or the_player.rect.right > c.SCREEN_WIDTH \
            or the_player.rect.top < 0 or the_player.rect.bottom > c.SCREEN_HEIGHT:
        if the_player.face == 'left':
            return 'go_left'
        elif the_player.face == 'right':
            return 'go_right'
        elif the_player.face == 'up':
            return 'go_up'
        elif the_player.face == 'down':
            return 'go_down'


def passageway_stop_player(player_obstacle_type, the_player):
    if player_obstacle_type == 'go_left':
        the_player.x_vel = 0
        the_player.y_vel = 0
        the_player.rect.centerx += 3
    elif player_obstacle_type == 'go_right':
        the_player.x_vel = 0
        the_player.y_vel = 0
        the_player.rect.centerx -= 3
    elif player_obstacle_type == 'go_up':
        the_player.x_vel = 0
        the_player.y_vel = 0
        the_player.rect.centery += 3
    elif player_obstacle_type == 'go_down':
        the_player.x_vel = 0
        the_player.y_vel = 0
        the_player.rect.centery -= 3


# update
def update_enemies(enemies, obstacles_ranges, surface):
    for each_enemy in enemies.sprites():
        each_enemy.update()
        update_enemy_pos(each_enemy)
        if each_enemy.name == 'LAB_robot_G':
            choice = random.randint(1, 5)
            if choice == 1:
                surface.blit(each_enemy.image, each_enemy.rect)
                each_enemy.draw_blood_bar(surface)
        else:
            surface.blit(each_enemy.image, each_enemy.rect)
            each_enemy.draw_blood_bar(surface)
    check_enemy_obstacle_edge(obstacles_ranges, enemies)


def update_ranged_weapons(weapon_name, ranged_weapons, the_player, enemies, obstacles_ranges, drop_items, surface, keys, press):
    start_fire_ranged_weapon(keys, the_player, weapon_name, ranged_weapons)
    for ranged_weapon in ranged_weapons.sprites():
        ranged_weapon.update(keys, press)
        update_ranged_weapons_pos(ranged_weapon)
        surface.blit(ranged_weapon.show_image, ranged_weapon.rect)
    check_ranged_weapons_edge(ranged_weapons)
    check_weapon_obstacle_edge(obstacles_ranges, ranged_weapons)
    check_weapon_enemy_collisions(ranged_weapons, enemies, surface, drop_items)


def update_state_now(state_name):
    file_name = 'state_now.txt'
    file_path = os.path.join('source/memory', file_name)
    with open(file_path, 'w') as f:
        f.write(state_name)


def update_blood_stored(level, the_player):
    file_name = 'blood_store.txt'
    if level == 1:
        file_path = os.path.join('source/states/firstlevel', file_name)
        with open(file_path, 'w') as f:
            f.write(str(the_player.health_point))
    elif level == 2:
        file_path = os.path.join('source/states/secondlevel', file_name)
        with open(file_path, 'w') as f:
            f.write(str(the_player.health_point))
    elif level == 3:
        file_path = os.path.join('source/states/thirdlevel', file_name)
        with open(file_path, 'w') as f:
            f.write(str(the_player.health_point))


def load_blood_stored(level, the_player):
    file_name = 'blood_store.txt'
    if level == 1:
        file_path = os.path.join('source/states/firstlevel', file_name)
        with open(file_path, 'r') as f:
            the_player.health_point = int(f.read())
    elif level == 2:
        file_path = os.path.join('source/states/secondlevel', file_name)
        with open(file_path, 'r') as f:
            the_player.health_point = int(f.read())
    elif level == 3:
        file_path = os.path.join('source/states/thirdlevel', file_name)
        with open(file_path, 'r') as f:
            the_player.health_point = int(f.read())


def start_over_set(enemies, drop_items, ranged_weapons):
    for each_enemy in enemies:
        enemies.remove(each_enemy)
    for drop_item in drop_items:
        drop_items.remove(drop_item)
    for ranged_weapon in ranged_weapons:
        ranged_weapons.remove(ranged_weapon)


# shop related
def shop_update_gears_num(price):
    file_name = 'gear_num.txt'
    file_path = os.path.join('source/memory', file_name)
    with open(file_path, 'r') as f:
        gears = int(f.read())

    gears -= price
    if gears < 0:
        return False

    file_name = 'gear_num.txt'
    file_path = os.path.join('source/memory', file_name)
    with open(file_path, 'w') as f:
        f.write(str(gears))

    return True


def update_weapon_now(weapon_name):
    file_name = 'weapon_now.txt'
    file_path = os.path.join('source/memory', file_name)
    with open(file_path, 'w') as f:
        f.write(weapon_name)


def update_supply(supply_name):
    if supply_name == 'red':
        file_name = 'supply_red.txt'
        file_path = os.path.join('source/memory', file_name)
        with open(file_path, 'r') as f:
            supply_num = int(f.read())
        supply_num += 1
        with open(file_path, 'w') as f:
            f.write(str(supply_num))
    elif supply_name == 'orange':
        file_name = 'supply_orange.txt'
        file_path = os.path.join('source/memory', file_name)
        with open(file_path, 'r') as f:
            supply_num = int(f.read())
        supply_num += 1
        with open(file_path, 'w') as f:
            f.write(str(supply_num))
    elif supply_name == 'green':
        file_name = 'supply_green.txt'
        file_path = os.path.join('source/memory', file_name)
        with open(file_path, 'r') as f:
            supply_num = int(f.read())
        supply_num += 1
        with open(file_path, 'w') as f:
            f.write(str(supply_num))
    elif supply_name == 'blue':
        file_name = 'supply_blue.txt'
        file_path = os.path.join('source/memory', file_name)
        with open(file_path, 'r') as f:
            supply_num = int(f.read())
        supply_num += 1
        with open(file_path, 'w') as f:
            f.write(str(supply_num))
    else:
        pass


def supply_effect(the_player):
    file_name = 'supply_red.txt'
    file_path = os.path.join('source/memory', file_name)
    with open(file_path, 'r') as f:
        supply_num = int(f.read())
    if supply_num > 0:
        the_player.origin_health_point += 10
        supply_num -= 1
    with open(file_path, 'w') as f:
        f.write(str(supply_num))

    file_name = 'supply_orange.txt'
    file_path = os.path.join('source/memory', file_name)
    with open(file_path, 'r+') as f:
        supply_num = int(f.read())
    if supply_num > 0:
        if the_player.health_point <= the_player.origin_health_point - 30:
            the_player.health_point += 30
        else:
            the_player.health_point = the_player.origin_health_point
        supply_num -= 1
    with open(file_path, 'w') as f:
        f.write(str(supply_num))

    file_name = 'supply_green.txt'
    file_path = os.path.join('source/memory', file_name)
    with open(file_path, 'r+') as f:
        supply_num = int(f.read())
    if supply_num > 0:
        the_player.vel += 3
        supply_num -= 1
    with open(file_path, 'w') as f:
        f.write(str(supply_num))

    file_name = 'supply_blue.txt'
    file_path = os.path.join('source/memory', file_name)
    with open(file_path, 'r+') as f:
        supply_num = int(f.read())
    if supply_num > 0:
        the_player.damage += 5
        supply_num -= 1
    with open(file_path, 'w') as f:
        f.write(str(supply_num))


def get_cost_list():
    file_name = 'weapon_cost.txt'
    file_path = os.path.join('source/memory', file_name)
    with open(file_path, 'r+') as f:
        cost_string = f.read()
    cost_list = cost_string.split(',', 8)
    return cost_list


def update_cost_list(cost_list, modify_pos):
    count = 0
    new_cost = ''
    while count < modify_pos - 1:
        new_cost += cost_list[count] + ','
        count += 1
    new_cost += '2'
    while count < 8:
        count += 1
        new_cost += ',' + cost_list[count]
    file_name = 'weapon_cost.txt'
    file_path = os.path.join('source/memory', file_name)
    with open(file_path, 'w') as f:
        f.write(new_cost)


def buying(update_shop, shop_type, screen, talk, talk_1, talk_2, cost, goods_name, goods_code):
    flag = 1
    screen.blit(talk, c.SHOP_TALK_POS)
    pygame.display.update()
    while flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                sound.click.play()
                if event.key == pygame.K_RETURN:
                    # if self.coins >= self.SHOP1_1:
                    if shop_update_gears_num(cost):
                        # self.coins -= self.SHOP1_1
                        # # TODO 背包变化
                        # self.text = self.font.render("coins:" + str(self.coins), True, (0, 0, 255))
                        if shop_type == 1:
                            update_weapon_now(goods_name)
                            update_cost_list(get_cost_list(), goods_code)
                        elif shop_type == 2:
                            update_supply(goods_name)
                        sound.buy.play()
                        update_shop(screen)
                        screen.blit(talk_1, c.SHOP_TALK_POS)
                        pygame.display.update()
                        pygame.time.delay(1000)
                        flag = 0
                    else:
                        screen.blit(talk_2, c.SHOP_TALK_POS)
                        pygame.display.update()
                        pygame.time.delay(1000)
                        flag = 0
                if event.key == pygame.K_ESCAPE:
                    flag = 0


def load_weapon_name():
    file_name = 'weapon_now.txt'
    file_path = os.path.join('source/memory', file_name)
    with open(file_path, 'r') as f:
        weapon_name = f.read()

    return weapon_name
