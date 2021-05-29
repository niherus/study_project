import pygame

class Auto:
    def __init__(self, screen, x, y, vx):
        self.screen = screen
        self.x = x
        self.y = y
        self.vx = vx
        self.z = 0
        self.t = 50
        self.t1 = 100
        
    def move(self):
        self.x += self.vx
        if self.z+self.x<0:
            self.vx *= -1
            self.t = 50
            self.t1 = 100
        if self.z+160+self.x>800:
            self.t = 60
            self.t1 = 110
            self.vx *= -1
    
    def draw(self):
        pygame.draw.circle(self.screen, "black", (30+self.x, self.y), 10)
        pygame.draw.circle(self.screen, "black", (130+self.x, self.y), 10)
        pygame.draw.polygon(self.screen, "black", [(self.z + self.x, self.y - 10), (self.z + 160 + self.x, self.y - 10),
                                              (160 + self.x, self.y - 30), (120 + self.x, self.y - 30),
                                              (120 + self.x, self.y - 50), (40 + self.x, self.y - 50),
                                              (40 + self.x, self.y - 30), (self.x,self.y - 30),(self.z + self.x, self.y-10)])
        pygame.draw.polygon(self.screen, "white", [( 110 + self.x, self.y - 30), (100 + self.x, self.y - 30), (self.t1 + self.x, self.y - 45)])
        pygame.draw.polygon(self.screen, "white", [(50 + self.x, self.y - 30), (self.t + self.x, self.y - 45), (60+self.x, self.y - 30)])