import pygame
import numpy as np
from map import Map, Tileset
from caméra import Camera

pygame.init()

TILESIZE = (32, 32)
MAPSIZE = (30, 40)
SCREENSIZE = (800, 600)
SPEED = 5
TILESET ="Design/Placeholder_tile.png"

screen = pygame.display.set_mode(SCREENSIZE)
pygame.display.set_caption("Test Map")

tileset = Tileset(TILESET, tilesize=TILESIZE, margin=1, spacing=1)
mapset = np.zeros(MAPSIZE, dtype=int)

map_ = Map(mapsize=MAPSIZE, tileset=tileset, mapset=mapset)
map_.draw()

player_pos = [MAPSIZE[1]*TILESIZE[0]//2, MAPSIZE[0]*TILESIZE[1]//2]
cam = Camera(mapsize=MAPSIZE, screensize=SCREENSIZE, tilesize=TILESIZE, speed=SPEED)
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_q]:
        player_pos[0] -= SPEED
    if keys[pygame.K_d]:
        player_pos[0] += SPEED
    if keys[pygame.K_z]:
        player_pos[1] -= SPEED
    if keys[pygame.K_s]:
        player_pos[1] += SPEED



    cam.update(player_pos)
    screen.blit(map_.image, map_.rect, (cam.x, cam.y, *SCREENSIZE))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()