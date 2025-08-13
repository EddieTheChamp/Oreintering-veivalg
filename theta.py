import heapq
import math
import pygame
from terrain_logic import pixel_to_map

# ---- CONFIGURABLE PARAMETERS ----
SAMPLE_STEP = 5  # pixels between samples for terrain speed averaging
MIN_SPEED = 0.3    # fallback minimum speed if terrain multiplier is too low


def theta_star(start, goal, terrain, is_passable_fn, debug_draw_fn=None):
    start = tuple(map(int, start))
    goal = tuple(map(int, goal))
    visited = set()
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    MAX_VISITS = 50000  # Reasonable fail-safe limit



    while open_set:
        _, current = heapq.heappop(open_set)

        print(f"➡️ Exploring: {current} — Visited so far: {len(visited)}")  # ADD THIS

        if current in visited:
            continue
        visited.add(current)
        if debug_draw_fn:
            debug_draw_fn(current)



        if len(visited) % 100 == 0:
            print(f"🔄 Visited {len(visited)} nodes...")
        if len(visited) > MAX_VISITS:
            print(" Search aborted: too many expansions.")
            return None
        GOAL_RADIUS = 20  # or whatever your control radius is

        if euclidean_distance(current, goal) <= GOAL_RADIUS:
            return reconstruct_path(came_from, current)

        for neighbor in get_neighbors(current):
            if not is_passable_fn(neighbor):
                continue

            # Check line of sight from parent if exists
            parent = came_from.get(current, current)

            if has_line_of_sight(terrain, parent, neighbor):
                tentative_parent = parent
            else:
                tentative_parent = current  # Fall back to A* behavior

            tentative_g = g_score[tentative_parent] + estimate_cost(terrain, tentative_parent, neighbor)
            if tentative_g < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = tentative_parent
                g_score[neighbor] = tentative_g
                f_score = tentative_g + euclidean_distance(neighbor, goal)
                heapq.heappush(open_set, (f_score, neighbor))


    return None  # No path found


def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from and came_from[current] != current:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path


GRID_STEP = 20 # <-- Adjust grid resolution here

def get_neighbors(pos):
    x, y = pos
    directions = [
        (-1, -1), (0, -1), (1, -1),
        (-1,  0),          (1,  0),
        (-1,  1), (0,  1), (1,  1)
    ]
    neighbors = []
    for dx, dy in directions:
        nx = x + dx * GRID_STEP
        ny = y + dy * GRID_STEP
        neighbors.append((nx, ny))
    return neighbors



def euclidean_distance(a, b):
    return math.hypot(b[0] - a[0], b[1] - a[1])


def has_line_of_sight(terrain, a, b):
    # Sample points along the line from a to b
    ax, ay = a
    bx, by = b
    dx = bx - ax
    dy = by - ay
    dist = math.hypot(dx, dy)
    steps = int(dist / SAMPLE_STEP)

    for i in range(1, steps):
        t = i / steps
        x = ax + dx * t
        y = ay + dy * t
        map_x, map_y = pixel_to_map(x, y)
        terrain_type = terrain.get_terrain_type(map_x, map_y)
        if not is_passable_terrain(terrain_type):
            return False

    return True


def is_passable_terrain(terrain_name):
    name = terrain_name.lower()
    return "vann" not in name and "upasserbart" not in name


def estimate_cost(terrain, a, b):
    # Estimate cost from a to b based on terrain speed multipliers
    ax, ay = a
    bx, by = b
    dx = bx - ax
    dy = by - ay
    dist = math.hypot(dx, dy)
    steps = int(dist / SAMPLE_STEP)

    multipliers = []
    for i in range(steps + 1):
        t = i / steps if steps else 0
        x = ax + dx * t
        y = ay + dy * t
        map_x, map_y = pixel_to_map(x, y)
        m = terrain.get_speed_multiplier(map_x, map_y)
        multipliers.append(max(m, MIN_SPEED))

    avg_speed = sum(multipliers) / len(multipliers) if multipliers else 1.0
    return dist / avg_speed
