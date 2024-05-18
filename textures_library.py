import pygame

map_textures = {"grass" : pygame.transform.scale(pygame.image.load("sprites/terrain/grass.png"), (50,50)),
                "gravel" : pygame.transform.scale(pygame.image.load("sprites/terrain/gravel.png"), (50,50)),
                "placeholder" : pygame.transform.scale(pygame.image.load("sprites/terrain/placeholder.png"), (50,50))}

item_textures = {"barry gun": pygame.transform.scale(pygame.image.load("sprites/items/barry_gun.png"), (50,50))}