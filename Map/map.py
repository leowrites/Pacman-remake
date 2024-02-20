import numpy as np
import pygame
from util.utility import (
    TILE_SIZE, WALL_BLUE, BLACK, grid_to_pixel
)


class Map:
    """
    creates a map object
    """
    def __init__(self, game):
        """
        use the game to draw on its screen
        load the images
        :param game: a game window
        """
        self.cherry_location = [[2, 4], [4, 16], [15, 2], [16, 16]]
        self.game_map = np.array(
            [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
            [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0],
            [0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0],
            [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0],
            [0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0],
            [0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        )
        # self.coins = np.zeros((20, 20), dtype=pygame.Rect)
        self.coins = None
        self.window = game

    def spawn_coins(self, COIN_IMAGE):
        """
        spawn the coins
        :return: coins array, total number of coins, coin rectangles stored in a list
        """
        total_coins = np.sum(1 - self.game_map)
        # initialize the array with total_coins zeros
        self.coins = np.zeros((20, 20), dtype=pygame.Rect)
        for y, rows in enumerate(self.game_map):
            for x in range(len(rows)):
                # coin cannot spawn inside jail?
                current = self.game_map[y][x]
                if current == 0 or [x, y] in self.cherry_location:
                    continue
                current_location = grid_to_pixel(x, y)
                self.coins[y][x] = COIN_IMAGE.get_rect(center=current_location)
        return self.coins, total_coins

    def draw_coins(self, coins, COIN_IMAGE):
        for y, rows in enumerate(coins):
            for x in range(len(rows)):
                # creating the surface
                if coins[y][x] != 0:
                    self.window.blit(COIN_IMAGE, coins[y][x])

    def spawn_cherry_rects(self, CHERRY_IMAGE):
        cherry_rects = []
        for cherry_cord in self.cherry_location:
            current_location = grid_to_pixel(cherry_cord[0], cherry_cord[1])
            rect = CHERRY_IMAGE.get_rect(center=current_location)
            cherry_rects.append(rect)
        return cherry_rects

    def draw_cherry(self, cherrys, CHERRY_IMAGE):
        for cherry_cord in cherrys:
            self.window.blit(CHERRY_IMAGE, cherry_cord)

    def draw_map(self):
        surface = pygame.Surface(TILE_SIZE)
        for y, rows in enumerate(self.game_map):
            for x in range(len(rows)):
                rect = surface.get_rect(center=grid_to_pixel(x, y))
                # creating the surface
                if self.game_map[y][x]:
                    pygame.draw.rect(surface, BLACK, surface.get_rect())
                else:
                    pygame.draw.rect(surface, WALL_BLUE, surface.get_rect())
                self.window.blit(surface, rect)
