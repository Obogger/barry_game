import pygame
import textures_library as tl

from global_classes import Vec2

class Item():
    def __init__(self, image_name, x = 0, y = 0, is_equipable = False, is_consumable = False) -> None:
        self.pos = Vec2(x,y)
        self.velocity = Vec2()
        self.size = Vec2(50,50)
        self.is_equipable = is_equipable
        self.is_consumable = is_consumable

        if self.is_equipable:
            self.ammo_type = None
        elif self.is_consumable:
            self.heal_amount = 30

        self.hitbox = pygame.rect.Rect(0,0,self.size.x,self.size.y)
        self.image = tl.item_textures[image_name]

item_list = {"barryGun": Item("barryGun", is_equipable=True),
             "fireHatchet": Item("fireHatchet", is_equipable=True),
             "melonSlice": Item("melonSlice", is_consumable=True)}
