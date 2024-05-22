import pygame
import textures_library as tl

from global_classes import Vec2

class Object():
    def __init__(self):
        self.pos = Vec2()
        self.size.x = 50
        self.size.y = 50
        self.hitbox = pygame.rect.Rect(self.pos.x - self.size.x / 2+ SCREEN_WIDTH/2,self.pos.y- self.size.y / 2+SCREEN_HEIGHT/2,self.size.x,self.size.y)
        self.image = pygame.transform.scale(pygame.image.load("sprites/particle/box.png"), (self.size.x,self.size.y))

item_list = {"barryGun": Item("barryGun", is_equipable=True),
             "fireHatchet": Item("fireHatchet", is_equipable=True),
             "melonSlice": Item("melonSlice", is_consumable=True),
             "gourd": Item("gourd", is_equipable=True, is_consumable=True)}
