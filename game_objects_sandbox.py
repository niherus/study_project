import pygame, json
import random, os

class Play_object:
    def __init__(self, screen, image, pos, anchor=(0, 0)):
        self.screen = screen
        self.orig_image = pygame.image.load("images\\" + image)
        self.image = self.orig_image.copy()
        self.width, self.height = self.orig_image.get_size()
        self.pos = pos
        self.anchor = anchor
        self.side = {"dx": "right", "dy": "up"}

    def draw(self):
        self.image = self.orig_image.copy()
        if self.side["dx"] == "left":
            x = self.pos[0] - self.width * (1 - self.anchor[0])
            self.image = pygame.transform.flip(self.image, True, False)
        elif self.side["dx"] == "right":
            x = self.pos[0] - self.width * self.anchor[0]

        if self.side["dy"] == "down":
            y = self.pos[1] - self.height * (1 - self.anchor[1])
            self.image = pygame.transform.flip(self.image, False, True)
        elif self.side["dy"] == "up":
            y = self.pos[1] - self.height * self.anchor[1]
        
        pos = (x, y)
        self.screen.blit(self.image, pos)

class Tile(Play_object):
    def __init__(self, screen, image, pos, ind, anchor=(0, 0), go_free=[False], deep=30):
        super(Tile, self).__init__(screen, image, pos)
        self.ind = ind

        self.go_free = go_free
        if len(self.go_free) == 1:
            self.go_free = self.go_free * 4
        elif len(self.go_free) == 2:
            self.go_free = [self.go_free[0]] * 2 + [self.go_free[1]] * 2
        elif len(self.go_free) != 4:
            raise Exception("Error: wrong contact sides")

        self.deep = deep
        
        sides = ["left", "right", "up", "down"]
        self.go_free = {sides[i]: cont for i, cont in enumerate(self.go_free)}
        
        if self.deep == False:
            self.deep = min(self.width, self.height)

    def side_contact(self, obj):
        contactes = []

        for side, check in self.go_free.items():
            if check:

                if side == "left":
                    if self.pos[0] + self.deep > obj.pos[0] + obj.width > self.pos[0] and\
                        self.pos[1] < obj.pos[1] + self.height//2 < self.pos[1] + self.height:
                        contactes.append("left")
                elif side == "right":
                    if self.pos[0] + self.width - self.deep < obj.pos[0] < self.pos[0] + self.width and\
                        self.pos[1] < obj.pos[1] + self.height//2 < self.pos[1] + self.height:
                        contactes.append("right")
                elif side == "up":
                    if self.pos[1] + self.deep > obj.pos[1] + obj.height > self.pos[1] and\
                        self.pos[0] < obj.pos[0] + self.width * self.anchor[0] < self.pos[0] + self.width:
                        contactes.append("up")
                elif side == "down":
                    if self.pos[1] + obj.height - self.deep < obj.pos[1] < self.pos[1] + obj.height and\
                        self.pos[0] < obj.pos[0] + self.width * self.anchor[0] < self.pos[0] + self.width:
                        contactes.append("down")

        return contactes

