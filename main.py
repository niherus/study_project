import pygame
import os, sys, json
from game_objects import *


pygame.init()

screen = pygame.display.set_mode((1200, 800))




all_liltes = []
for i in range(1, 20):
    all_liltes.append("plat_" + str(i) + ".png")

levels_list = os.listdir("levels")
start_pos = (0, int(levels_list[0][:-5].split("_")[2]) - 4)
LVL1 = Level(screen, all_liltes, levels_list[0], (0, 800), start_pos)            
pers = Pers(screen, idle_image = ["pers_idle_1.png",
                                  "pers_idle_2.png",
                                  "pers_idle_1.png",
                                  "pers_idle_3.png",
                                  "pers_idle_4.png",
                                  "pers_idle_5.png",
                                  "pers_idle_4.png",
                                  "pers_idle_5.png",
                                  "pers_idle_4.png",
                                  "pers_idle_5.png",
                                  "pers_idle_4.png",
                                  "pers_idle_5.png",
                                  "pers_idle_4.png",
                                  "pers_idle_5.png",
                                  "pers_idle_4.png",
                                  "pers_idle_5.png",
                                  "pers_idle_4.png",
                                  "pers_idle_5.png",
                                  "pers_idle_4.png",
                                  "pers_idle_5.png",
                                  ],
            idle_timing = [400, 25, 700, 200, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
            walk_image = ["pers_walk_2.png", "pers_walk_1.png", "pers_walk_4.png", "pers_walk_3.png", "pers_walk_1.png"],
            walk_timing = [10, 10, 10, 10, 10],
            hit_image={
                "punch1": ["pers_punch1_1.png", "pers_punch1_2.png"],
                "punch2": ["pers_punch2_1.png", "pers_punch2_2.png", "pers_punch2_3.png", "pers_punch2_4.png", "pers_punch2_5.png"]
                },
            hit_timing={
                "punch1": [7, 12],
                "punch2": [7, 12, 5, 10, 15]
                },
            cur_level = LVL1
            )
dog1 = Enemy(screen, idle_image = ["dog1_enemy_idle_1.png",
                                   "dog1_enemy_idle_2.png",
                                   "dog1_enemy_idle_3.png",
                                   "dog1_enemy_idle_4.png",
                                   "dog1_enemy_idle_5.png",
                                   "dog1_enemy_idle_6.png",
                                   "dog1_enemy_idle_7.png",
                                   ],
            idle_timing = [700, 25, 20, 1000, 20, 25, 100],
            walk_image = ["dog1_enemy_walk_1.png", "dog1_enemy_walk_2.png", "dog1_enemy_walk_3.png", "dog1_enemy_walk_4.png"],
            walk_timing = [10, 10, 10, 10],
            attack_image={
                "paw_hit":["dog1_enemy_attack_1.png", "dog1_enemy_attack_2.png",
                           "dog1_enemy_attack_3.png", "dog1_enemy_attack_4.png",
                           "dog1_enemy_attack_5.png", "dog1_enemy_attack_6.png",
                           "dog1_enemy_attack_7.png"],
                "bite":["dog1_enemy_bite_1.png", "dog1_enemy_bite_2.png",
                        "dog1_enemy_bite_3.png", "dog1_enemy_bite_4.png"]
                },
             attack_timing={
                "paw_hit":[15, 17, 15, 10, 5, 5, 30],
                "bite":[15, 30, 30, 30]
                },
             cur_level = LVL1,
             start_pos = (0, 8),
             behavior_plan = ["idle", *(["walk"]*10) , "idle", *(["sprint"]*3)],
             way_points=[(9, 8), (0, 8)],
             attacker=pers
             )
pers.set_enemy(dog1)
bg = BackGround(screen, ["bg1.jpg", "bg2.jpg"])

clock = pygame.time.Clock()
while True:
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and not pers.hit_status:
            pers.step = 0
            pers.time = 0
            if event.button == 1:
                pers.hit_status = "punch1"
            elif event.button == 3:
                pers.hit_status = "punch2"

        if event.type == pygame.KEYDOWN:
            if not pers.hit_status and not pers.dash:
                pers.step = 0
                pers.time = 0
    
            if event.key == 32 and pers.ground != None:
                pers.cur_level.shift(dy=131) 
                pers.jump = True 
     
            if event.key == 113 and not pers.cool_dash:
                pers.dash = True
                pers.side = "right"
            elif event.key == 101 and not pers.cool_dash:
                pers.dash = True
                pers.side = "left"
            if event.key == 97:
                pers.side = "right"
                pers.move = True
            elif event.key == 100:
                pers.side = "left"
                pers.move = True
            
                    
        elif event.type == pygame.KEYUP:

            if event.key != 32:
                if (event.key == 97 or event.key == 101) and pers.side == "left":
                    pers.move = True
                elif (event.key == 100 or event.key == 113) and pers.side == "right":
                    pers.move = True
                else:
                    pers.move = False
        
    
    dog1.update()
    pers.update()
    bg.draw(1)
    LVL1.draw()
    dog1.draw()
    pers.draw()
    pygame.display.update()