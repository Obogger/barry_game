import pygame
import time
import random
import math
import textures_library as tl
import item_library
import copy

from global_classes import Vec2

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

class Player():
    health = 100
    max_health = 100
    primary_item = None
    inventory:list[item_library.Item] = []
    pos = Vec2()
    speed = 400
    velocity = Vec2()
    size = Vec2()
    size.x = 100
    size.y = 100
    hitbox = pygame.rect.Rect(pos.x - size.x / 2+ SCREEN_WIDTH/2,pos.y- size.y / 2+SCREEN_HEIGHT/2,size.x,size.y)
    image = pygame.transform.scale(pygame.image.load("sprites/characters/player.png"), (size.x ,size.y))

class Enemy():
    def __init__(self) -> None:
        self.pos = Vec2()
        self.health = 100
        self.speed = 250
        self.velocity = Vec2()
        self.size = Vec2()
        self.size.x = 100
        self.size.y = 100
        self.hitbox = pygame.rect.Rect(self.pos.x - self.size.x / 2+ SCREEN_WIDTH/2,self.pos.y- self.size.y / 2+SCREEN_HEIGHT/2,self.size.x,self.size.y)
        self.image = pygame.transform.scale(pygame.image.load("sprites/characters/jared_of_norwegian_descent.png"), (self.size.x,self.size.y))

    
    def change_velocity(self, player):
        dt_y = self.pos.y - player.pos.y
        dt_x = self.pos.x - player.pos.x
        if dt_y != 0 or dt_x != 0:
            if math.sqrt(abs(abs(dt_y**2) + abs(dt_x**2))) < 100:
                self.velocity.x = 0
                self.velocity.y = 0
 
            else:
                degrees_to_player = math.atan2((self.pos.y-player.pos.y), (self.pos.x-player.pos.x))+ math.radians(random.randint(-20,20))
                speed_y = math.sin(degrees_to_player)* self.speed 
                speed_x = math.cos(degrees_to_player)* self.speed  
                self.velocity.x = -speed_x
                self.velocity.y = -speed_y
        else:
            self.velocity.x = 0
            self.velocity.y = 0

class Camera():
    def __init__(self) -> None:
        self.pos = Vec2()

class Particle():
    def __init__(self) -> None:
        self.pos = Vec2()
        self.velocity = Vec2()
        self.size = Vec2()
        self.size.x = 20
        self.size.y = 20
        self.hitbox = pygame.rect.Rect(self.pos.x - self.size.x / 2+ SCREEN_WIDTH/2,self.pos.y- self.size.y / 2+SCREEN_HEIGHT/2,self.size.x,self.size.y)
        self.image = pygame.transform.scale(pygame.image.load("sprites/particle/bulbert.png"), (self.size.x,self.size.y))

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    pygame.font.init()
    standard_font = pygame.font.Font(size=30)

    player = Player()

    running = True

    last_dt = 1

    map_data, item_list = load_map()

    camera = Camera()

    entity_list = []
    bullet_list = []

    is_inventory_open = False
    start_invetory_pos = None
    end_invetory_pos = None

    while running:
        start_time = time.time()
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_k:
                    entity_list.append(Enemy())
                    entity_list[-1].pos.x = random.randint(0,400)
                    entity_list[-1].pos.y = random.randint(0,800)
                elif event.key == pygame.K_TAB:
                    is_inventory_open = True if is_inventory_open == False else False
                elif event.key == pygame.K_BACKSPACE:
                    drop_item(player, item_list)
                elif event.key == pygame.K_e:
                    pick_up_item(player, item_list)
                elif event.key == pygame.K_w:
                    player.velocity.y -= player.speed
                elif event.key == pygame.K_s:
                    player.velocity.y += player.speed
                elif event.key == pygame.K_a:
                    player.velocity.x -= player.speed
                elif event.key == pygame.K_d:
                    player.velocity.x += player.speed
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:         
                    if is_inventory_open:
                        start_invetory_pos = pygame.mouse.get_pos()
                        end_invetory_pos = None
                    else:
                        print("use_item")
                        bullet_list.append(use_item(player, pygame.mouse.get_pos())) if use_item(player, pygame.mouse.get_pos()) != None else None
            elif event.type ==pygame.MOUSEBUTTONUP:
                if event.button == pygame.BUTTON_LEFT:         
                    if is_inventory_open:
                        start_invetory_pos = None
                        end_invetory_pos = pygame.mouse.get_pos()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    player.velocity.y += player.speed
                elif event.key == pygame.K_s:
                    player.velocity.y -= player.speed
                elif event.key == pygame.K_a:
                    player.velocity.x += player.speed
                elif event.key == pygame.K_d:
                    player.velocity.x -= player.speed


        update_pos(player, entity_list,last_dt, camera)
        update_bullets(bullet_list, camera, entity_list, last_dt)
        update_camera(camera,player)


        #________________ DRAW SECTION ________________
        screen.fill((32,32,60))
        render_data(screen, map_data, camera)

        render_etities(screen,player,entity_list,camera)
        render_bullets(screen, bullet_list, camera)
        render_items(screen,camera,item_list)
    
        if is_inventory_open:
            open_inventory(screen,player, start_invetory_pos, end_invetory_pos, item_list)
            end_invetory_pos = None
        pygame.draw.rect(screen, (255,0,0),player.hitbox,width=3)
        pygame.draw.circle(screen, (255,0,0), (player.pos.x + 2.5 - camera.pos.x+player.size.x/2, player.pos.y - 2.5 -camera.pos.y+player.size.y/2), 5.0, 5)





        dt_surface = standard_font.render("{:.2f} FPS".format(1 / last_dt), True, color=(255,255,255))
        screen.blit(dt_surface, (0,0))

        dt_surface = standard_font.render("Health {}".format(player.health), True, color=(255,255,255))
        screen.blit(dt_surface, (0,600))
        pygame.display.flip()

        end_time = time.time()

        dt = end_time - start_time
        last_dt = dt

