import pygame
from config import WIDTH, HEIGHT

# These will be set from main.py to control map offset
camera_x = 0
camera_y = 0

def set_camera_offset(x, y):
    global camera_x, camera_y
    camera_x = x
    camera_y = y

def draw_path(surface, path, color=(0, 255, 0), width=3):
    if len(path) > 1:
        pygame.draw.lines(surface, color, False, [(x - camera_x, y - camera_y) for x, y in path], width)

def draw_debug_pixel(surface, pixel, color=(255, 0, 0)):
    from config import WIDTH, HEIGHT
    global camera_x, camera_y

    screen_x = pixel[0] - camera_x
    screen_y = pixel[1] - camera_y

    if 0 <= screen_x < WIDTH and 0 <= screen_y < HEIGHT:
        pygame.draw.circle(surface, color, (int(screen_x), int(screen_y)), 1)
        pygame.display.update()

