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


def load_map():
    map_request = f"{server_address}ll={ll[0]},{ll[1]}&size={size}&z={zoom}&l=map&apikey={api_key}"
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


pygame.init()
screen = pygame.display.set_mode((600, 450))
pygame.display.set_caption("terrorblabe >> drow ranger")
map_file = load_map()
screen.blit(pygame.image.load(map_file), (0, 0))
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

            screen.blit(pygame.image.load(map_file), (0, 0))
            pygame.display.flip()

pygame.quit()
os.remove(map_file)