selcted_item = None

def open_inventory(screen:pygame.Surface, player: Player, start_mouse_pos, end_mouse_pos, item_list):
    global selcted_item
    inventory_screen_rect = pygame.rect.Rect(100,100,500,500)
    pygame.draw.rect(screen,(150,150,150),inventory_screen_rect)

    primary_slot_rect = pygame.rect.Rect(150,150,50,50)
    pygame.draw.rect(screen,(50,50,50),primary_slot_rect)

    index = 0
    boxes = []
    for item in player.inventory:
        if item:
            box = pygame.rect.Rect(250, 150 + (index * 50),50,50)
            if start_mouse_pos:
                if box.collidepoint(start_mouse_pos):
                    new_mouse_pos = pygame.mouse.get_pos()
                    selcted_item = item
                    screen.blit(item.image, pygame.rect.Rect(new_mouse_pos[0], new_mouse_pos[1],50,50))
                    index += 1
                else:
                    screen.blit(item.image, box)
                    boxes.append(box)
                    index += 1
            else:
                screen.blit(item.image, box)
                boxes.append(box)
                index += 1

    print(start_mouse_pos)
    if start_mouse_pos and player.primary_item:
        if primary_slot_rect.collidepoint(start_mouse_pos):
            print("dsdsd")
            new_mouse_pos = pygame.mouse.get_pos()
            selcted_item = player.primary_item
            screen.blit(player.primary_item.image, pygame.rect.Rect(new_mouse_pos[0], new_mouse_pos[1],50,50))    
        elif player.primary_item: 
            screen.blit(player.primary_item.image, primary_slot_rect)
    elif player.primary_item: 
        screen.blit(player.primary_item.image, primary_slot_rect)

    if end_mouse_pos:
        if primary_slot_rect.collidepoint(end_mouse_pos) and selcted_item:
            if player.primary_item:
                player.inventory.append(player.primary_item)

            player.primary_item = selcted_item
            player.inventory.remove(selcted_item)
        elif primary_slot_rect.collidepoint(end_mouse_pos) != True and selcted_item == player.primary_item:
            player.inventory.append(player.primary_item)
            player.primary_item = None
        elif inventory_screen_rect.collidepoint(end_mouse_pos) != True and selcted_item:
            item = selcted_item
            player.inventory.remove(selcted_item)
            item.pos.x = player.pos.x + 100
            item.pos.y = player.pos.y + 100
            item_list.append(item)

        selcted_item = False

    return
def pick_up_item(player, item_list):
    for item in item_list:
        if item.hitbox.colliderect(player.hitbox):
            print("picked")
            player.inventory.append(item)
            item_list.remove(item)
            print(player.inventory)
            return


def drop_item(player:Player, item_list):
    if player.primary_item:
        item = player.primary_item
        player.primary_item = None
        item.pos.x = player.pos.x + 100
        item.pos.y = player.pos.y + 100

        item_list.append(item)



def render_items(screen:pygame.Surface, camera: Camera, item_list:list[item_library.Item]):
    for item in item_list:
        item.hitbox.x = item.pos.x - camera.pos.x
        item.hitbox.y = item.pos.y - camera.pos.y
        screen.blit(item.image, (item.pos.x - camera.pos.x, item.pos.y-camera.pos.y))
        #pygame.draw.rect(screen, (255,0,0), item.hitbox, 3)



def render_bullets(screen, bullet_list, camera):
    for entity in bullet_list:
        pygame.draw.rect(screen, (255,0,0),entity.hitbox,width=3)
        screen.blit(entity.image, (entity.pos.x - camera.pos.x, entity.pos.y - camera.pos.y))
        

