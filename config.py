# config.py
# Screen settings
WIDTH = 800
HEIGHT = 800
FPS = 60

MAP_WIDTH = 3000
MAP_HEIGHT = 3000

# Player settings
BASE_SPEED = 2.0
ROTATION_SPEED = 3

# File paths
MAP_IMAGE_PATH = "Vannbassengan_3_2022-03-09.png"
PLAYER_IMAGE_PATH = "arrow.png"
PGW_PATH = "Vannbassengan_3_2022-03-09.pgw"
HS_PATH = "highscore.txt"
REPLAY_PATH = "replay.json"
ASTAR_PATH = "astar_path.json"

# Game mechanics
CONTROL_RADIUS = 20
CLIFF_THRESHOLD = 30

#Controllpoints, start and goal
CONTROL_POINTS = [
    {"pos": (326211, 6482779), "number": 1},
    #{"pos": (700, 700), "number": 2},
    #{"pos": (400, 600), "number": 3}
]

START_POS = (326213, 6482845)
GOAL_POS = (326423, 6482824)

