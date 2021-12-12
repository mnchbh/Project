import pygame
from pygame import mixer
import os
import random
import csv
import button
mixer.init()
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH*0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Tester')

#set framerate
clock = pygame.time.Clock()
FPS = 60
#define game varibles
GRAVITY = 0.75
SCROLL_THRESH = 200
ROWS = 16
COLS = 150
TILE_SIZE = SCREEN_HEIGHT//ROWS
TILE_TYPES = 19
MAX_LEVELS = 1
screen_scroll = 0
bg_scroll = 0
level = 0
start_game = False
start_intro = False
#define player action variables
moving_left = False
moving_right = False
shoot = False

#load music and sound
pygame.mixer.music.load('audio/Puzzle-Game.mp3')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1, 0.0, 5000)
jump_fx = pygame.mixer.Sound('audio/jump.wav')
jump_fx.set_volume(0.05)
shot_fx = pygame.mixer.Sound('audio/shot.wav')
shot_fx.set_volume(0.05)

#load images
#button images
start_img = pygame.image.load('img/start_btn.png').convert_alpha()
exit_img = pygame.image.load('img/exit_btn.png').convert_alpha()
restart_img = pygame.image.load('img/restart_btn.png').convert_alpha()
#background
pinel1_img = pygame.image.load('img/Layer_0011_0.png').convert_alpha()
pinel2_img = pygame.image.load('img/Layer_0010_1.png').convert_alpha()
pinel3_img = pygame.image.load('img/Layer_0009_2.png').convert_alpha()
pinel4_img = pygame.image.load('img/Layer_0008_3.png').convert_alpha()
pinel5_img = pygame.image.load('img/Layer_0006_4.png').convert_alpha()
pinel6_img = pygame.image.load('img/Layer_0005_5.png').convert_alpha()
pinel7_img = pygame.image.load('img/Layer_0003_6.png').convert_alpha()
pinel8_img = pygame.image.load('img/Layer_0002_7.png').convert_alpha()
pinel9_img = pygame.image.load('img/Layer_0001_8.png').convert_alpha()
pinel10_img = pygame.image.load('img/Layer_0000_9.png').convert_alpha()
#store tiles in a list
img_list = []
for x in range(TILE_TYPES):
	img = pygame.image.load(f'img/pic/{x}.png')
	img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
	img_list.append(img)
#Arrow
arrow_img = pygame.image.load('img/player1/arrow.png').convert_alpha()
#health
health_box_img = pygame.image.load('img/item/heart.png').convert_alpha()
item_boxes = {
    'Health'    : health_box_img}

#define color
BG = (144, 201, 120)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
PINK = (235, 65, 54)

#define font
font = pygame.font.SysFont('Futura', 30)

def draw_txt(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))

def draw_bg():
    screen.fill(BG)
    windth = pinel1_img.get_width()
    for i in range(10):
        screen.blit(pinel1_img, ((i*windth)-bg_scroll*0.5, 0))
        screen.blit(pinel2_img, ((i*windth)-bg_scroll*0.5, SCREEN_HEIGHT-pinel2_img.get_height()))
        # screen.blit(pinel3_img, ((i*windth)-bg_scroll*0.45, SCREEN_HEIGHT-pinel3_img.get_height()))
        screen.blit(pinel4_img, ((i*windth)-bg_scroll*0.5, SCREEN_HEIGHT-pinel4_img.get_height()))
        # screen.blit(pinel5_img, ((i*windth)-bg_scroll*0.55, SCREEN_HEIGHT-pinel5_img.get_height()))
        screen.blit(pinel6_img, ((i*windth)-bg_scroll*0.6, SCREEN_HEIGHT-pinel6_img.get_height()))
        screen.blit(pinel7_img, ((i*windth)-bg_scroll*0.65, SCREEN_HEIGHT-pinel7_img.get_height()))
        screen.blit(pinel8_img, ((i*windth)-bg_scroll*0.7, SCREEN_HEIGHT-pinel8_img.get_height()))
        screen.blit(pinel9_img, ((i*windth)-bg_scroll*0.75, SCREEN_HEIGHT-pinel9_img.get_height()))
        screen.blit(pinel10_img, ((i*windth)-bg_scroll*0.8, SCREEN_HEIGHT-pinel10_img.get_height()))

#function to reset level
def reset_level():
    enemy_group.empty()
    arrow_group.empty()
    item_group.empty()
    decoration_group.empty()
    water_group.empty()
    exit_group.empty()

    #create empty tile list
    data = []
    for row in range(ROWS):
        r = [-1] * COLS
        data.append(r)

    return data

