import pygame
from pygame.locals import *
import random

pygame.init()
pygame.mixer.init()
woosh_sound = pygame.mixer.Sound('woosh.mp3')
woosh_sound.set_volume(0.2)
pop_sound = pygame.mixer.Sound('pop.mp3')
pop_sound.set_volume(0.4)

width = 500
height = 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Game Menghindar')

background = pygame.image.load('images/background.png')
background = pygame.transform.scale(background, (width, height))

menu_img = pygame.image.load('images/menu.png')
menu_img = pygame.transform.scale(menu_img, (width, height))

red = (200, 0, 0)
white = (255, 255, 255)

left_lane = 150
center_lane = 250
right_lane = 350
lanes = [left_lane, center_lane, right_lane]

player_x = 250
player_y = 400

clock = pygame.time.Clock()
fps = 120

menu = True
gameover = False
speed = 2
score = 0

# ================= CLASS =================
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.frames = []
        for i in range(1, 5):
            img = pygame.image.load(f'images/{i}.png').convert_alpha()

            scale = 45 / img.get_width()
            img = pygame.transform.scale(
                img,
                (int(img.get_width() * scale), int(img.get_height() * scale))
            )
            self.frames.append(img)

        self.frame_index = 0
        self.animation_speed = 0.15

        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.frames = []
        for i in range(11, 17):
            img = pygame.image.load(f'images/{i}.png')

            scale = 45 / img.get_width()
            img = pygame.transform.scale(
                img,
                (int(img.get_width() * scale), int(img.get_height() * scale))
            )
            self.frames.append(img)

        self.frame_index = 0
        self.animation_speed = 0.2

        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

player = Player(player_x, player_y)
player_group.add(player)

crash = pygame.image.load('images/kena.png')
crash_rect = crash.get_rect()

gameover_img = pygame.image.load('images/kalah.png')
gameover_img = pygame.transform.scale(gameover_img, (300, 150))
gameover_rect = gameover_img.get_rect(center=(width//2, height//2 - 50))

running = True
while running:
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        if event.type == KEYDOWN:

            if menu and event.key == K_RETURN:
                pop_sound.play()
                menu = False

            elif not menu and not gameover:
                if event.key == K_LEFT and player.rect.centerx > left_lane:
                    player.rect.x -= 100
                    woosh_sound.play()

                elif event.key == K_RIGHT and player.rect.centerx < right_lane:
                    player.rect.x += 100
                    woosh_sound.play()

    if menu:
        screen.blit(menu_img, (0, 0))

        pygame.display.update()
        continue

    screen.blit(background, (0, 0))

    player_group.update()
    player_group.draw(screen)

    if len(enemy_group) < 2:
        add_enemy = True
        for enemy in enemy_group:
            if enemy.rect.top < enemy.rect.height * 1.5:
                add_enemy = False

        if add_enemy:
            lane = random.choice(lanes)
            enemy = Enemy(lane, height / -2)
            enemy_group.add(enemy)


    if not gameover:
        for enemy in enemy_group:
            enemy.rect.y += speed

            if enemy.rect.top >= height:
                enemy.kill()
                score += 1

                if score > 0 and score % 5 == 0:
                    speed += 1

    enemy_group.update()
    enemy_group.draw(screen)

    font = pygame.font.Font(pygame.font.get_default_font(), 16)
    text = font.render('Score: ' + str(score), True, white)
    screen.blit(text, (20, 400))

    if not gameover:
        if pygame.sprite.spritecollide(player, enemy_group, True):
            gameover = True
            crash_rect.center = [player.rect.center[0], player.rect.top]

    if gameover:
        screen.blit(crash, crash_rect)
        screen.blit(gameover_img, gameover_rect)

        font = pygame.font.Font(pygame.font.get_default_font(), 20)
        text = font.render('Tekan ENTER untuk bermain lagi', True, white)
        text_rect = text.get_rect(center=(width//2, height//2 + 80))
        screen.blit(text, text_rect)

    pygame.display.update()

    while gameover:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == QUIT:
                gameover = False
                running = False

            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    pop_sound.play()
                    gameover = False
                    speed = 2
                    score = 0
                    enemy_group.empty()
                    player.rect.center = [player_x, player_y]

pygame.quit()