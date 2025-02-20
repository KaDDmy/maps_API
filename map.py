import os
import sys

import pygame
import requests

server_address = 'https://static-maps.yandex.ru/v1?'
api_key = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'
ll = [37.616627, 55.760931]
size = '650,450'
zoom = 10
min_zoom = 2
max_zoom = 20
move_step = 0.1
min_lat, max_lat = -85, 85
min_lon, max_lon = -180, 180
theme = "light"

WIDTH, HEIGHT = 600, 450
BUTTON_WIDTH, BUTTON_HEIGHT = 100, 40
BUTTON_X, BUTTON_Y = WIDTH - BUTTON_WIDTH - 10, HEIGHT - BUTTON_HEIGHT - 10


def load_map():
    map_request = f"{server_address}ll={ll[0]},{ll[1]}&size={size}&z={zoom}&theme={theme}&apikey={api_key}"
    response = requests.get(map_request)
    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    return map_file


def draw_theme_button():
    """Рисует кнопку переключения темы."""
    pygame.draw.rect(screen, (50, 50, 50), (BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT))
    font = pygame.font.Font(None, 24)
    text = font.render("Тема", True, (255, 255, 255))
    text_rect = text.get_rect(center=(BUTTON_X + BUTTON_WIDTH // 2, BUTTON_Y + BUTTON_HEIGHT // 2))
    screen.blit(text, text_rect)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("terrorblabe >> drow ranger")
map_file = load_map()
screen.blit(pygame.image.load(map_file), (0, 0))
draw_theme_button()
pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                if zoom < max_zoom:
                    zoom += 1
                    map_file = load_map()
            if event.key == pygame.K_PAGEDOWN:
                if zoom > min_zoom:
                    zoom -= 1
                    map_file = load_map()
            if event.key == pygame.K_UP:
                ll[1] = min(ll[1] + move_step, max_lat)
                map_file = load_map()
            if event.key == pygame.K_DOWN:
                ll[1] = max(ll[1] - move_step, min_lat)
                map_file = load_map()
            if event.key == pygame.K_RIGHT:
                ll[0] = min(ll[0] + move_step, max_lon)
                map_file = load_map()
            if event.key == pygame.K_LEFT:
                ll[0] = max(ll[0] - move_step, min_lon)
                map_file = load_map()

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if BUTTON_X <= x <= BUTTON_X + BUTTON_WIDTH and BUTTON_Y <= y <= BUTTON_Y + BUTTON_HEIGHT:
                theme = "dark" if theme == "light" else "light"
                map_file = load_map()

        screen.blit(pygame.image.load(map_file), (0, 0))
        draw_theme_button()
        pygame.display.flip()

pygame.quit()
os.remove(map_file)