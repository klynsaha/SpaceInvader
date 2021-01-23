import random
import math
import time
import pygame
from pygame import mixer

# Initialize
pygame.init()

# Create a screen
screen = pygame.display.set_mode((800, 600)) # (width, height)

# Background
backgroundImg = pygame.image.load('res/images/background.png')
mixer.music.load('res/soundtrack/background.wav')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption('Space Invader')
icon = pygame.image.load('res/images/ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('res/images/player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Emeny
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for _ in range(num_of_enemies):
    enemyImg.append(pygame.image.load('res/images/enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(30, 150))
    enemyX_change.append(3)
    enemyY_change.append(20)

# Bullet
bulletImg = []
bulletX = []
bulletY = []
bulletX_change = []
bulletY_change = []
bullet_state = []
num_of_bullets = 10
top = 0
for _ in range(num_of_bullets):
    bulletImg.append(pygame.image.load('res/images/bullet.png'))
    bulletX.append(0)
    bulletY.append(480)
    bulletX_change.append(0)
    bulletY_change.append(10)
    bullet_state.append("ready")

# Scoring
# www.dafont.com
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
over_font = pygame.font.Font("freesansbold.ttf", 64)
textX = 10
textY = 10

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x,y))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y, i):
    global top
    global bullet_state
    bullet_state[i] = "fire"
    screen.blit(bulletImg[i], (x+16, y+10))
    bulletY[i] -= bulletY_change[i]

def isCollision(x1, y1, x2, y2):
    distance = math.sqrt((x1-x2)**2 + (y1-y2)**2)
    return distance < 30

def game_over_text():
    over_text = font.render("GAME OVER!", True, (255, 255, 255))
    screen.blit(over_text, (300, 250))

# Game loop
running = True
pause = 0
while(running):
    # RGB
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(backgroundImg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Key is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if top < num_of_bullets and bullet_state[top] == "ready":
                    bulletX[top] = playerX
                    bullet_state[top] = "fire"
                    top += 1
                    bullet_sound = mixer.Sound('res/soundtrack/laser.wav')
                    bullet_sound.play()
        # Key release
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    for x in range(num_of_bullets):
        # Bullet Movement
        if bulletY[x] < 0:
            bulletY[x] = 480
            bullet_state[x] = "ready"
            top -= 1

        if bullet_state[x] == "fire":
            fire_bullet(bulletX[x], bulletY[x], x)

    playerX += playerX_change
    # Player confined within screen
    if playerX <= 0:
        playerX = 0
    elif playerX > 736:
        playerX = 736

    # Enemy Movement
    for i in range(num_of_enemies):
        # Game over
        if enemyY[i] > 450:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        # Enemy confined within screen
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] > 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # Collision
        for j in range(num_of_bullets):
            collision = isCollision(enemyX[i], enemyY[i], bulletX[j], bulletY[j])
            if collision:
                explosionSound = mixer.Sound("res/soundtrack/explosion.wav")
                explosionSound.play()
                bulletY[j] = 480
                bullet_state[j] = "ready"
                top -= 1
                score_value += 1
                enemyX[i] = random.randint(0, 735)
                enemyY[i] = random.randint(30, 150)
        enemy(enemyX[i], enemyY[i], i)


    show_score(textX, textY)
    player(playerX, playerY)
    pygame.display.update()