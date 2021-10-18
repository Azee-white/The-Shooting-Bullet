# @author:Azee-white

import pygame
import os
pygame.font.init()
# from pygame.constants import K_LCTRL

# from pygame.key import get_pressed

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PyGame1")

white = (255, 255, 255)
black = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)


FPS = 60
BULL = 9
MAX_BULLETS = 5
VEL = 5
size = 55, 40

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2


def draw_window(red, yellow, r_bullets, y_bullets, red_health, yellow_health):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, black, BORDER)

    red_health_text = HEALTH_FONT.render(
        "Health: " + str(red_health), 1, white)
    yellow_health_text = HEALTH_FONT.render(
        "Health: " + str(yellow_health), 1, white)

    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in r_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in y_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    pygame.display.update()


YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    'D:\AkshatMain\Program\PyGame\Assets\spaceship_yellow.png')
YELLOW_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (size)), 90)
RED_SPACESHIP_IMAGE = pygame.image.load(
    'D:\AkshatMain\Program\PyGame\Assets\spaceship_red.png')
RED_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(RED_SPACESHIP_IMAGE, (size)), 270)

SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))


def yellow_handle_move(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x + 15:
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15:
        yellow.y += VEL


def red_handle_move(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:
        red.y -= VEL
        
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15:
        red.y += VEL


def handle_bullets(y_bullets, r_bullets, yellow, red):
    for bullet in y_bullets:
        bullet.x += BULL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            y_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            y_bullets.remove(bullet)
    for bullet in r_bullets:
        bullet.x -= BULL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            r_bullets.remove(bullet)
        elif bullet.x < 0:
            r_bullets.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, white)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)
    
def main():
    red = pygame.Rect(700, 300, 55, 40)
    yellow = pygame.Rect(100, 300, 55, 40)

    r_bullets = []
    y_bullets = []

    red_health = 20
    yellow_health = 20

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(y_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    y_bullets.append(bullet)

                if event.key == pygame.K_RCTRL and len(r_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x, red.y + red.height//2 - 2, 10, 5)
                    r_bullets.append(bullet)
                if event.type == pygame.K_RETURN:
                    main()

            if event.type == RED_HIT:
                    red_health -= 1
                    # BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                    yellow_health -= 1

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"

        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_move(keys_pressed, yellow)
        red_handle_move(keys_pressed, red)
        handle_bullets(y_bullets, r_bullets, yellow, red)
        draw_window(red, yellow, r_bullets, y_bullets,
                    red_health, yellow_health)
    main()


if __name__ == "__main__":
    main()