class Archer(pygame.sprite.Sprite):
    def __init__(self, cha_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.cha_type = cha_type
        self.speed = speed
        self.shoot_cooldown = 0
        self.health = 100
        self.max_health = self.health
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        #ai specific variables
        self.move_counter = 0
        self.vision = pygame.Rect(0, 0, 150, 20)
        self.idling = False
        self.idling_counter = 0

        #load all imagefor the players
        animation_types = ['idle', 'run', 'jump', 'shoot', 'dead']
        for animation in animation_types:
            #reset temporary list of images
            temp_list = []
            #count number of files in the folder
            num_frame = len(os.listdir(f'img/{self.cha_type}/{animation}'))
            for i in range(num_frame):
                img = pygame.image.load(f'img/{self.cha_type}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width()*scale), int(img.get_height()*scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        self.update_animation()
        self.check_alive()
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def move(self, moving_left, moving_right):
        #reset movement variables
        screen_scroll = 0
        dx = 0
        dy = 0
        #assign movement variable if moving left or right
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1
        #jump
        if self.jump == True and self.in_air == False:
            self.vel_y = -13
            self.jump = False
            self.in_air = True
        #apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        #check for collision
        for tile in world.obstacle_list:
            #check collision in the x direction
            if tile[1].colliderect(self.rect.x+dx, self.rect.y, self.width, self.height):
                dx = 0
                #if the ai has hit a wall then make it turn around
                if self.cha_type == 'enemy':
                    self.direction *= -1
                    self.move_counter = 0
            #check for collision in the y direction
            if tile[1].colliderect(self.rect.x, self.rect.y+dy, self.width, self.height):
                #check if below the ground, i.e. jumping 
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                    #check if above the ground, i.e. falling
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom

        #check for collision with water
        if pygame.sprite.spritecollide(self, water_group, False):
            self.health = 0

        #check for collision with exit
        level_complete = False
        if pygame.sprite.spritecollide(self, exit_group, False):
            level_complete = True

        #check if fallen off the map
        if self.rect.bottom > SCREEN_HEIGHT:
            self.health = 0

        #check if going off the edges of the screen
        if self.cha_type == 'player1':
            if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
                dx = 0

        #update rectangle position
        self.rect.x += dx
        self.rect.y += dy

        #update scroll based on player position
        if self.cha_type == 'player1':
            if (self.rect.right > SCREEN_WIDTH - SCROLL_THRESH and bg_scroll < (world.level_length * TILE_SIZE) - SCREEN_WIDTH)\
                or (self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
                self.rect.x -= dx
                screen_scroll = -dx

        return screen_scroll, level_complete

    def shoot(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = 20
            arrow = Arrow(self.rect.centerx+(1*self.rect.size[0]*self.direction), self.rect.centery, self.direction)
            arrow_group.add(arrow)
            shot_fx.play()

    def ai(self):
        if self.alive and player.alive:
            if random.randint(1, 200) == 1 and self.idling == False:
                self.update_action(0)
                self.idling = True
                self.idling_counter = 100
            #check if the ai in near the player
            if self.vision.colliderect(player.rect):
                #stop running and face the player
                self.update_action(3)
                if self.frame_index == 6:
                    self.shoot()
            else:
                if self.idling == False:
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left, ai_moving_right)
                    self.update_action(1)
                    self.move_counter += 1
                    #update ai vision as the enemy moves
                    self.vision.center = (self.rect.centerx+75*self.direction, self.rect.centery)
                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                            self.idling = False
        #scroll
        self.rect.x += screen_scroll


    def update_animation(self):
        #update animation
        if self.action == 2:
            ANIMATION_COOLDOWN = 100
        elif self.action == 3:
            ANIMATION_COOLDOWN = 60
        else:
            ANIMATION_COOLDOWN = 120
        #update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        #check if enough time has passed since the last update
        if pygame.time.get_ticks()-self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #if the animation has run out the rest back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 4:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

    def update_action(self, new_action):
        #ceck if new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            #updape the animation setting
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(4)

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

class World():
    def __init__(self):
        self.obstacle_list = []

    def process_data(self, data):
        self.level_length = len(data[0])
        #iterate through each value in level data file
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)
                    if tile >= 0 and tile <= 8 or tile == 12:
                        self.obstacle_list.append(tile_data)
                    elif tile >= 9 and tile <= 10:
                        water = Water(img, x * TILE_SIZE, y * TILE_SIZE)
                        water_group.add(water)
                    elif tile == 11 or (tile > 12 and tile <= 14):
                        decoration = Decoration(img, x * TILE_SIZE, y * TILE_SIZE)
                        decoration_group.add(decoration)
                    elif tile == 16:#create player
                        player = Archer('player1', x * TILE_SIZE, y * TILE_SIZE, 1.65, 5)
                        health_bar = Healthbar(10, 10, player.health, player.health)
                    elif tile == 17:#create enemies
                        enemy = Archer('enemy', x * TILE_SIZE, y * TILE_SIZE, 1.65, 2)
                        enemy_group.add(enemy)
                    elif tile == 18:#create health box
                        item_box = ItemBox('Health', x * TILE_SIZE, y * TILE_SIZE)
                        item_group.add(item_box)
                    elif tile == 15:#create exit
                        exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
                        exit_group.add(exit)

        return player, health_bar

    def draw(self):
        for tile in self.obstacle_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])


