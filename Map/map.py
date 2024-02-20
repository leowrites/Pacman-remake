import numpy as np
import pygame

TILE_SIZE = (30, 30)
WALL_SIZE = (20, 20)
COIN_SIZE = (15, 15)
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
WALL_BLUE = pygame.Color(0, 0, 128)


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
        self.cherry_cord1 = [2, 4]
        self.cherry_cord2 = [4, 16]
        self.cherry_cord3 = [15, 2]
        self.cherry_cord4 = [16, 16]
        self.cherry_location = [self.cherry_cord1, self.cherry_cord2, 
                                self.cherry_cord3, self.cherry_cord4]
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
                current_location = (x * TILE_SIZE[0] + 15, y * TILE_SIZE[1] + 15)
                self.coins[y][x] = COIN_IMAGE.get_rect(center=current_location)
        return self.coins, total_coins

    def draw_coins(self, coins, COIN_IMAGE):
        for y, rows in enumerate(coins):
            for x in range(len(rows)):
                current = coins[y][x]
                current_location = (x * TILE_SIZE[0] + 15, y * TILE_SIZE[1] + 15)
                rect = COIN_IMAGE.get_rect(center=current_location)
                # creating the surface
                if current != 0:
                    self.window.blit(COIN_IMAGE, rect)

    def spawn_cherry_rects(self, CHERRY_IMAGE):
        cherry_rects = []
        for cherry_cord in self.cherry_location:
            current_location = (cherry_cord[0] * TILE_SIZE[0] + 15, cherry_cord[1] * TILE_SIZE[1] + 15)
            rect = CHERRY_IMAGE.get_rect(center=current_location)
            cherry_rects.append(rect)
        return cherry_rects

    def draw_cherry(self, cherrys, CHERRY_IMAGE):
        for cherry_cord in cherrys:
            self.window.blit(CHERRY_IMAGE, cherry_cord)

    def draw_map(self):
        for y, rows in enumerate(self.game_map):
            for x in range(len(rows)):
                current = self.game_map[y][x]
                current_rect = (x * TILE_SIZE[0] + 15, y * TILE_SIZE[1] + 15)
                surface = pygame.Surface(TILE_SIZE)
                rect = surface.get_rect(center=current_rect)
                # creating the surface
                if current == 1:
                    pygame.draw.rect(surface, BLACK, surface.get_rect())
                    self.window.blit(surface, rect)
                elif current == 0:
                    pygame.draw.rect(surface, WALL_BLUE, surface.get_rect())
                    self.window.blit(surface, rect)