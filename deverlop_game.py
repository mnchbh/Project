import pygame
import button
import csv
import pickle

pygame.init()

clock = pygame.time.Clock()
FPS = 60

#game Window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
LOWER_MARGIN = 100
SIDE_MARGIN = 300

screen = pygame.display.set_mode((SCREEN_WIDTH+SIDE_MARGIN, SCREEN_HEIGHT+LOWER_MARGIN))
pygame.display.set_caption('Lavel Editor')

#define game veriables

ROWS = 16
MAX_COLS = 150
TILE_SIZE = SCREEN_HEIGHT//ROWS
TILE_TYPES = 9
level = 0
current_tile = 0
scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 1

# load images
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
	img = pygame.image.load(f'img/pic/{x}.png').convert_alpha()
	img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
	img_list.append(img)

save_img = pygame.image.load('img/save_btn.png').convert_alpha()
load_img = pygame.image.load('img/load_btn.png').convert_alpha()

#define colour
GREEN = (144, 201, 120)
WHITE = (255, 255, 255)
RED = (200, 25, 25)

#define font
font = pygame.font.SysFont('Futura', 30)

#create empty tile list
world_data = []
for row in range(ROWS):
	r = [-1]*MAX_COLS
	world_data.append(r)

#create ground
for tile in range(0, MAX_COLS):
	world_data[ROWS-1][tile] = 0

#fuction for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

#create fuction for drawing bk
def draw_bg():
	screen.fill(GREEN)
	windth = pinel1_img.get_width()
	for i in range(10):
		screen.blit(pinel1_img, ((i*windth)-scroll*0.5, 0))
		screen.blit(pinel2_img, ((i*windth)-scroll*0.5, SCREEN_HEIGHT-pinel2_img.get_height()))
		screen.blit(pinel3_img, ((i*windth)-scroll*0.45, SCREEN_HEIGHT-pinel3_img.get_height()))
		screen.blit(pinel4_img, ((i*windth)-scroll*0.5, SCREEN_HEIGHT-pinel4_img.get_height()))
		screen.blit(pinel5_img, ((i*windth)-scroll*0.55, SCREEN_HEIGHT-pinel5_img.get_height()))
		screen.blit(pinel6_img, ((i*windth)-scroll*0.6, SCREEN_HEIGHT-pinel6_img.get_height()))
		screen.blit(pinel7_img, ((i*windth)-scroll*0.65, SCREEN_HEIGHT-pinel7_img.get_height()))
		screen.blit(pinel8_img, ((i*windth)-scroll*0.7, SCREEN_HEIGHT-pinel8_img.get_height()))
		screen.blit(pinel9_img, ((i*windth)-scroll*0.75, SCREEN_HEIGHT-pinel9_img.get_height()))
		screen.blit(pinel10_img, ((i*windth)-scroll*0.8, SCREEN_HEIGHT-pinel10_img.get_height()))

#draw grid
def draw_grid():
	#vertical lines
	for c in range(MAX_COLS+1):
		pygame.draw.line(screen, WHITE, (c*TILE_SIZE-scroll, 0), (c*TILE_SIZE-scroll, SCREEN_HEIGHT))
	#horizontal lines
	for c in range(MAX_COLS+1):
		pygame.draw.line(screen, WHITE, (0, c*TILE_SIZE), (SCREEN_HEIGHT, c*TILE_SIZE))

#function for drawing the world tiles
def draw_world():
	for y, row in enumerate(world_data):
		for x, tile in enumerate(row):
			if tile >= 0:
				screen.blit(img_list[tile], (x * TILE_SIZE - scroll, y * TILE_SIZE))

#create buttons
save_button = button.Button(SCREEN_WIDTH//2, SCREEN_HEIGHT+LOWER_MARGIN-50, save_img, 1)
load_button = button.Button(SCREEN_WIDTH//2+200, SCREEN_HEIGHT+LOWER_MARGIN-50, load_img, 1)

#make a button list
button_list = []
button_col = 0
button_row = 0
for i in range(len(img_list)):
	tile_button = button.Button(SCREEN_HEIGHT+(75 * button_col)+175, (75 * button_row)+150, img_list[i], 1)
	button_list.append(tile_button)
	button_col += 1
	if button_col == 3:
		button_row += 1
		button_col = 0

run = True
while run:

	clock.tick(FPS)

	draw_bg()
	draw_grid()
	draw_world()
	draw_text(f'Level: {level}', font, WHITE, 10, SCREEN_HEIGHT+LOWER_MARGIN-90)
	draw_text('Press UP or DOWN to change Level', font, WHITE, 10, SCREEN_HEIGHT+LOWER_MARGIN-55)

	#save and load data
	if save_button.draw(screen):
		#save level data
		# pickle_out = open(f'level{level}_data', 'wb')
		# pickle.dump(world_data, pickle_out)
		# pickle_out.close()
		with open(f'level{level}_data.csv', 'w', newline='') as csvfile:
			writer = csv.writer(csvfile, delimiter=',')
			for r in world_data:
				writer.writerow(r)
	if load_button.draw(screen):
		#load in level data
		#reset scroll back to the start of the level
		scroll = 0
		# world_data = []
		# pickle_in = open(f'level{level}_data', 'rb')
		# world_data = pickle.load(pickle_in)
		with open(f'level{level}_data.csv', 'w', newline='') as csvfile:
			reader = csv.reader(csvfile, delimiter=',')
			for x, row in enumerate(reader):
				for y, tile in enumerate(row):
					world_data[x][y] = int(tile)

	#draw tile panel and tile
	pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH, 0, SIDE_MARGIN, SCREEN_HEIGHT))
	
	#choose a tile
	button_count = 0
	for button_count, i in enumerate(button_list):
		if i.draw(screen):
			current_tile = button_count

	#highlight the selected tile
	pygame.draw.rect(screen, RED, button_list[current_tile].rect, 3)

	#scrooll the map
	if scroll_left == True and scroll > 0:
		scroll -= 5*scroll_speed
	if scroll_right == True and scroll < (MAX_COLS*TILE_SIZE)-SCREEN_WIDTH:
		scroll += 5*scroll_speed

	#add new tile to the screen
	#get mouse position
	pos = pygame.mouse.get_pos()
	x = (pos[0]+scroll)//TILE_SIZE
	y = pos[1]//TILE_SIZE

	#check that the coordinates are within the tile area
	if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:
		#update tile value
		if pygame.mouse.get_pressed()[0] == 1:
			if world_data[y][x] != current_tile:
				world_data[y][x] = current_tile
		
		if pygame.mouse.get_pressed()[2] == 1:
			world_data[y][x] = -1

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		#keyboard presses
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				level += 1
			if event.key == pygame.K_DOWN and level > 0:
				level -= 1
			if event.key == pygame.K_LEFT:
				scroll_left = True
			if event.key == pygame.K_RIGHT:
				scroll_right = True
			if event.key == pygame.K_RSHIFT:
				scroll_speed = 5
		
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT:
				scroll_left = False
			if event.key == pygame.K_RIGHT:
				scroll_right = False
			if event.key == pygame.K_RSHIFT:
				scroll_speed = 5

	pygame.display.update()

pygame.quit()
