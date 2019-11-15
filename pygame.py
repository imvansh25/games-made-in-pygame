import pygame
import sys
import random
import time

pygame.mixer.pre_init(44100,16,2,4096)
pygame.init()

WIDTH = 1000
HEIGHT = 600

RED = (255,0,0)
BLACK = (0,0,0)
BLUE = (0,0,255)
YELLOW =(255,255,0)
player_size = 50
shift_size = 40

player_pos = [WIDTH/2, HEIGHT- 2*player_size]

enemy_size = 50
enemy_pos = [random.randint(0,WIDTH-enemy_size), 0]
enemy_list = [enemy_pos]

speed = 0

screen = pygame.display.set_mode((WIDTH,HEIGHT))

game_over = False

clock = pygame.time.Clock()
clock_time = 30
start_time = time.time()

myFont = pygame.font.SysFont("monospace", 35);

# music section
pygame.mixer.music.load("jazzinparis.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

def drop_enemies(enemy_list):
	delay = random.random()
	if len(enemy_list) < 10 and delay < 0.1:
		x_pos = random.randint(0,WIDTH-enemy_size)
		y_pos = 0
		enemy_list.append([x_pos,y_pos])

def draw_enemies(enemy_list):
	for enemy_pos in enemy_list:
		pygame.draw.rect(screen, BLUE ,(enemy_pos[0] , enemy_pos[1] , enemy_size , enemy_size))

def detect_collision(player_pos,enemy_pos):
	p_x = player_pos[0]
	p_y = player_pos[1]
	e_x = enemy_pos[0]
	e_y = enemy_pos[1]
	if (e_x>=p_x and e_x<(p_x+player_size)) or (p_x>=e_x and p_x<(e_x+enemy_size)):
		if (e_y>=p_y and e_y < (p_y+player_size)) or (p_y>=e_y and p_y<(e_y+enemy_size)):
			return True
	return False

def update_enemy_positions(enemy_list, score):
	# change enemy position
	for idx, enemy_pos in enumerate(enemy_list):
		if enemy_pos[1] >=0 and enemy_pos[1] <HEIGHT:
			enemy_pos[1] += speed*1.5
		else:
			enemy_list.pop(idx)
			score += 1
	return score


def collision_check(enemy_list,player_pos):
	for enemy_pos in enemy_list:
		if detect_collision(enemy_pos,player_pos):
			return True
	return False

score = 0

while not game_over:

	for event in pygame.event.get():

		if event.type == pygame.QUIT:
			pygame.quit()

		if event.type == pygame.KEYDOWN:
			x = player_pos[0]
			y = player_pos[1]
			if event.key == pygame.K_LEFT:
				x -= shift_size
			elif event.key == pygame.K_RIGHT:
				x +=  shift_size
			elif event.key == pygame.K_DOWN:
				y +=  shift_size
			elif event.key == pygame.K_UP:
				y -=  shift_size
			x=max(x,0)
			x=min(x,WIDTH-player_size)
			y=max(y,0)
			y=min(y,HEIGHT-player_size)
			player_pos = [ x , y ]

	# clear screen again and again
	screen.fill(BLACK)

	drop_enemies(enemy_list)
	score = update_enemy_positions(enemy_list,score)
	speed = (score//20)+1

	time_now = round(time.time()-start_time,2)
	text1 = "Score: "+ str(score)
	text2 = "Level: "+ str(speed)
	text3 = "Timer: "+ str(time_now)
	label1 = myFont.render(text1, 1, YELLOW)
	label2 = myFont.render(text2, 1, YELLOW)
	label3 = myFont.render(text3, 1, YELLOW)
	screen.blit(label1,(WIDTH-220,HEIGHT-40))
	screen.blit(label2,(10,HEIGHT-40))
	screen.blit(label3,(5,5))

	if collision_check(enemy_list,player_pos):
		game_over=True
		break;

	draw_enemies(enemy_list)

	pygame.draw.rect(screen, RED ,(player_pos[0] , player_pos[1] , player_size , player_size))

	# speed of for loop
	clock.tick(clock_time)

	# update the display
	pygame.display.update()

if game_over == True:
	pygame.quit()