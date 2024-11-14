import pygame, sys
from pygame.locals import *
import random

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racing Game")

player_image = pygame.image.load("Player.png")
enemy_image = pygame.image.load("Enemy.png")
coin_image = pygame.image.load("Coin.png")
road_image = pygame.image.load("Road.jpg")

player_image = pygame.transform.scale(player_image, (50, 70))
enemy_image = pygame.transform.scale(enemy_image, (50, 70))
coin_image = pygame.transform.scale(coin_image, (30, 30))
road_image = pygame.transform.scale(road_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

score = 0
font = pygame.font.SysFont('Arial', 36)

def game_over_screen():
    game_over_text = font.render("Game Over", True, RED)
    final_score_text = font.render(f"Your Score: {score}", True, GREEN)
    exit_text = font.render("Press Q to Exit", True, BLUE)

    DISPLAYSURF.fill(WHITE)
    DISPLAYSURF.blit(game_over_text, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 3 - 50))
    DISPLAYSURF.blit(final_score_text, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2))
    DISPLAYSURF.blit(exit_text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + 50))

    pygame.display.update()

def reset_game():
    global player, enemy, background_y, score, coins
    player = Player()
    enemy = Enemy()
    coins = pygame.sprite.Group()
    background_y = 0
    score = 0
    for _ in range(5):
        coins.add(Coin())

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_image
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        self.rect.move_ip(0, 10)
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        self.last_position_y = self.rect.y

    def update(self):
        pressed_keys = pygame.key.get_pressed()

        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)

        if self.rect.y < self.last_position_y - 15:
            global score
            score += 10
            self.last_position_y = self.rect.y

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = coin_image
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def update(self):
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
        else:
            self.rect.move_ip(0, 5) 

    def draw(self, surface):
        surface.blit(self.image, self.rect)

def save_high_score(score):
    with open("high_score.txt", "w") as f:
        f.write(str(score))

def load_high_score():
    try:
        with open("high_score.txt", "r") as f:
            return int(f.read())
    except FileNotFoundError:
        return 0

all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
coins = pygame.sprite.Group()

player = Player()
enemy = Enemy()

all_sprites.add(player)
all_sprites.add(enemy)
enemies.add(enemy)

for _ in range(5):
    coin = Coin()
    all_sprites.add(coin)
    coins.add(coin)

background_y = 0


load_high_score()

coin_spawn_timer = pygame.time.get_ticks()
coin_spawn_delay = 2000 

game_running = True
while game_running:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    if pygame.time.get_ticks() - coin_spawn_timer > coin_spawn_delay:
        coin_spawn_timer = pygame.time.get_ticks()  
        new_coin = Coin()
        all_sprites.add(new_coin)
        coins.add(new_coin)

    if pygame.sprite.spritecollide(player, enemies, False):
        game_over_screen()

        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_q:
                        save_high_score(score)  
                        pygame.quit()
                        sys.exit()
                if event.type == QUIT:
                    save_high_score(score)
                    pygame.quit()
                    sys.exit()

    if game_running:
        player.update()
        for e in enemies:
            e.move()
        for c in coins:
            c.update()

        collected_coins = pygame.sprite.spritecollide(player, coins, True)  
        for coin in collected_coins:
            score += 10  

        background_y += 5
        if background_y >= SCREEN_HEIGHT:
            background_y = 0

        DISPLAYSURF.fill(WHITE)
        DISPLAYSURF.blit(road_image, (0, background_y - SCREEN_HEIGHT))
        DISPLAYSURF.blit(road_image, (0, background_y))

        all_sprites.draw(DISPLAYSURF)

        score_text = font.render(f"Score: {score}", True, BLUE)
        DISPLAYSURF.blit(score_text, (SCREEN_WIDTH - score_text.get_width() - 20, 20))

        pygame.display.update()

    FramePerSec.tick(FPS)
