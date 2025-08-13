import pygame
import sys
from config import WIDTH, HEIGHT, MAP_IMAGE_PATH, START_POS, GOAL_POS
from terrain_logic import TerrainMap, map_to_pixel, pixel_to_map
from theta import theta_star, is_passable_terrain
from drawing import draw_path, draw_debug_pixel, set_camera_offset


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Theta* Pathfinding Visualization")

# Load map and terrain
map_image = pygame.image.load(MAP_IMAGE_PATH).convert()
terrain = TerrainMap("Shapefile/vannbassengene_areas.shp")

# Convert UTM to pixel
start_px = map_to_pixel(*START_POS)
goal_px = map_to_pixel(*GOAL_POS)
start = (int(start_px[0]), int(start_px[1]))
goal = (int(goal_px[0]), int(goal_px[1]))

# Compute camera offset to center on start
camera_x = start[0] - WIDTH // 2
camera_y = start[1] - HEIGHT // 2
set_camera_offset(camera_x, camera_y)

def apply_offset(pos):
    return (pos[0] - camera_x, pos[1] - camera_y)

# ✅ Fix draw_debug_pixel so it accounts for camera offset
def draw_debug_pixel(surface, pixel, color=(255, 0, 0)):
    screen_x = pixel[0] - camera_x
    screen_y = pixel[1] - camera_y
    if 0 <= screen_x < WIDTH and 0 <= screen_y < HEIGHT:
        pygame.draw.circle(surface, color, (int(screen_x), int(screen_y)), 1)
        pygame.display.update()
        pygame.event.pump()
        pygame.time.delay(1)

# Draw map so debug pixels show
screen.blit(map_image, (-camera_x, -camera_y))
pygame.display.flip()

# Passability check
def is_passable(pixel):
    x, y = pixel
    map_x, map_y = pixel_to_map(x, y)
    terrain_type = terrain.get_terrain_type(map_x, map_y)
    return is_passable_terrain(terrain_type)

# Run Theta*
print("🟡 Running Theta* pathfinding...")
path = theta_star(start, goal, terrain, is_passable,
                  debug_draw_fn=lambda p: draw_debug_pixel(screen, p))

if not path:
    print("❌ No path found.")
else:
    print(f"✅ Path found with {len(path)} steps.")

# Main loop
running = True
while running:
    screen.blit(map_image, (-camera_x, -camera_y))

    if path:
        draw_path(screen, path)
        pygame.draw.circle(screen, (0, 0, 255), apply_offset(start), 6)
        pygame.draw.circle(screen, (255, 255, 0), apply_offset(goal), 6)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
sys.exit()
