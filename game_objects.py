import pygame, json
import random

def dash(x, scale = 10, mult = 0.1, shift = 3):
    return scale*2**(-mult*(x-shift)**2)


class Tile:
    def __init__(self, screen, image, pos, ind):
        self.name = image
        self.image = pygame.image.load("images\\" + image)
        self.x, self.y = pos
        self.screen = screen
        self.ind = ind
    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))
 
        
class Level:
    def __init__(self, screen, tiles_list, leveL_file, map_pos, start_pos):
        self.screen = screen
        self.x, self.y = (map_pos[0] - 100 * start_pos[0], map_pos[1] - 100 * start_pos[1])
        self.tiles_list = tiles_list
        self.lowest = None
        file = "levels\\" + leveL_file
        self.lvl = []
        
        try:
            with open(file, "r") as f:
                self.map = json.load(f)
        except FileNotFoundError:
            raise Exception("Level not found")
        
        i = 0
        for pos, cur_pic in self.map.items():
            pos = tuple(map(int, pos.split(",")))
            pic = pygame.image.load("images\\" + cur_pic)
            coord = (-self.x + pos[0] * 100, -self.y + pos[1] * 100)
             
            temp_tile = Tile(self.screen, image=cur_pic, pos=coord, ind=pos)

            self.lvl.append(temp_tile)
            if self.lowest == None:
                self.lowest = pos[1]
                i = 0
            elif pos[1] > self.lowest:
                self.lowest = pos[1]
                i = len(self.lvl) - 1
            
            self.lowest = i
            
                   
    def shift(self, dx = 0, dy = 0):
        for l in self.lvl:
            l.x += dx
            l.y += dy
        
        
    def draw(self):
        for tile in self.lvl:
            tile.draw()
        
        

class BackGround:
    def __init__(self, screen, images):
        self.screen = screen
        
        
        self.images = []
        for image in images:
            self.images.append(pygame.image.load("images\\" + image))
        self.x = 0
        self.y = 0
        
    def draw(self, num):
        self.screen.blit(self.images[num], (self.x, self.y))
        
    def move(self, vx, vy):
        self.x += vx
        self.y += vy

