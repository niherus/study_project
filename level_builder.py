import os, sys, json
import pygame
from structure_level_builder import *

def save(widget):
    file = "levels\\{0}_{1}_{2}".format(text_input1.text, workspace.cell_size[0], workspace.cell_size[1])
    if os.path.isfile(file):
        log = "{0} is overwritten".format(file.split("\\")[1] + ".json")
    else:
        log = "{0} is successfuly saved".format(file.split("\\")[1] + ".json")
    with open(file + ".json", "w") as f:
        json.dump(workspace.map, f)
    return log

def load(widget):
    file = "levels\\{0}_{1}_{2}.json".format(text_input1.text, workspace.cell_size[0], workspace.cell_size[1])
    try:
        with open(file, "r") as f:
            workspace.map = json.load(f)
            log = "{0} is successfuly loaded".format(file.split("\\")[1])
    except FileNotFoundError:
        log = "{0} is not found".format(file.split("\\")[1])

    return log


all_liltes = []
for i in range(1, 20):
    all_liltes.append("plat_" + str(i) + ".png")

pygame.init()

screen = pygame.display.set_mode((1200, 800), pygame.RESIZABLE)

text_input1 = Text_input(screen, "level_name", pos=(200, 30), font_size=20)
btn1 = Button(screen, "Save", func=save, pos=(200, 70), font_size=20)
btn2 = Button(screen, "Load", func=load, pos=(200, 110), font_size=20)

log_terminal = Log_Win(screen, pos=(800, 600))
toolbox = ToolBox(screen, all_liltes)
workspace = WorkSpace(screen)

cur_pic = None
coords = None
pic = None
clock = pygame.time.Clock()
dir_shift = None
while True:
    clock.tick(60)
    screen.fill("#c2d1e5")
    
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            
            if event.button == 1:
                text_input1.is_active(event.pos)
                log_terminal.press(event.pos)
                cur_pic = toolbox.press(event.pos)
                
                if cur_pic != None:
                    log_line = workspace.add_tile(cur_pic, event.pos)
                    
                    if log_line != None:
                        log_terminal.add_line(log_line)
                        
                if btn1.press(event.pos):
                    btn1.pressed = True
                    
                if btn2.press(event.pos):
                    btn2.pressed = True
                    
            if event.button == 3:
                
                if cur_pic != None:
                    cur_pic = None
                    pic = None
                    toolbox.current = None
                else:
                    log_line = workspace.remove_tile(event.pos)
                    
                    if log_line != None:
                        log_terminal.add_line(log_line)
            
            if event.button == 4:
                toolbox.shift("up")
                
            if event.button == 5:
                toolbox.shift("down")
                
            if text_input1.active:
                
                if event.button == 4:
                    text_input1.font_size += 1
                    text_input1.update_font()
                elif event.button == 5:
                    text_input1.font_size -= 1
                    text_input1.update_font()
                    
        if event.type == pygame.MOUSEBUTTONUP:
            
            if btn1.pressed and btn1.func != None:
                log = btn1.do()
                log_terminal.add_line(log)
                btn1.pressed = False
            elif btn1.pressed and btn1.func == None:
                log_terminal.add_line("Useless button 1")
                btn1.pressed = False
                
            if btn2.pressed and btn2.func != None:
                log = btn2.do()
                log_terminal.add_line(log)
                btn2.pressed = False
            elif btn2.pressed and btn1.func == None:
                log_terminal.add_line("Useless button 2")
                btn2.pressed = False
            
        if event.type == pygame.MOUSEMOTION:
            
            if cur_pic != None:
                pic = pygame.image.load("images\\" + cur_pic)
                
            coords = event.pos
            
        if event.type == pygame.KEYDOWN:
            
            if text_input1.active:
                
                if event.key == 8:
                    text_input1.remove_text()
                elif event.key != 13 and event.key != 32:
                    text_input1.add_text(event.unicode)
            else:
                dir_shift = event.key
                
        if event.type == pygame.KEYUP:
            
            if event.key == 97 or event.key == 100 \
               or event.key == 119 or event.key == 115:
                dir_shift = None
                
    if dir_shift == 97:
        workspace.shift(dx=5)
        
    if dir_shift == 100:
        workspace.shift(dx=-5)
        
    if dir_shift == 119:
        workspace.shift(dy=5)
        
    if dir_shift == 115:
        workspace.shift(dy=-5)

    workspace.draw()
    toolbox.draw() 
    text_input1.draw()
    btn1.draw()
    btn2.draw()
    log_terminal.draw()
    
    if pic != None:
        screen.blit(pic, coords)
        
    pygame.display.update()