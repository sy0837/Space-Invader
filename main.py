import pygame
import random
import math
from pygame import mixer

# Initializing Pygames
pygame.init()

# Making the Screen
screen = pygame.display.set_mode((900, 600))  # (width ,height)
# Game Name or Caption
pygame.display.set_caption("Space Invaders")

back = pygame.image.load('background.png')
# Game Icon
icon = pygame.image.load('space.png')
pygame.display.set_icon(icon)

mixer.music.load('background.wav')
mixer.music.set_volume(0.05)
mixer.music.play(-1)

playerX = 400
playerY = 500
playerX_change = 0
playerY_change = 0
m_change = 7

enemies = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
no_of_enemies = 6
for i in range(no_of_enemies):
    enemies.append(pygame.image.load('nature.png'))
    enemyX.append(random.randint(0, 850))
    enemyY.append(random.randint(0, 100))
    enemyX_change.append(4)
    enemyY_change.append(25)

bullet = pygame.image.load('security.png')
bulletX = 0
bulletY = 500
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"
bullet_path = 0

score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 700
textY = 10

gameOverFont = pygame.font.Font('freesansbold.ttf', 64)


def setScore(x, y):
    set_score = font.render("Score : " + str(score), True, (255, 255, 255))
    screen.blit(set_score, (x, y))


def firebullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet, (x + 16, y - 10))


def iscollision(enemX, enemY, bulleX, bulleY):
    distance = math.sqrt((math.pow(enemX - bulleX, 2) + math.pow(enemY - bulleY, 2)))
    # print(distance)
    if distance < 30:
        return True
    else:

        return False


def enemy(x, y, i):
    screen.blit(enemies[i], (x, y))


def player(x, y):
    screen.blit(icon, (x, y))

#To Set End Text
def setOverText():
    end_text = gameOverFont.render("GAME OVER", True, (255, 255, 255))
    scoretext = gameOverFont.render("Score : " + str(score), True, (255, 255, 255))
    screen.blit(end_text, (250, 250))
    screen.blit(scoretext, (250, 350))

#for continous running of window
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(back, (0, 0))
    #Event listenters
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -m_change
            elif event.key == pygame.K_RIGHT:
                playerX_change = m_change
            elif event.key == pygame.K_UP:

                playerY_change = -m_change
            elif event.key == pygame.K_DOWN:

                playerY_change = m_change
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.set_volume(0.1)
                    bullet_sound.play()
                    firebullet(playerX, bulletY)
                    bullet_path = playerX
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0
                playerX_change = 0

    #Changing the X-Axis Direction of Rocket
    playerX += playerX_change
    # playerY += playerY_change
    if playerX > 850:
        playerX = 850
    elif playerX < -10:
        playerX = -10
    if playerY > 830:
        playerY = 830
    elif playerY < 70:
        playerY = 70


    #for random movement of enemies and collison
    for i in range(no_of_enemies):
        if enemyY[i] > 450:
            for j in range(no_of_enemies):
                enemyY[j] = 2000
            setOverText()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] > 850:
            enemyX_change[i] = -random.randint(2, 10)
            enemyY[i] += random.randint(15, enemyY_change[i])
        elif enemyX[i] < -10:
            enemyX_change[i] = random.randint(2, 10)
            enemyY[i] += random.randint(15, enemyY_change[i])

        #Collision
        collision = iscollision(enemyX[i], enemyY[i], bullet_path, bulletY)
        if collision:
            col_sound = mixer.Sound('explosion.wav')
            col_sound.set_volume(0.1)
            col_sound.play()
            bulletY = 500
            bullet_state = "ready"
            score += 1
            print(score)
            enemyX[i] = random.randint(0, 850)
            enemyY[i] = random.randint(0, 100)
        enemy(enemyX[i], enemyY[i], i)

    #For Bullet Movement
    if bulletY <= 0:
        bulletY = playerY
        bullet_state = "ready"

    if bullet_state == "fire":
        firebullet(bullet_path, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    setScore(textX, textY)
    pygame.display.update()
