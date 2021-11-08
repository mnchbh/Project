import pygame
import os
pygame.init()

SCREEN_WIDTH = 800
SCREE_HEIGHT = int(SCREEN_WIDTH*0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREE_HEIGHT))
pygame.display.set_caption('Tester')

#set framerate
clock = pygame.time.Clock()
FPS = 60
#define game varibles
GRAVITY = 0.75
#define player action variables
moving_left = False
moving_right = False
hit = False

#define color
BG = (144, 201, 120)
RED = (255, 0, 0)

def draw_bg():
    screen.fill(BG)
    pygame.draw.line(screen, RED, (0, 500), (SCREE_HEIGHT, 500))

class Knight(pygame.sprite.Sprite):
    def __init__(self, cha_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.cha_type = cha_type
        self.speed = speed
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

        #load all imagefor the players
        animation_types = ['idle', 'run', 'jump', 'hit', 'dead']
        for animation in animation_types:
            #reset temporary list of images
            temp_list = []
            #count number of files in the folder
            num_frame = len(os.listdir(f'img/{self.cha_type}/{animation}'))
            for i in range(num_frame):
                img = pygame.image.load(f'img/{self.cha_type}/{animation}/{i}.png')
                img = pygame.transform.scale(img, (img.get_width()*scale, int(img.get_height()*scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def move(self, moving_left, moving_right):
        #reset movement variables
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

        #check collision with floor
        if self.rect.bottom+dy > 500:
            dy = 500-self.rect.bottom
            self.in_air = False
        
        #update rectangle position
        self.rect.x += dx
        self.rect.y += dy

    def update_animation(self):
        #update animation
        if self.action == 2:
            ANIMATION_COOLDOWN = 50
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
            self.frame_index = 0

    def update_action(self, new_action):
        #ceck if new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            #updape the animation setting
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()


    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)



player = Knight('player', 200, 200, 3, 5)
# enemy = Knight('enemy/goblin',400, 200, 2, 6)

run = True
while run:

    clock.tick(FPS)

    draw_bg()
    player.update_animation()
    player.draw()

    #update player actions
    if player.alive:
        if player.in_air:
            player.update_action(2)
        elif moving_left or moving_right:
            player.update_action(1) #1 == run
        else:
            player.update_action(0) #0 == idle
        player.move(moving_left, moving_right)

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
                hit == True
            if event.key == pygame.K_w and player.alive:
                player.jump = True
            if event.key == pygame.K_ESCAPE:
                run = False

        #keybord button released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_f:
                hit == True

    pygame.display.update()

pygame.quit()