def update_bullets(bullet_list:list[Particle], camera, entity_list: list[Enemy], dt):
    for bullet in bullet_list:
        bullet.pos.x += bullet.velocity.x * dt
        bullet.pos.y += bullet.velocity.y * dt

        bullet.hitbox.x = bullet.pos.x - camera.pos.x
        bullet.hitbox.y = bullet.pos.y - camera.pos.y

        for entity in entity_list:
            if bullet.hitbox.colliderect(entity.hitbox):
                print("hit")
                entity.health -= 30
                if entity.health <= 0:
                    entity_list.remove(entity)
                bullet_list.remove(bullet)
                break


def use_item(player:Player, mouse_pos):
     
    if player.primary_item:
        item = player.primary_item
    else:
        return
    print(player.inventory)
    if item.is_equipable:
        particle = Particle()
        particle.pos.x = player.pos.x - particle.size.x / 2 + player.hitbox.width / 2
        particle.pos.y = player.pos.y - particle.size.y / 2 + player.hitbox.height / 2

        dt_y = SCREEN_HEIGHT/2 - mouse_pos[1]
        dt_x = SCREEN_WIDTH/2 - mouse_pos[0]
        if dt_y != 0 or dt_x != 0:
            degrees_to_mouse = math.atan2(dt_y, dt_x) + math.radians(random.randint(-10,10))
            speed_y = math.sin(degrees_to_mouse)* 1000
            speed_x = math.cos(degrees_to_mouse)* 1000
            particle.velocity.x = -speed_x
            particle.velocity.y = -speed_y
        else:
            particle.velocity.x = 0
            particle.velocity.y = 0
        return particle
    elif item.is_consumable:
        player.primary_item = None
        heal(player,item.heal_amount)


def update_camera(camera:Camera, player: Player):
    camera.pos.x = (player.pos.x-SCREEN_WIDTH/2) + player.hitbox.width / 2
    camera.pos.y = (player.pos.y-SCREEN_HEIGHT/2) + player.hitbox.height / 2


def render_etities(screen, player:Player, entity_list, camera):
    for entity in entity_list:
        screen.blit(entity.image, (entity.pos.x - camera.pos.x, entity.pos.y - camera.pos.y))
        pygame.draw.rect(screen, (255,0,0),entity.hitbox,width=3)
        pygame.draw.line(screen,(255,255,255),(player.pos.x-camera.pos.x + player.hitbox.width / 2, player.pos.y-camera.pos.y + player.hitbox.height / 2),(entity.pos.x - camera.pos.x + player.hitbox.width / 2, entity.pos.y - camera.pos.y + player.hitbox.height / 2),5)

    screen.blit(player.image, (player.pos.x-camera.pos.x, player.pos.y-camera.pos.y))
    if player.primary_item:
        screen.blit(player.primary_item.image, (SCREEN_WIDTH/2,SCREEN_HEIGHT-100))


    if player.primary_item:
        screen.blit(player.primary_item.image, (player.pos.x-camera.pos.x+player.size.x / 2, player.pos.y-camera.pos.y - 10+ player.size.y / 2))
def update_pos(player: Player, entity_list: list[Enemy], dt, camera):
    if player.velocity.x != 0 or player.velocity.y != 0:
        degrees_to_player = math.atan2(player.velocity.y, player.velocity.x)
        speed_y = math.sin(degrees_to_player)* player.speed
        speed_x = math.cos(degrees_to_player)* player.speed
    else:
        speed_y = 0
        speed_x = 0

    player.pos.x += speed_x * dt
    player.pos.y += speed_y * dt

    for entity in entity_list:
        entity.change_velocity(player)
        entity.pos.x += entity.velocity.x * dt
        entity.pos.y += entity.velocity.y * dt

        entity.hitbox.x = entity.pos.x - camera.pos.x
        entity.hitbox.y = entity.pos.y - camera.pos.y

        if entity.hitbox.colliderect(player.hitbox):
            player.health -= 1



def load_map():
    map_file = open("export.mapdata", "r")
    map_lines = map_file.readlines()
    map_file.close()

    map_data = []
    item_data = []
    item_list = []

    item_iteration = False
    for line in map_lines:
        if line == "ITEMS\n":
            item_iteration = True
        elif item_iteration:
            split_line = line.split()
            texture_name, x, y = split_line[0], int(split_line[1]), int(split_line[2])
            item_data.append([texture_name,x,y])
        else:
            split_line = line.split()
            texture_name, x, y = split_line[0], int(split_line[1]), int(split_line[2])
            map_data.append([texture_name,x,y])
    
    for item_d in item_data:
        item = copy.deepcopy(item_library.item_list[item_d[0]])
        item.pos.x, item.pos.y = int(item_d[1]), int(item_d[2])

        item_list.append(item)

    print(item_data)
    return map_data, item_list
    
def render_data(screen, map_data, camera):
    for line in map_data:
        screen.blit(tl.map_textures[line[0]], (line[1] - camera.pos.x, line[2]- camera.pos.y))

def heal(entity:Player, heal_amount):
    entity.health = entity.health + heal_amount if entity.health + heal_amount <= entity.max_health else entity.max_health
        




main()

pygame.quit()