class Decoration(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll

class Water(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll

class Exit(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll

class ItemBox(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y,):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        #scroll
        self.rect.x += screen_scroll
        #check if the player has picked up item
        if pygame.sprite.collide_rect(self, player):
            #check what kind of box it was
            if self.item_type == 'Health' and player.health < 100:
                player.health += 20
                if player.health > player.max_health:
                    player.health = player.max_health
                #delete the item
                self.kill()

class Healthbar():
    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health

    def draw(self, health):
        #update with new health
        self.health = health
        #calculate health ratio
        ratio = self.health/self.max_health
        pygame.draw.rect(screen, BLACK, (self.x-2, self.y-2, 154, 24))
        pygame.draw.rect(screen, RED, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, GREEN, (self.x, self.y, 150*ratio, 20))

class Arrow(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = arrow_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        #move arrow
        self.rect.x += (self.direction*self.speed)+screen_scroll
        #check if arrow has gone of screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
        #check for collision withlevel
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()
        #check collection with characters
        if pygame.sprite.spritecollide(player, arrow_group, False):
            if player.alive:
                player.health -= 5
                self.kill()
        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy, arrow_group, False):
                if enemy.alive:
                    enemy.health -= 30
                    self.kill()

class ScreenFade():
    def __init__(self, direction, colour, speed):
        self.direction = direction
        self.colour = colour
        self.speed = speed
        self.fade_counter = 0


    def fade(self):
        fade_complete = False
        self.fade_counter += self.speed
        if self.direction == 1:#whole screen fade
            pygame.draw.rect(screen, self.colour, (0 - self.fade_counter, 0, SCREEN_WIDTH // 2, SCREEN_HEIGHT))
            pygame.draw.rect(screen, self.colour, (SCREEN_WIDTH // 2 + self.fade_counter, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.draw.rect(screen, self.colour, (0, 0 - self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
            pygame.draw.rect(screen, self.colour, (0, SCREEN_HEIGHT // 2 +self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT))
        if self.direction == 2:#vertical screen fade down
            pygame.draw.rect(screen, self.colour, (0, 0, SCREEN_WIDTH, 0 + self.fade_counter))
        if self.fade_counter >= SCREEN_WIDTH:
            fade_complete = True

        return fade_complete


#create screen fades
intro_fade = ScreenFade(1, BLACK, 4)
death_fade = ScreenFade(2, WHITE, 4)

#create buttons
start_button = button.Button(SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 - 150, start_img, 1)
exit_button = button.Button(SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 50, exit_img, 1)
restart_button = button.Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, restart_img, 2)

#create sprite groups
enemy_group = pygame.sprite.Group()
arrow_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()


#create empty tile lists
world_data = []
for row in range(ROWS):
    r = [-1]*COLS
    world_data.append(r)
#load in level data and create world
with open(f'level{level}_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)
world = World()
player, health_bar = world.process_data(world_data)
# player = Archer('player1', 300, 300, 3, 5)
# health_bar = Healthbar(10, 10, player.health, player.max_health)


run = True
while run:

    clock.tick(FPS)
    if start_game == False:
        #draw menu
        screen.fill(BLACK)
        #add buttons
        if start_button.draw(screen):
            start_game = True
        if exit_button.draw(screen):
            run = False
    else:
        #update background
        draw_bg()
        #draw world map
        world.draw()
        #show player health
        health_bar.draw(player.health)

        player.update()
        player.draw()

        for enemy in enemy_group:
            enemy.ai()
            enemy.update()
            enemy.draw()


        #update and draw groups
        arrow_group.update()
        item_group.update()
        decoration_group.update()
        water_group.update()
        exit_group.update()
        arrow_group.draw(screen)
        item_group.draw(screen)
        decoration_group.draw(screen)
        water_group.draw(screen)
        exit_group.draw(screen)

        #show intro
        if start_intro == True:
            if intro_fade.fade():
                start_intro = False
                intro_fade.fade_counter = 0

        #update player actions
        if player.alive:
            if player.in_air:
                player.update_action(2) #jump
            # shoot arrow
            elif shoot:
                player.update_action(3) #shoot
                if player.frame_index == 6:
                    player.shoot()
            elif moving_left or moving_right:
                player.update_action(1) #run

            else:
                player.update_action(0) #idle
            screen_scroll, level_complete = player.move(moving_left, moving_right)
            bg_scroll -= screen_scroll

            if level_complete:
                start_intro = True
                level += 1
                bg_scroll = 0
                world_data = reset_level()
                if level <= MAX_LEVELS:
                    #load in level data and create world
                    with open(f'level{level}_data.csv', newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)
                    world = World()
                    player, health_bar = world.process_data(world_data) 
        
        else:
            screen_scroll = 0
            if death_fade.fade():
                if restart_button.draw(screen):
                    death_fade.fade_counter = 0
                    start_intro = True
                    bg_scroll = 0
                    world_data = reset_level()
                    #load in level data and create world
                    with open(f'level{level}_data.csv', newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)
                    world = World()
                    player, health_bar = world.process_data(world_data)


    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            run = False
        #keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_f:
                shoot = True
            if event.key == pygame.K_w and player.alive:
                player.jump = True
                jump_fx.play()
            if event.key == pygame.K_ESCAPE:
                run = False

        #keybord button released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_f:
                shoot = False
    pygame.display.update()

pygame.quit()
