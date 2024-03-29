import pygame
from pathfinding.core.grid import Grid
from random import randint
from enum import Enum

pygame.font.init()

SECONDS = 10
COUNTDOWN = SECONDS * 60
UNIT_SIZE = 30
TILE_SIZE = (30, 30)
WALL_SIZE = (20, 20)
COIN_SIZE = (15, 15)
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
WALL_BLUE = pygame.Color(0, 0, 128)

def load_images_pacman():
    PACMAN_RIGHT_OPEN = pygame.transform.smoothscale(pygame.image.load("assets/pacman_right_open.png"), (20, 20))
    PACMAN_RIGHT_CLOSED = pygame.transform.smoothscale(pygame.image.load("assets/pacman_right_closed.png"), (20, 20))
    PACMAN_LEFT_OPEN = pygame.transform.smoothscale(pygame.image.load("assets/pacman_left_open.png"), (20, 20))
    PACMAN_LEFT_CLOSED = pygame.transform.smoothscale(pygame.image.load("assets/pacman_left_closed.png"), (20, 20))
    PACMAN_DOWN_CLOSED = pygame.transform.smoothscale(pygame.image.load("assets/pacman_down_close.png"), (20, 20))
    PACMAN_DOWN_OPEN = pygame.transform.smoothscale(pygame.image.load("assets/pacman_down_open.png"), (20, 20))
    PACMAN_UP_OPEN = pygame.transform.smoothscale(pygame.image.load("assets/pacman_up_open.png"), (20, 20))
    PACMAN_UP_CLOSED = pygame.transform.smoothscale(pygame.image.load("assets/pacman_up_closed.png"), (20, 20))
    PACMAN_IMAGES = {
        1: PACMAN_RIGHT_OPEN,
        2: PACMAN_RIGHT_CLOSED,
        3: PACMAN_LEFT_OPEN,
        4: PACMAN_LEFT_CLOSED,
        5: PACMAN_DOWN_OPEN,
        6: PACMAN_DOWN_CLOSED,
        7: PACMAN_UP_OPEN,
        8: PACMAN_UP_CLOSED
    }
    return PACMAN_IMAGES


def load_images_ghost():
    INKY = pygame.transform.smoothscale(pygame.image.load("assets/inky.png"), (20, 20))
    PINKY = pygame.transform.smoothscale(pygame.image.load("assets/pinky.png"), (20, 20))
    BLINKY = pygame.transform.smoothscale(pygame.image.load("assets/blinky.png"), (20, 20))
    CLYDE = pygame.transform.smoothscale(pygame.image.load("assets/clyde.png"), (20, 20))
    IMAGES = {
        'inky': INKY,
        'pinky': PINKY,
        'blinky': BLINKY,
        'clyde': CLYDE
    }
    return IMAGES


def load_scared_ghosts():
    SCARED = pygame.transform.smoothscale(pygame.image.load("assets/scared.png"), (20, 20))
    return SCARED


def load_images_coin():
    COIN_IMAGE = pygame.transform.scale(pygame.image.load("assets/coin.png"), (7, 7))
    return COIN_IMAGE


def load_images_cherry():
    CHERRY_IMAGE = pygame.transform.scale(pygame.image.load('assets/cherry.png'), (30, 30))
    return CHERRY_IMAGE


def load_font():
    game_font = pygame.font.Font("assets/font.ttf", 20)
    return game_font


def load_game_over_font():
    game_over_font = pygame.font.Font("assets/font.ttf", 50)
    return game_over_font


def generate_grid(game_map):
    map_list = list(game_map)
    grid = Grid(matrix=map_list)
    return grid


def count_down():
    """
    because the game updates 60 times a second, function
    should subtract 1 from COUNTDOWN 60 times a second to acheive countdown
    :return: state of the pacman
    """
    # redo this with events
    global COUNTDOWN
    COUNTDOWN -= 1
    if COUNTDOWN == 0:
        # resets the clock
        COUNTDOWN = SECONDS * 60
        return PacmanState.NORMAL
    return PacmanState.EAT_GHOST


def generate_random_loc(game_map):
    cord = [randint(1, 18), randint(1, 18)]
    while game_map[cord[0]][cord[1]] != 1:
        cord = generate_random_loc(game_map)
    return cord


def pixel_to_grid(pixel):
    return [pixel[0] // UNIT_SIZE, pixel[1] // UNIT_SIZE]

def grid_to_pixel(x, y):
    return [x * UNIT_SIZE + 15, y * UNIT_SIZE + 15]

class PacmanState(Enum):
    EAT_GHOST = 0
    NORMAL = 1

class GhostState(Enum):
    CHASE = 0
    HIDE = 1
    SCARED = 2

class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3