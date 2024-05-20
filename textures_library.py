import pygame
import os

def init():
    dir = "sprites/terrain/"
    for map_texture_file in os.listdir(dir):
        item_name = list(map_texture_file)
        while "_" in item_name:
            under_index = item_name.index("_")
            item_name.pop(under_index)
            item_name[under_index] = chr(ord(item_name[under_index]) - 32)
        
        item_name = "".join(item_name[:-4])
        map_textures[item_name] = pygame.transform.scale(pygame.image.load("".join([dir, map_texture_file])), (50,50))


    dir = "sprites/items/"
    for map_item_file in os.listdir(dir):
        item_name = list(map_item_file)
        while "_" in item_name:
            under_index = item_name.index("_")
            item_name.pop(under_index)
            item_name[under_index] = chr(ord(item_name[under_index]) - 32)
        
        item_name = "".join(item_name[:-4])
        item_textures[item_name] = pygame.transform.scale(pygame.image.load("".join([dir, map_item_file])), (50,50))

map_textures = {}

item_textures = {}

init()