class Character(Play_object):
    def __init__(self, screen, start_image, pos, name, hp=100, tag=False, speed=3, anchor=(0.25, 0),\
                 manual=False):#, behavior=None, way_points=None, range_set=None):
        super(Character, self).__init__(screen, start_image, pos, anchor)
        self.name = name
        file = f"{self.name}.json"
        with open(os.path.join("images", "animations", file), "r") as f:
            self.animation_set = json.load(f)

        self.hp = hp
        self.speed = speed
        self.vy = 0
        self.ay = 0.5
        self.status = "idle"
        self.manual = manual
        self.pressed = []
        if manual:
            with open(os.path.join("control_sets", file), "r") as f:
                self.control_set = json.load(f)
        else:
            with open(os.path.join("behavior", file), "r") as f:
                self.behavior = json.load(f)
        self.dash_time = 0       
        self.time = 0
        self.step = 0
        
    def play_animation(self, name):
        current_animation = self.animation_set[name]
        images = current_animation["images"]
        timing = current_animation["timing"]
        self.orig_image = pygame.image.load("images\\" + images[self.step])
        if self.time == timing[self.step]:
            self.step += 1
            self.time = 0
        if self.step == len(images):
            self.step = 0
        self.time += 1

    def restart(self):
        self.dash_time = 0 
        self.time = 0
        self.step = 0
        
    def idle(self):
        self.play_animation("idle")
        
    def walk(self, world):

        self.play_animation("walk")
        if self.side["dx"] == "left":
            world.shift(dx=self.speed)
        elif self.side["dx"] == "right":
            world.shift(dx=-self.speed)
        
    def gravity(self, world):
        
        place = world.grounded(self)

        if not place:
            world.shift(dy=-self.vy)
            self.vy += self.ay
        else:
            
            self.vy = 0
    def jump(self, world):
        world.shift(dy=world.grounded(self).pos[1] - self.pos[1] - self.height + 60)
        self.vy = -15
        
    def dash(self, world):
        self.play_animation("dash")
        coef = self.dash_calc(self.dash_time)
 
        if self.side["dx"] == "left":
            world.shift(dx=coef*self.speed)
        elif self.side["dx"] == "right":
            world.shift(dx=-coef*self.speed)
        if coef < 1:
            
            self.restart()
            self.status = "walk"
        self.dash_time += 1
            
    def dash_calc(self, dash):
        return 10 * 2**(-(dash*0.1)**2)
    def attack(self, victim, method):
        print("attack")

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

class Level:
    def __init__(self, screen, leveL_file, map_pos, start_pos):
        self.screen = screen
        self.x, self.y = (map_pos[0] - 100 * start_pos[0] - 10, map_pos[1] - 100 * start_pos[1] - 10)
        self.lowest = False
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
             
            temp_tile = Tile(self.screen, image=cur_pic, pos=coord, ind=pos, go_free=[False, True])

            self.lvl.append(temp_tile)
            if self.lowest == False:
                self.lowest = pos[1]
                i = 0
            elif pos[1] > self.lowest:
                self.lowest = pos[1]
                i = len(self.lvl) - 1
            
            self.lowest = i
        self.characters_manual = dict()
        self.characters_auto = dict()
        
    def add_character(self, char):
        if char.manual:
            self.characters_manual[char.name] = char
        else:
            self.characters_auto[char.name] = char
    def grounded(self, char):
        for tile in self.lvl:
            if "up" in tile.side_contact(char):
                return tile
        return False
        
    def update_from_event(self, event):
        for char in self.characters_manual.values():
            all_keys = list(char.control_set["key"].keys())
            all_mouse = list(char.control_set["mouse"].keys())
            if event.type == pygame.KEYDOWN:
                for key in all_keys:
                    if event.key == int(key) :
                        if int(key) not in char.pressed:
                            char.pressed.append(int(key))
                        char.restart()
                        action = char.control_set["key"][key].split("_")

                        if action[0] != "jump":
                            char.status = action[0]
                            if len(action) == 2:
                                char.side["dx"] = action[1]
                        elif action[0] == "jump" and self.grounded(char):
                            char.jump(self)
                          
            if event.type == pygame.KEYUP:
 
                
                if str(event.key) in all_keys:
                    if event.key in char.pressed:
                        char.pressed.remove(event.key)
                    #action = char.control_set["key"][str(event.key)].split("_")[0]

                    if not char.pressed:
                        char.restart()
                        char.status = "idle"                      
                    
    def update_fps(self):
        for char in self.characters_auto.values():
            if char.status == "idle":
                pass
                #char.idle()
        for char in self.characters_manual.values():
            char.gravity(self)
            if char.status == "idle":
                char.idle()
            if char.status == "walk":
                char.walk(self)
            if char.status == "dash":
                char.dash(self)
    def shift(self, dx = 0, dy = 0):
        for tile in self.lvl:
            x = tile.pos[0] + dx
            y = tile.pos[1] + dy
            tile.pos = (x, y)
        
        
    def draw(self):
        for tile in self.lvl:
            tile.draw()
        for char in self.characters_manual.values():
            char.draw()
        for char in self.characters_auto.values():
            char.draw()