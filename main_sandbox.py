import pygame
import os, sys, json
from game_objects_sandbox import *


pygame.init()

screen = pygame.display.set_mode((1200, 800))

bg = BackGround(screen, ["bg1.jpg", "bg2.jpg"])
LVL1 = Level(screen, "level_name_20_10.json", (0, 800), (0, 6))
pers = Character(screen, "pers_idle_1.png", pos=(300, 500), anchor=(0.25, 0), name="pers", manual=True)

LVL1.add_character(pers)
clock = pygame.time.Clock()

while True:
    clock.tick(60)
    bg.draw(1)
    LVL1.draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        LVL1.update_from_event(event)
    LVL1.update_fps()
    pygame.display.update()