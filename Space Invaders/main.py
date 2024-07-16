# Import required libraries
import pygame
import random
import math
import os

# Initialize pygame
pygame.init()

# Create screen
screen = pygame.display.set_mode((800,600))

# Clock
clock = pygame.time.Clock()


# Background
background = pygame.image.load(os.path.join('assets', 'images', 'background.jpg'))
background = pygame.transform.scale(background, (800,600))


# Background Sound
pygame.mixer.music.load(os.path.join('assets', 'sounds', 'background sound.mp3'))
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.6)


# Title and icon
pygame.display.set_caption('Space Invaders')
title_icon = pygame.image.load(os.path.join('assets', 'images', 'ufo.png'))
pygame.display.set_icon(title_icon)


# Score
score_val = 0
score_font = pygame.font.Font('freesansbold.ttf', 22)
def show_score():
    score = score_font.render("Score: " + str(score_val), True, (255, 255, 255))
    screen.blit(score, (10,10))


# Game over
game_over_flag = False
game_over_font = pygame.font.Font(os.path.join('assets', 'fonts', 'ALGER.ttf'), 64)
text_font_1 = pygame.font.Font(os.path.join('assets', 'fonts', 'calibrili.ttf'), 32)
text_font_2 = pygame.font.Font(os.path.join('assets', 'fonts', 'timesi.ttf'), 42)
def game_over():
    over = game_over_font.render("Game Over", False, (255,0,0))
    text1 = text_font_1.render("Game window closes automatically in 5 Seconds", False, (255,255,255))
    text2 = text_font_1.render("Thank You for playing!", False, (255,255,255))
    text3 = text_font_2.render("Your Final Score: " + str(score_val), False, (255,255,255))
    text4 = text_font_2.render("Waves survived: " + str(score_val//21), False, (255,255,255))
    text5 = text_font_2.render("Your Accuracy: " + str(accuracy) + '%', False, (255,255,255))
    screen.blit(over, (220,180))
    screen.blits(((text3, (230,269)), (text4, (230,305))))
    screen.blit(text5, (230,341))
    screen.blits(((text1, (75,410)), (text2, (250,445))))


# Wave number
wave_number_font = pygame.font.Font('freesansbold.ttf', 22)
def show_wave_number():
    global score_val
    wave_number = score_val//21 + 1
    wave = wave_number_font.render("Wave Number: " + str(wave_number), True, (255,255,255))
    screen.blit(wave, (270,10))


# Player Health
player_health_font = pygame.font.Font('freesansbold.ttf', 22)
player_health = 3
def show_player_health():
    global player_health
    health = player_health_font.render("Player Health: " + str(player_health), True, (255,255,255))
    screen.blit(health, (600,10))

# Player info
playerImg = pygame.image.load(os.path.join('assets', 'images', 'playerImg.png'))
image_size = (64,64)
playerImg = pygame.transform.scale(playerImg, image_size)
player_x = 368
player_y = 480
player_x_change = 0
player_y_change = 0

def player(x, y):
    screen.blit(playerImg, (x, y))
def boundaries(x,y):
    if x <=0 and (y<=536 and y>=400):
        x = 0
    elif x >=736 and (y<=536 and y>=400):
        x = 736
    elif y <=400 and (x>=0 and x<=736):
        y = 400
    elif y >=536 and (x>=0 and x<=736):
        y = 536
    return x,y


# Enemy info
enemy_hit = 0

eImg = pygame.image.load(os.path.join('assets', 'images', 'enemyImg.png'))
eImg = pygame.transform.scale(eImg, (52,52))
enemyImg = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
num_of_enemy = 21
enemy_speed = 0.2

for i in range(3):    
    x = 36
    y = 40
    for j in range(7):
        enemyImg.append(eImg)
        enemy_y.append(y + i*70)
        enemy_x_change.append((1+(score_val//21))*enemy_speed)
        # enemy_y_change.append(0)
        if i%2!=0:    
            enemy_x.append(52 + x + j*104) # 40+x+j*79.5
        else:
            enemy_x.append(x + j*104)  # x+j*79.5

def enemy(i, x, y):
    screen.blit(enemyImg[i], (x, y))
def spawn_enemy():    # moves the respective enmy to location, doesnt reprint them
    for i in range(3):    
        x = 36
        y = 40
        for j in range(7):
            enemyImg[((i*7)+(j+1))-1] = eImg
            enemy_y[((i*7)+(j+1))-1] = y + i*70
            enemy_x_change[((i*7)+(j+1))-1] = (1+(score_val//21))*enemy_speed
            # enemy_y_change[((i*7)+(j+1))-1] = 0
            if i%2!=0:    
                enemy_x[((i*7)+(j+1))-1] = 52 + x + j*104    # 40+x+j*79.5
            else:
                enemy_x[((i*7)+(j+1))-1] = x + j*104     # x+j*79.5


# Player Bullet
bullet_fired_count = 0

p_bImg = pygame.image.load(os.path.join('assets', 'images', 'playerBullet.png'))
p_bImg = pygame.transform.scale(p_bImg, (24,32))
PbulletImg = []
Pbullet_x = []
Pbullet_y = []
Pbullet_y_change = []
Pbullet_state = []

for i in range(1):
    PbulletImg.append(p_bImg)
    Pbullet_x.append(0)
    Pbullet_y.append(480)
    Pbullet_y_change.append(10)
    Pbullet_state.append('ready')

def fire_bullet_player(i,x,y):
    global Pbullet_state
    Pbullet_state[i] = 'fire'
    screen.blit(PbulletImg[i], (x + 20, y + 10))


# Enemy Bullet info
enemybulletfire = 0
enemy_fire_bullet_event = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_fire_bullet_event, 2000)

e_bImg = pygame.image.load(os.path.join('assets', 'images', 'enemyBullet.png'))
e_bImg = pygame.transform.scale(e_bImg, (48,48))
EbulletImg = []
Ebullet_x = []
Ebullet_y = []
Ebullet_state = []

for i in range(1):
    EbulletImg.append(e_bImg)
    Ebullet_x.append(2000)
    Ebullet_y.append(2000)
    # Ebullet_y_change.append(Ebullet_speed)
    Ebullet_state.append(True)

def fire_bullet_enemy(i,x,y):
    global Ebullet_state
    Ebullet_state = False
    screen.blit(EbulletImg[i], (x+2,y+2))


# Check Collision for enemy
def isCollision_enemy(x1,x2,y1,y2):
    distance = math.sqrt((math.pow(x2-x1, 2)) + (math.pow(y2-y1, 2)))
    if distance < 30:
        global enemy_hit
        enemy_hit += 1
        return True
    else: 
        return False


# Check collision for player
def isCollision_player(x1,x2,y1,y2):
    distance = math.sqrt((math.pow(x2-x1, 2)) + (math.pow(y2-y1, 2)))
    if distance < 38:
        return True
    else:
        return False


# Accuracy
accuracy = 0


# Main Game Loop
running = True
while running:
    screen.fill((0,0,0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player_x_change = -6
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player_x_change = 6
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                player_y_change = -3
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                player_y_change = 3
            if event.key == pygame.K_SPACE:
                bullet_fired_count += 1
                for i in range(1):
                    if Pbullet_state[i] == 'ready':
                        Pbullet_x[i] = player_x
                        Pbullet_y[i] = player_y
                        fire_bullet_player(i, Pbullet_x[i], Pbullet_y[i])
                        player_bullet_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'player bullet.wav'))
                        player_bullet_sound.play()
                        player_bullet_sound.set_volume(0.3)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_w or event.key == pygame.K_s:
                player_y_change = 0
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
                player_x_change = 0

        if event.type == enemy_fire_bullet_event:
            enemybulletfire += 1
            bullet = False
            while bullet == False:
                r = random.randint(0,20)
                if enemy_y[r] != 3000:
                    Ebullet_x[0] = enemy_x[r]
                    Ebullet_y[0] = enemy_y[r]
                    fire_bullet_enemy(0,Ebullet_x[0], Ebullet_y[0])
                    enemy_bullet_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'enemy bullet.wav'))
                    enemy_bullet_sound.play()
                    bullet = True

    
    player_x += player_x_change
    player_y += player_y_change
    player_x, player_y = boundaries(player_x, player_y)


    # Enemy Movement
    for i in range(3):
        for j in range(7):    
            enemy(((i*7)+(j+1))-1, enemy_x[((i*7)+(j+1))-1], enemy_y[((i*7)+(j+1))-1])
            if i%2!=0:    
                enemy_x[((i*7)+(j+1))-1] += enemy_x_change[((i*7)+(j+1))-1]
                if enemy_x[((i*7)+(j+1))-1] >= (52 + x + j*104)+36:
                    enemy_x_change[((i*7)+(j+1))-1] = -((1+(score_val//21))*enemy_speed)
                if enemy_x[((i*7)+(j+1))-1] <= (52 + x + j*104)-88:
                    enemy_x_change[((i*7)+(j+1))-1] = +((1+(score_val//21))*enemy_speed)
            else:
                enemy_x[((i*7)+(j+1))-1] -= enemy_x_change[((i*7)+(j+1))-1]
                if enemy_x[((i*7)+(j+1))-1] >= (x + j*104)+88:
                    enemy_x_change[((i*7)+(j+1))-1] = +((1+(score_val//21))*enemy_speed)
                if enemy_x[((i*7)+(j+1))-1] <= (x + j*104)-36:
                    enemy_x_change[((i*7)+(j+1))-1] = -((1+(score_val//21))*enemy_speed)

            # Collision
            enemy_collision = isCollision_enemy(Pbullet_x[0], enemy_x[((i*7)+(j+1))-1], Pbullet_y[0], enemy_y[((i*7)+(j+1))-1])
            if enemy_collision:
                e_collision_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'enemy hit.wav'))
                e_collision_sound.play()
                e_collision_sound.set_volume(0.3)
                Pbullet_y[0] = 480
                Pbullet_state[0] = 'ready'
                score_val += 1
                enemy_x[((i*7)+(j+1))-1] = 3000
                enemy_y[((i*7)+(j+1))-1] = 3000

            # Game over
            if player_health == 0:
                pygame.mixer.music.stop()
                if game_over_flag == False:
                    game_over_flag = True
                    game_over_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'game over.wav'))
                    game_over_sound.play()
                for k in range(num_of_enemy):
                    enemy_y[k] = 3000
                    game_over()
                    pygame.display.update()
                    pygame.time.delay(13)
                    running = False


    # Player Bullet Movement
    for i in range(1):
        if Pbullet_y[i]<=-32:
            Pbullet_y[i] = 480
            Pbullet_state[i] = 'ready'
        if Pbullet_state[i] == "fire":
            fire_bullet_player(i, Pbullet_x[i], Pbullet_y[i])
            Pbullet_y[i] -= Pbullet_y_change[i]


    # Enemy Bullet Movement
    for i in range(1):
        if Ebullet_y[i] >= 600:
            Ebullet_y[i] = 2000
            Ebullet_state = True
        if Ebullet_state == False:
            fire_bullet_enemy(i,Ebullet_x[i], Ebullet_y[i])
            Ebullet_y[i] += ((1+(score_val//21))*0.5) + 2.5

        # collision
        player_collision = isCollision_player(Ebullet_x[0], player_x, Ebullet_y[0], player_y)
        if player_collision:
            p_collision_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'player hit.wav'))
            p_collision_sound.play()
            p_collision_sound.set_volume(0.25)
            Ebullet_x[0] = 2000
            Ebullet_y[0] = 2000
            Ebullet_state = True
            player_health -= 1


    # Enemy Spawn
    if score_val > 0  and  score_val % num_of_enemy == 0:
        spawn_enemy()


    # Accuracy
    if bullet_fired_count == 0:
        accuracy = 0
    else:
        accuracy = round((score_val / bullet_fired_count)*100, 2)


    player(player_x, player_y)
    show_score()
    show_wave_number()
    show_player_health()

    pygame.display.update()
    clock.tick(120)

print("Player bullet fired: ", bullet_fired_count)
print("Enemies destroyed: ", score_val)
print("Enemy bullet fired: ", enemybulletfire)
print("Player Heath: ", player_health)