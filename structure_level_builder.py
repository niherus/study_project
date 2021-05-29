import pygame

class Text_input:
    def __init__(self, screen, text, pos=(0,0), size=(100, 20),\
                 padding=10, bg="#FF9BB9", fg="#000000", auto_scale=True,\
                 active=False, font_size=12, font_name="Arial"):
        
        self.screen = screen
        self.text = text
        self.font_name, self.font_size = font_name, font_size
        self.font = pygame.font.SysFont(font_name, font_size, bold=True)
        self.pos = pos
        w, h = self.font.size(self.text)
        self.auto_scale = auto_scale
        self.size = size
        self.padding = padding
        if self.auto_scale:
                self.size = (w + self.padding, self.size[1])
                self.size = (self.size[0], h + self.padding)
        self.active = active
        self.bg = bg
        self.fg = fg
        
    def draw(self):
        w, h = self.font.size(self.text)
        if self.auto_scale:
                self.size = (w + self.padding, self.size[1])
                self.size = (self.size[0], h + self.padding)
        
        text_pos = (self.pos[0] + self.padding//2, self.pos[1] + self.padding//2)
        border = (self.pos[0] - 2, self.pos[1] - 2, self.size[0] + 4, self.size[1] + 4)
        pygame.draw.rect(self.screen, color="#000000", rect=pygame.Rect(*border))
        pygame.draw.rect(self.screen, color=self.bg, rect=pygame.Rect(*self.pos, *self.size ))
        text = self.font.render(self.text, False, self.fg)
        self.screen.blit(text, text_pos)
        
    def is_active(self, pos):
        if self.pos[0] < pos[0] < self.pos[0] + self.size[0] and\
           self.pos[1] < pos[1] < self.pos[1] + self.size[1]:
            self.active = True
        else:
            self.active = False
    
    def add_text(self, text):
        self.text += text
        
    def remove_text(self):
        if len(self.text):
            self.text = self.text[:-1]
            
    def update_font(self):
        self.font = pygame.font.SysFont(self.font_name, self.font_size, bold=True)
        
class Button:
    def __init__(self, screen, text, func=None, pos=(0, 0), size=(50, 10), autoscale=True,\
                 padding=10, bg="#FF9BB9", bg_pressed="#A618A6", fg="#000000", auto_scale=True,\
                 pressed=False, font_size=12, font_name="Arial"):
        self.screen = screen
        self.text = text
        self.func = func
        self.pos = pos
        self.size = size
        self.auto_scale = auto_scale
        self.pressed = pressed
        self.padding = padding
        self.bg = bg
        self.bg_pressed = bg_pressed
        self.fg = fg
        self.font_name, self.font_size = font_name, font_size
        self.font = pygame.font.SysFont(font_name, font_size, bold=True)
        w, h = self.font.size(self.text)
        if self.auto_scale:
            self.size = (w + self.padding, self.size[1])
            self.size = (self.size[0], h + self.padding)

    def draw(self):
        border = (self.pos[0] - 2, self.pos[1] - 2, self.size[0] + 4, self.size[1] + 4)
        pygame.draw.rect(self.screen, color="#000000", rect=pygame.Rect(*border))
        if not self.pressed:
            pygame.draw.rect(self.screen, color=self.bg, rect=pygame.Rect(*self.pos, *self.size ))
        else:
            pygame.draw.rect(self.screen, color=self.bg_pressed, rect=pygame.Rect(*self.pos, *self.size ))
        text_pos = (self.pos[0] + self.padding//2, self.pos[1] + self.padding//2)
        text = self.font.render(self.text, False, self.fg)
        self.screen.blit(text, text_pos)
        
    def press(self, pos):
        if self.pos[0] < pos[0] < self.pos[0] + self.size[0] and\
           self.pos[1] < pos[1] < self.pos[1] + self.size[0]:
            return True
    
    def do(self):
        if self.func != None:
            log = self.func(self)
        return log

class Log_Win:
    
    def __init__(self, screen, pos=(0, 0), size=(400, 200),\
                 padding=10, alpha=64, bg="#7A65BF", fg="#000000",\
                 active=False, font_size=16, font_name="Arial"):
        
        self.screen = screen
        self.text_lines = ["LEVEL BUILDER v0.1"]
        
        self.pos = pos
        self.size = size
        self.alpha = alpha
        self.bg = bg
        self.fg = fg
        self.font_name, self.font_size = font_name, font_size
        self.font = pygame.font.SysFont(font_name, font_size, bold=True)
        w, h = self.font.size(self.text_lines[0])
        self.padding = padding
        self.start_line = 0
        self.finish = size[1] // (h + padding)
        
        self.ar_pos_up = (pos[0] + size[0] - 50, pos[1] + size[1] - 100)
        self.ar_pos_down = (pos[0] + size[0] - 50, pos[1] + size[1] - 50)
        
    def add_line(self, text):
        w, h = self.font.size(text)
        
        k = w // (self.size[0] - self.padding)
        if k > 0:
            for i in range(k + 1):

                self.text_lines.append(text[i * len(text) // (k + 1): (i + 1) * len(text) // (k + 1)])
        else:
            self.text_lines.append(text)

    def draw(self):
        w, h = self.font.size(self.text_lines[0])
        
        base = pygame.Surface(self.size)
        base.set_alpha(self.alpha)
        base.fill(self.bg)
        self.screen.blit(base, self.pos)
        
        self.arrow_up = pygame.image.load("images\\arrow.png")
        self.arrow_down = pygame.transform.flip(self.arrow_up, False, True)
        
        self.screen.blit(self.arrow_up, self.ar_pos_up)
        self.screen.blit(self.arrow_down, self.ar_pos_down)
        
        if self.finish > len(self.text_lines) - self.start_line:
            finish = len(self.text_lines)
        else:
            finish = self.finish
        st_x, st_y = self.pos
        
        for i in range(self.start_line, finish):
            text = self.font.render(str(i) + " "\
                                    + self.text_lines[i], False, self.fg)
            self.screen.blit(text, (st_x + 2 + self.padding,\
                                    st_y + 2 + h * (i - self.start_line) + self.padding))
    
    def press(self, pos):
        if self.ar_pos_up[0] < pos[0] < self.ar_pos_up[0] + 40 and\
           self.ar_pos_up[1] < pos[1] < self.ar_pos_up[1] + 40:
            if self.start_line < len(self.text_lines):
                self.start_line += 1
            
        if self.ar_pos_down[0] < pos[0] < self.ar_pos_down[0] + 40 and\
           self.ar_pos_down[1] < pos[1] < self.ar_pos_down[1] + 40:
            if self.start_line > 0:
                self.start_line -= 1

class ToolBox:
    def __init__(self, screen, plats, pos=(0, 0), size=(180, 800),\
                 padding=10, alpha=255, bg="#7A65BF", fg="#000000",\
                 font_size=25, font_name="Arial"):
        self.screen = screen
        self.plats = plats
        self.pos = pos
        self.size = size
        self.padding = padding
        self.alpha = alpha
        self.bg = bg
        self.start_pic = 0
        self.ar_pos_up = (pos[0] + size[0] - 45, pos[1] + size[1] - 100)
        self.ar_pos_down = (pos[0] + size[0] - 45, pos[1] + size[1] - 50)
        self.bg = bg
        self.fg = fg
        self.font_name, self.font_size = font_name, font_size
        self.font = pygame.font.SysFont(font_name, font_size, bold=True)
        self.current = None
        
    def draw(self):
        
        base = pygame.Surface(self.size)
        base.set_alpha(self.alpha)
        base.fill(self.bg)
        self.screen.blit(base, self.pos)
        w, h = self.font.size("1")
        for i in range(len(self.plats)):
            st_x, st_y = self.pos
            text = self.font.render(str(i + 1), False, self.fg)
            self.screen.blit(text, (st_x + 2 + self.padding//2,\
                                   self.pos[1] + self.size[0] * (i - self.start_pic) + self.padding))
            
            
            plat = pygame.image.load("images\\" + self.plats[i])
            self.screen.blit(plat, (self.pos[0] + self.padding * 3,\
                                    self.pos[1] + self.size[0] * (i - self.start_pic) + self.padding))
        
        self.arrow_up = pygame.image.load("images\\arrow.png")
        self.arrow_down = pygame.transform.flip(self.arrow_up, False, True)
        
        self.screen.blit(self.arrow_up, self.ar_pos_up)
        self.screen.blit(self.arrow_down, self.ar_pos_down)
    def shift(self, direct="up"):
        if direct=="up" and self.start_pic > 0:
                self.start_pic -= 1
                self.current = None
        
        if direct=="down" and self.start_pic < len(self.plats):
                self.start_pic += 1
                self.current = None
        
    def press(self, pos):
        
        if self.ar_pos_up[0] < pos[0] < self.ar_pos_up[0] + 40 and\
           self.ar_pos_up[1] < pos[1] < self.ar_pos_up[1] + 40:
           self.shift("up")
            
        if self.ar_pos_down[0] < pos[0] < self.ar_pos_down[0] + 40 and\
           self.ar_pos_down[1] < pos[1] < self.ar_pos_down[1] + 40:
           self.shift("down")
        
        for i in range(len(self.plats)):
            x = self.pos[0] + self.padding * 3
            y = self.pos[1] + self.size[0] * (i - self.start_pic) + self.padding
            
            if x < pos[0] < x + 100 and\
               y < pos[1] < y + 100:
                self.current = self.plats[i]
        return self.current
        
        

class WorkSpace:
    def __init__(self, screen, cell_size=(20, 10), grid_scale=100, grid_width=1, grid_color="#A67618",\
                 fg="#000000", font_size=25, font_name="Arial"):
        self.screen = screen
        self.pos = (0, 0)
        
        self.cell_size = cell_size
        self.grid_scale = grid_scale
        self.grid_width = grid_width
        self.grid_color = grid_color
        
        self.font_name, self.font_size = font_name, font_size
        self.font = pygame.font.SysFont(font_name, font_size, bold=True)
        self.fg = fg
        self.map = dict()
        self.shift_to_start()
    def draw_grid(self):
        w, h = self.font.size(str(max(self.cell_size)))
        for i in range(self.cell_size[0]):
            

            st = (i * self.grid_scale - self.pos[0], 0)
            text = self.font.render(str(i + 1), False, self.fg)
            self.screen.blit(text, (st[0] + w, st[1]))
            end = (i * self.grid_scale - self.pos[0], 800)
            pygame.draw.line(self.screen, self.grid_color, st, end, self.grid_width)
        
        for i in range(self.cell_size[1]):
            st = (0, i * self.grid_scale - self.pos[1])

            end = (1200, i * self.grid_scale - self.pos[1])
            text = self.font.render(str(i + 1), False, self.fg)
            self.screen.blit(text, (end[0] - w, end[1]))
            pygame.draw.line(self.screen, self.grid_color, st, end, self.grid_width)
    def draw(self):
        self.draw_grid()
   
        for pos, cur_pic in self.map.items():
            pos = tuple(map(int, pos.split(",")))
            pic = pygame.image.load("images\\" + cur_pic)
            coord = (-self.pos[0] + pos[0] * self.grid_scale, -self.pos[1] + pos[1] * self.grid_scale)
            self.screen.blit(pic, coord)
    def shift(self, dx=0, dy=0):
        self.pos = (self.pos[0] + dx, self.pos[1] + dy)
    
    def shift_to_start(self):
        kx = 1200 // self.grid_scale
        ky = 800 // self.grid_scale
        dx = -self.pos[0] - 180
        dy = - self.pos[1] + self.grid_scale * (self.cell_size[1] - ky)
        self.shift(dx, dy)
    
    def add_tile(self, pic_name, coord):
        i = (coord[0] + self.pos[0]) // self.grid_scale
        j = (coord[1] + self.pos[1]) // self.grid_scale
        if self.cell_size[0] >= i >= 0 and self.cell_size[1] >= j >= 0:
            self.map[str(i) + ", "+ str(j)] = pic_name
            return "{0} placed on {1}".format(pic_name, (i, j))
    
    def remove_tile(self, coord):
        i = (coord[0] + self.pos[0]) // self.grid_scale
        j = (coord[1] + self.pos[1]) // self.grid_scale
        if self.cell_size[0] >= i >= 0 and self.cell_size[1] >= j >= 0 and str(i) + ", "+ str(j) in self.map.keys():
            pic_name = self.map[str(i) + ", "+ str(j)] 
            del self.map[str(i) + ", "+ str(j)]
            return "{0} removed from {1}".format(pic_name, (i, j))
    
    