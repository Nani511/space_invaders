import pygame
import random
import math
from typing import Tuple, List

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SPEED = 3
BULLET_SPEED = 10
ENEMY_SPEED = 0.5
ENEMY_DROP = 40

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Space Invaders by Sanjeth")

        self.player_img = self.create_surface((64, 64), (0, 255, 0))
        self.player_x = 370
        self.player_y = 480
        self.player_x_change = 0

        self.enemy_img = self.create_surface((64, 64), (255, 0, 0))
        self.enemies = self.create_enemies(6)

        self.bullet_img = self.create_surface((8, 32), (255, 255, 0))
        self.bullet_x = 0
        self.bullet_y = 480
        self.bullet_y_change = BULLET_SPEED
        self.bullet_state = "ready"

        self.score_value = 0
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.over_font = pygame.font.Font('freesansbold.ttf', 64)

    def create_surface(self, size: Tuple[int, int], color: Tuple[int, int, int]) -> pygame.Surface:
        surface = pygame.Surface(size)
        surface.fill(color)
        return surface

    def create_enemies(self, num: int) -> List[dict]:
        enemies = []
        for _ in range(num):
            enemy = {
                "img": self.enemy_img,
                "x": random.randint(0, 736),
                "y": random.randint(50, 150),
                "x_change": ENEMY_SPEED,
                "y_change": ENEMY_DROP,
            }
            enemies.append(enemy)
        return enemies

    def show_score(self, x: int, y: int):
        score = self.font.render("Score: " + str(self.score_value), True, (255, 255, 255))
        self.screen.blit(score, (x, y))

    def game_over_text(self):
        over_text = self.over_font.render("GAME OVER", True, (255, 255, 255))
        self.screen.blit(over_text, (200, 250))

    def player(self, x: int, y: int):
        self.screen.blit(self.player_img, (x, y))

    def enemy(self, enemy: dict):
        self.screen.blit(enemy["img"], (enemy["x"], enemy["y"]))

    def fire_bullet(self, x: int, y: int):
        self.bullet_state = "fire"
        self.screen.blit(self.bullet_img, (x + 28, y + 10))

    def is_collision(self, enemy_x: int, enemy_y: int, bullet_x: int, bullet_y: int) -> bool:
        distance = math.sqrt(math.pow(enemy_x - bullet_x, 2) + math.pow(enemy_y - bullet_y, 2))
        return distance < 27

    def run(self):
        running = True
        game_over = False
        while running:
            self.screen.fill((0, 0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.player_x_change = -PLAYER_SPEED
                    if event.key == pygame.K_RIGHT:
                        self.player_x_change = PLAYER_SPEED
                    if event.key == pygame.K_SPACE:
                        if self.bullet_state == "ready":
                            self.bullet_x = self.player_x
                            self.fire_bullet(self.bullet_x, self.bullet_y)

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        self.player_x_change = 0

            if not game_over:
                self.player_x += self.player_x_change
                self.player_x = max(0, min(self.player_x, 736))

                for enemy in self.enemies:
                    if enemy["y"] > 440:
                        game_over = True
                        break

                    enemy["x"] += enemy["x_change"]
                    if enemy["x"] <= 0:
                        enemy["x_change"] = ENEMY_SPEED
                        enemy["y"] += enemy["y_change"]
                    elif enemy["x"] >= 736:
                        enemy["x_change"] = -ENEMY_SPEED
                        enemy["y"] += enemy["y_change"]

                    if self.is_collision(enemy["x"], enemy["y"], self.bullet_x, self.bullet_y):
                        self.bullet_y = 480
                        self.bullet_state = "ready"
                        self.score_value += 1
                        enemy["x"] = random.randint(0, 736)
                        enemy["y"] = random.randint(50, 150)

                    self.enemy(enemy)

                if self.bullet_y <= 0:
                    self.bullet_y = 480
                    self.bullet_state = "ready"

                if self.bullet_state == "fire":
                    self.fire_bullet(self.bullet_x, self.bullet_y)
                    self.bullet_y -= self.bullet_y_change

                self.player(self.player_x, self.player_y)
                self.show_score(10, 10)
            else:
                self.game_over_text()

            pygame.display.update()
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