class Pers:
    def __init__(self, screen, idle_image, idle_timing,
                 walk_image, walk_timing,
                 hit_image,
                 hit_timing,
                 cur_level, x=300, y=500, speed = 3):
        self.screen = screen
        self.hp = 100
        self.idle_image = idle_image
        self.idle_timing = idle_timing
        self.walk_image = walk_image
        self.walk_timing = walk_timing
        
        self.hit_image = hit_image
        self.hit_timing = hit_timing
        self.hit_status = False
        
        self.cur_level = cur_level
        self.ori_image = pygame.image.load("images\\" + self.idle_image[0])
        w, h = self.ori_image.get_size()
        self.image = self.ori_image.copy()
        self.x = x
        self.draw_x = self.x + w//4
        self.y = y
        self.speed = speed
        self.vy = 0
        self.ay = 0.5
        self.side = "right"
        self.move = False
        self.dash = False

        self.jump = False
        self.ground = None
        self.last_ground = self.cur_level.lvl[self.cur_level.lowest]
        self.cool_dash = 0
        self.time = 0
        self.step = 0
        self.debug = True
        self.hurt = False
        self.attacker = None
    def set_enemy(self, attacker):
        self.attacker = attacker
    def update(self):
        w, h = self.ori_image.get_size()
        if self.side == "left":
            self.draw_x = self.x + 3*w//4
        elif self.side == "right":
            self.draw_x = self.x + w//4
            
        self.get_hit(self.attacker)
        if self.cool_dash > 0:
            self.cool_dash -= 1
        if not self.grounded():
            if self.last_ground.y - self.y > -100:
                self.cur_level.shift(dy=-self.vy)
            else:
                self.y += self.vy
            self.vy += self.ay
        else:
            self.vy = 0
            dy = self.ground.y - self.y - 100
            if dy < 3:
               self.cur_level.shift(dy=-dy)
            
        
        if self.jump:
            self.vy = -13
        
            self.jump = False
        if self.dash and not self.hit_status:

            self.ori_image =  pygame.image.load("images\\" + self.walk_image[1])
            if self.side == "left":
                self.image = self.ori_image.copy()
                self.cur_level.shift(dx=-dash(self.time) * self.speed)
            elif self.side == "right":
                self.image = pygame.transform.flip(self.ori_image, True, False)
                self.cur_level.shift(dx=dash(self.time) * self.speed)

            self.time += 1
            if dash(self.time) < 0.01:
                self.dash = False
                self.time = 0
                self.cool_dash = 40

        elif self.hit_status:
            
            self.ori_image = pygame.image.load("images\\" + self.hit_image[self.hit_status][self.step])
            
            if self.side == "left":
                self.image = self.ori_image.copy()
            elif self.side == "right":
                self.image = pygame.transform.flip(self.ori_image, True, False)
                
            if self.hit_timing[self.hit_status][self.step] > self.time:
                self.time += 1
            else:
                self.step += 1
                self.time = 0
            
            if self.step == len(self.hit_timing[self.hit_status]):
                self.step = 0
                self.time = 0
                self.hit_status = False
        elif not self.dash and not self.hit_status:
            if self.move:
                self.ori_image = pygame.image.load("images\\" + self.walk_image[self.step])
                if self.side == "left":
                    self.image = self.ori_image.copy()
                    self.cur_level.shift(dx=-self.speed)

                elif self.side == "right":
                    self.image = pygame.transform.flip(self.ori_image, True, False)
                    self.cur_level.shift(dx=self.speed)

                self.time += 1
                if self.walk_timing[self.step] <= self.time:
                    self.step += 1
                    self.step %= len(self.walk_image)
                    self.time = 0
            else:
                self.ori_image = pygame.image.load("images\\" + self.idle_image[self.step])
                if self.side == "left":
                    self.image = self.ori_image.copy()
                elif self.side == "right":
                    self.image = pygame.transform.flip(self.ori_image, True, False)
                self.time += 1
                if self.idle_timing[self.step] <= self.time:
                    self.step += 1
                    self.step %= len(self.idle_image)
                    self.time = 0
                
    def draw(self):


        if self.debug:
            w, h = self.ori_image.get_size()
            
            base = pygame.Surface((w, h))
            base.set_alpha(64)
            base.fill("#00ff00")
            self.screen.blit(base, (self.draw_x, self.y))
            hit_box = pygame.Surface((40, h))
            hit_box.set_alpha(128)
            hit_box.fill("#800080")
            if self.side == "left":
                self.screen.blit(hit_box, (self.draw_x + w - 40, self.y))
            elif self.side == "right":
                self.screen.blit(hit_box, (self.draw_x, self.y))
            center = pygame.Surface((5, h))
            center.fill("#ffffff")
            self.screen.blit(center, (self.draw_x + w//2, self.y))
        
        
            
        self.screen.blit(self.image, (self.draw_x, self.y))
        pos = (50, 50)
        size = (200*self.hp/100, 20)
        border = (pos[0] - 2, pos[1] - 2, 200 + 4, 20 + 4)
        pygame.draw.rect(self.screen, color="#000000", rect=pygame.Rect(*border))
        pygame.draw.rect(self.screen, color="#ff0000", rect=pygame.Rect(*pos, *size ))
    
    def grounded(self):
        flag = False
        w, h = self.ori_image.get_size()
        for plat in self.cur_level.lvl:
            if int(plat.name.split("_")[1][:-4]) < 9:
                if plat.y - 80 >= self.y >= plat.y - 110:
                    if self.side == "left":
                    
                        x_pos = self.draw_x + w // 4
                    elif self.side == "right":
                        x_pos = self.draw_x + 3*w // 4
                    if plat.x < x_pos - 10 < plat.x + 100 or plat.x < x_pos + 10 < plat.x + 100 :
                        self.ground = plat
                        return True
                
        self.ground = None
        
        return False
    
    def get_hit(self, attacker):
        if isinstance(attacker, Enemy):
            w, h = attacker.ori_image.get_size()
            w1, h1 = self.ori_image.get_size()
            if attacker.cur_mode == "attack":
                if  attacker.attack_mode == "bite" and attacker.step == 1 and not self.hurt:
                    
                    if attacker.side == "right":
                        print(self.y, attacker.y + h//2, self.y + h1)
                        if  attacker.x - self.x -  w1 < 0 and self.y < attacker.y + h//2 < self.y + h1 :
                            self.hp -= 5
                            self.hurt = True

                    elif attacker.side == "left":
                        if  attacker.x - self.x > 0 and self.y < attacker.y + h//2< self.y + h1 :
                            self.hp -= 5
                            self.hurt = True
                elif attacker.attack_mode == "paw_hit" and attacker.step <= 4 and not self.hurt:
         
                    if attacker.side == "right":
                        if  attacker.x - self.x - w1 < 0 and self.y < attacker.y + h//2< self.y + h1 :
                            self.hp -= 20
                            self.hurt = True

                    elif attacker.side == "left":
                        if  attacker.x - self.x > 0 and self.y < attacker.y + h//2< self.y + h1 :
                            self.hp -= 20
                            self.hurt = True
                elif attacker.ready:
                    self.hurt = False
                    

class Enemy:
    def __init__(self, screen, idle_image, idle_timing,
                 walk_image, walk_timing,
                 attack_image, attack_timing,
                 cur_level, start_pos, behavior_plan, attacker,
                 way_points=[], chase_range = 1000, attack_range = 100):
        self.screen = screen
        self.idle_image = idle_image
        self.idle_timing = idle_timing
        self.walk_image = walk_image
        self.walk_timing = walk_timing
        self.attack_image = attack_image
        self.attack_timing = attack_timing
        self.cur_level = cur_level
        self.debug = True
        base = f"{start_pos[0]}, {start_pos[1]}"

        if base in self.cur_level.map.keys():
            if int(self.cur_level.map[base][:-4].split("_")[1]) < 9:
                self.start_pos = start_pos
            else:
                raise Error("Can't stay here")
        else:
            raise Error("Can't stay here")

        self.base = self.get_way(self.start_pos)

        self.ori_image = pygame.image.load("images\\" + self.idle_image[0])
        self.w, self.h = self.ori_image.get_size()
        self.x = self.base.x
        self.y = self.base.y - self.h + 20
        self.image = self.ori_image.copy()
        self.behavior_plan = behavior_plan
        self.beh_num = 0
        self.cur_mode = self.behavior_plan[self.beh_num]
        self.attack_mode = "bite"
        self.side = "left"
        self.time = 0
        self.step = 0
        self.way_points = way_points
        self.destine = 0
        self.dx = 0
        self.speed = 1
        self.finish_tile = self.get_way(self.way_points[self.destine])
        self.x_f, self.y_f = self.finish_tile.x, self.finish_tile.y
        self.hp = 500
        self.max_hp = 500
        self.hurt = False
        self.attacker=attacker
        self.attack_range=attack_range
        self.chase_range=chase_range
        self.ready = False
    def draw(self):
        if self.debug:
            w, h = self.ori_image.get_size()
            
            base = pygame.Surface((w, h))
            base.set_alpha(64)
            base.fill("#00ff00")
            self.screen.blit(base, (self.x, self.y))
            hit_box = pygame.Surface((40, h))
            hit_box.set_alpha(128)
            hit_box.fill("#800080")
            if self.side == "left":
                self.screen.blit(hit_box, (self.x + w - 40, self.y))
            elif self.side == "right":
                self.screen.blit(hit_box, (self.x, self.y))
            
            center = pygame.Surface((5, h))
            center.fill("#ffffff")
            self.screen.blit(center, (self.x + w//2, self.y))
        self.screen.blit(self.image, (self.x, self.y))
        pos = (self.x, self.y)
        size = (200*self.hp/self.max_hp, 20)
        border = (pos[0] - 2, pos[1] - 2, 200 + 4, 20 + 4)
        pygame.draw.rect(self.screen, color="#000000", rect=pygame.Rect(*border))
        pygame.draw.rect(self.screen, color="#ff0000", rect=pygame.Rect(*pos, *size ))
    
    def update(self):
  
        if self.range_to_attacker(self.attacker) < self.chase_range:
            self.next_way()
        self.get_hit(self.attacker)
        self.x_f, self.y_f = self.finish_tile.x, self.finish_tile.y
        self.x = self.base.x + self.dx
        self.y = self.base.y - self.h + 20
        if self.cur_mode == "idle":
            self.ori_image = pygame.image.load("images\\" + self.idle_image[self.step])
            self.w, self.h = self.ori_image.get_size()
            if self.side == "right":
                self.image = self.ori_image.copy()
            elif self.side == "left":
                self.image = pygame.transform.flip(self.ori_image, True, False)
            self.time += 1
            if self.idle_timing[self.step] <= self.time:
                self.step += 1
                self.time = 0
            if self.step == len(self.idle_image):
                self.step = 0
                self.behavior()
                
        elif self.cur_mode == "walk":
            self.ori_image = pygame.image.load("images\\" + self.walk_image[self.step])
            self.w, self.h = self.ori_image.get_size()
            if self.side == "right":
                self.image = pygame.transform.flip(self.ori_image, True, False)
                self.dx -= self.speed 
                if self.x_f > self.x:
                    self.next_way()
            elif self.side == "left":
                self.image = self.ori_image.copy()
                self.dx += self.speed
                if self.x_f < self.x:
                    self.next_way()
            self.time += 1
            if self.walk_timing[self.step] <= self.time:
                self.step += 1
                self.time = 0
            if self.step == len(self.walk_image):
                self.step = 0
                self.behavior()
                
        elif self.cur_mode == "sprint":
            self.ori_image = pygame.image.load("images\\" + self.walk_image[self.step])
            self.w, self.h = self.ori_image.get_size()
            if self.side == "right":
                self.image = pygame.transform.flip(self.ori_image, True, False)
                self.dx -= 2*self.speed
                if self.x_f > self.x:
                    self.next_way()
            elif self.side == "left":
                self.image = self.ori_image.copy()
                self.dx += 2*self.speed
                if self.x_f < self.x:
                    self.next_way()
            self.time += 1
            if self.walk_timing[self.step] <= self.time:
                self.step += 1
                self.time = 0
            if self.step == len(self.walk_image):
                self.step = 0
                self.behavior()        
            
                
        elif self.cur_mode == "attack":
            self.x_f, self.y_f = self.attacker.x, self.attacker.y
            mode = self.attack_image[self.attack_mode]
            timing = self.attack_timing[self.attack_mode]
            self.ori_image = pygame.image.load("images\\" + mode[self.step])
            self.w, self.h = self.ori_image.get_size()
            if self.side == "left":
                self.image = self.ori_image.copy()
            elif self.side == "right":
                self.image = pygame.transform.flip(self.ori_image, True, False)
            self.time += 1
            if timing[self.step] <= self.time:
                self.step += 1
                self.time = 0
            
            if self.step == len(mode):
                self.step = 0
                self.attack_mode = random.choice(["bite", "paw_hit"])
                self.ready = True
                if self.range_to_attacker(self.attacker) >= self.attack_range:
                    self.cur_mode = "sprint"
            else:
                self.ready = False
                    
    def behavior(self):
        
        self.cur_mode = self.behavior_plan[self.beh_num]
        self.beh_num += 1
        self.beh_num %= len(self.behavior_plan)
    
    def get_way(self, tile_coord):
        for i, tile in enumerate(self.cur_level.lvl):
            if tile.ind == tile_coord:
                break
        return tile
    def range_to_attacker(self, attacker):
        w, h = attacker.ori_image.get_size()
        
        if attacker.side == "left":
            dx1 = (attacker.draw_x + 3*w//4)
            
        elif attacker.side == "right":
            dx1 = (attacker.draw_x + w//4)
        
        if attacker.side == "right":
            dx2 = (self.x + self.w//4)
            
        elif attacker.side == "left":
            dx2 = (self.x + 3*self.w//4)

        dx = dx1 - dx2
        dy = (attacker.y + h//2) - (self.y + self.h//2)
        return ((dx)**2 + (dy)**2) ** 0.5    
    def next_way(self):
        w, h = self.attacker.ori_image.get_size()
        if self.range_to_attacker(self.attacker) >= self.chase_range and self.cur_mode != "attack":
            self.destine += 1
            self.destine %= len(self.way_points)
            self.finish_tile = self.get_way(self.way_points[self.destine])
            self.x_f, self.y_f = self.finish_tile.x, self.finish_tile.y
        elif self.range_to_attacker(self.attacker) >= self.attack_range and self.cur_mode != "attack":
            self.destine = 0
            self.cur_mode = "sprint"
            if self.attacker.side == "left":
                catch_x = self.attacker.draw_x + 3*w/4
            elif self.attacker.side == "right":
                catch_x = self.attacker.draw_x + w/4
            self.x_f, self.y_f = catch_x, self.attacker.y
        else:
            
            self.destine = 0
            self.cur_mode = "attack"
            
        
        if self.range_to_attacker(self.attacker) > self.chase_range:
            if self.x + self.w//2 - self.x_f - w//2 > 0:
                self.side = "right"
            else:
                self.side = "left"
        else:
            if self.side == 'left':
                hit_b = self.x 
            elif self.side == 'right':
                hit_b = self.x + self.w
            if hit_b - self.x_f > 0:
                self.side = "right"
            else:
                self.side = "left"
                
                
  
                          
    def get_hit(self, attacker):

        if isinstance(attacker, Pers):
            w, h = attacker.ori_image.get_size()
            if attacker.hit_status == "punch1" and attacker.step == 1 and not self.hurt:
                
                if attacker.side == "left":
                    if  attacker.draw_x - self.x > 0 and self.y < attacker.y - 20 < self.y + self.h/2 :
                        self.hp -= 5
                        self.hurt = True
                        print("damage", attacker.draw_x, self.x, attacker.draw_x - self.x - w, attacker.side)
                elif attacker.side == "right":
                    if  attacker.draw_x - self.x - w < 0 and self.y < attacker.y - 20 < self.y + self.h/2 :
                        self.hp -= 5
                        self.hurt = True
                        print("damage", attacker.draw_x, self.x, attacker.draw_x - self.x - w, attacker.side)
            elif attacker.hit_status == "punch2" and attacker.step == 4 and not self.hurt:
                if attacker.side == "left":
                    if  attacker.draw_x - self.x > 0 and self.y < attacker.y - 20 < self.y + self.h/2 :
                        self.hp -= 20
                        self.hurt = True
                        print("damage", attacker.draw_x, self.x, attacker.draw_x - self.x - w, attacker.side)
                elif attacker.side == "right":
                    if  attacker.draw_x - self.x - w < 0 and self.y < attacker.y - 20 < self.y + self.h/2 :
                        self.hp -= 20
                        self.hurt = True
                        print("damage", attacker.draw_x, self.x, attacker.draw_x - self.x - w, attacker.side)
            elif attacker.hit_status == False:
                self.hurt = False
class Pocket:
    def __init__(self, screen, main_image, size=(4, 5), things=dict(), things_size=(50, 50), show=False, padding=20, pos=(0, 0)):
        self.screen = screen
        self.ori_image = pygame.image.load(map_image)
        self.things = things
        self.padding = padding
        self.w, self.h = size
        self.wt, self.ht = things_size
        self.x, self.y = pos
    def draw(self):
        for i in range(self.w):
            for j in range(self.h):
                self.screen.blit(self.image, (self.x + self.padding + i * self.wt, self.y + self.padding + j * self.ht))