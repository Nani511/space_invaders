import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Title and Icon
pygame.display.set_caption("Space Invaders by sanjeth")

# Player
player_img = pygame.Surface((64, 64))
player_img.fill((0, 255, 0))  # Green square as the player
player_x = 370
player_y = 480
player_x_change = 0
player_speed = 3

# Enemy
enemy_img = pygame.Surface((64, 64))
enemy_img.fill((255, 0, 0))  # Red square as the enemy

enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemy_x.append(random.randint(0, 736))
    enemy_y.append(random.randint(50, 150))
    enemy_x_change.append(0.5)  # Reduced speed to 0.5
    enemy_y_change.append(40)

# Bullet
bullet_img = pygame.Surface((8, 32))
bullet_img.fill((255, 255, 0))  # Yellow rectangle as the bullet
bullet_x = 0
bullet_y = 480
bullet_y_change = 10  # Bullet speed set to 10
bullet_state = "ready"  # Ready state means the bullet is ready to be fired

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

text_x = 10
text_y = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def player(x, y):
    screen.blit(player_img, (x, y))

def enemy(x, y):
    screen.blit(enemy_img, (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 28, y + 10))

def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt(math.pow(enemy_x - bullet_x, 2) + math.pow(enemy_y - bullet_y, 2))
    return distance < 27

# Game Loop
running = True
game_over = False
while running:
    screen.fill((0, 0, 0))  # RGB black background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Keystroke controls
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -player_speed
            if event.key == pygame.K_RIGHT:
                player_x_change = player_speed
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_x = player_x
                    fire_bullet(bullet_x, bullet_y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    if not game_over:
        # Player movement
        player_x += player_x_change
        player_x = max(0, min(player_x, 736))

        # Enemy movement
        for i in range(num_of_enemies):
            if enemy_y[i] > 440:
                game_over = True
                break

            enemy_x[i] += enemy_x_change[i]
            if enemy_x[i] <= 0:
                enemy_x_change[i] = 0.5  # Slower speed
                enemy_y[i] += enemy_y_change[i]
            elif enemy_x[i] >= 736:
                enemy_x_change[i] = -0.5  # Slower speed
                enemy_y[i] += enemy_y_change[i]

            # Collision
            collision = is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
            if collision:
                bullet_y = 480
                bullet_state = "ready"
                score_value += 1
                enemy_x[i] = random.randint(0, 736)
                enemy_y[i] = random.randint(50, 150)

            enemy(enemy_x[i], enemy_y[i])

        # Bullet movement
        if bullet_y <= 0:
            bullet_y = 480
            bullet_state = "ready"

        if bullet_state == "fire":
            fire_bullet(bullet_x, bullet_y)
            bullet_y -= bullet_y_change

        player(player_x, player_y)
        show_score(text_x, text_y)
    else:
        game_over_text()

    pygame.display.update()
pygame.quit()
