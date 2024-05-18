import pygame
import time
import math
import textures_library as tl

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

class Vec2():
    def __init__(self,x=0,y=0) -> None:
        self.x = x
        self.y = y


class Camera():
    pos = Vec2()
    velocity = Vec2()
    speed = 500

def main():
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    running = True

    camera = Camera()


    dt = 0
    current_map = [["placeholder", Vec2()]]
    selected_texture_name = "grass"
    while running:
        start_time = time.time()
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    camera.velocity.y -= camera.speed
                elif event.key == pygame.K_s:
                    camera.velocity.y += camera.speed
                elif event.key == pygame.K_a:
                    camera.velocity.x -= camera.speed
                elif event.key == pygame.K_d:
                    camera.velocity.x += camera.speed
                elif event.key == pygame.K_e:
                    export(current_map)
                elif event.key == pygame.K_1:
                    selected_texture_name = "grass"
                elif event.key == pygame.K_2:
                    selected_texture_name = "gravel"
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    camera.velocity.y += camera.speed
                elif event.key == pygame.K_s:
                    camera.velocity.y -= camera.speed
                elif event.key == pygame.K_a:
                    camera.velocity.x += camera.speed
                elif event.key == pygame.K_d:
                    camera.velocity.x -= camera.speed
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    paint_map(pygame.mouse.get_pos(), current_map, camera,selected_texture_name)
                elif event.button == pygame.BUTTON_RIGHT:
                    remove_tile(pygame.mouse.get_pos(), current_map, camera)

        update_camera_pos(camera, dt)



        screen.fill("purple")



        draw_grid(screen, camera)
        draw_map(screen, camera, current_map)
        draw_camera(screen)

        pygame.display.flip()
        end_time = time.time()
        dt = end_time - start_time

def export(current_map):
    file = open("export.mapdata", "w")
    for tile in current_map:
        line = "{} {} {}\n".format(tile[0], int(tile[1].x), int(tile[1].y))
        file.write(line)
    file.close()

def remove_tile(mouse_pos, current_map, camera:Camera):
    grid_pos_x = 50 * ((mouse_pos[0] + camera.pos.x)// 50)
    grid_pos_y = 50 * ((mouse_pos[1] + camera.pos.y)// 50)
    for tile in current_map:
        if tile[1].x == grid_pos_x and tile[1].y == grid_pos_y:
            current_map.remove(tile)

def paint_map(mouse_pos, current_map, camera:Camera, selected_texture_name):
    grid_pos_x = 50 * ((mouse_pos[0] + camera.pos.x)// 50)
    grid_pos_y = 50 * ((mouse_pos[1] + camera.pos.y)// 50)
    for tile in current_map:
        if tile[1].x == grid_pos_x and tile[1].y == grid_pos_y:
            current_map.remove(tile)

    current_map.append([selected_texture_name, Vec2(grid_pos_x, grid_pos_y)])    



def draw_map(screen:pygame.Surface, camera:Camera, current_map):
    for tile in current_map:
        texture = tl.map_textures[tile[0]]
        screen.blit(texture, (tile[1].x-camera.pos.x, tile[1].y-camera.pos.y))

    pass

def update_camera_pos(camera, dt):
    if camera.velocity.x != 0 or camera.velocity.y != 0:
        degrees_to_player = math.atan2(camera.velocity.y, camera.velocity.x)
        speed_y = math.sin(degrees_to_player)* camera.speed
        speed_x = math.cos(degrees_to_player)* camera.speed
    else:
        speed_y = 0
        speed_x = 0

    camera.pos.x += speed_x * dt
    camera.pos.y += speed_y * dt

def draw_grid(screen: pygame.Surface, camera:Camera):
    y = 0
    start_y = camera.pos.y // 50
    start_x = camera.pos.x // 50
    while y * 50 < SCREEN_HEIGHT:
        x = 0
        while x * 50 - camera.pos.x < SCREEN_WIDTH- camera.pos.x:
            rect = pygame.rect.Rect(x*50 - camera.pos.x + start_x*50 , y*50-camera.pos.y + start_y * 50, 50,50)
            pygame.draw.rect(screen,(255,255,255),rect,width=2)
            x += 1

        y += 1


def draw_camera(screen: pygame.Surface):
    pygame.draw.circle(screen, (255,0,0), (SCREEN_WIDTH/2, SCREEN_HEIGHT/2),20)
main()
pygame.quit()