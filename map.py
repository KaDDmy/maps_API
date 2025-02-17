import os
import sys

import pygame
import requests

server_address = 'https://static-maps.yandex.ru/v1?'
api_key = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'
ll = f'37.616627,55.760931'
size = '650,450'
zoom = 10
min_zoom = 2
max_zoom = 20

def load_map(zoom):
    map_request = f"{server_address}ll={ll}&size={size}&z={zoom}&l=map&apikey={api_key}"
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
map_file = load_map(zoom)
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
                    map_file = load_map(zoom)
            if event.key == pygame.K_PAGEDOWN:
                if zoom > min_zoom:
                    zoom -= 1
                    map_file = load_map(zoom)
            screen.blit(pygame.image.load(map_file), (0, 0))
            pygame.display.flip()

pygame.quit()

os.remove(map_file)
