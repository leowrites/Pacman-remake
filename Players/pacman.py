import random
import pygame
import numpy as np
from util.utility import (pixel_to_grid, grid_to_pixel, PacmanState)

UNIT_SIZE = 30
WALL_COLOR = pygame.Color(0, 0, 128)


class Pacman:
    # static variables for all pacman
    cur_location_on_grid = [10, 14]
    # this is for showing the pacman
    velocity_x = 1
    velocity_y = 1
    direction = "right"
    is_super = False

    def __init__(self, game_map, game_window, image):
        self.RIGHT = True
        self.LEFT = False
        self.UP = False
        self.DOWN = False

        self.moving = True
        self.alive = True

        self.score = 0
        self.game_map = game_map
        self.image = image
        self.current_image = 1
        self.mode = PacmanState.NORMAL
        self.rect = self.image[1].get_rect(center=
                                           grid_to_pixel(self.cur_location_on_grid[0], self.cur_location_on_grid[1]))

        # this is used to locate the pacman on the grid
        self.game_window = game_window

    def move(self):
        # need to map the pacman's location to the cell on a map
        # we can use a for loop to detect if the pacman collides with a block that has a value 1
        if self.RIGHT:
            self.rect.x += self.velocity_x
        elif self.LEFT:
            self.rect.x -= self.velocity_x
        elif self.UP:
            self.rect.y -= self.velocity_y
        elif self.DOWN:
            self.rect.y += self.velocity_y

    def eat_cherry(self, cherry_rects):
        """
        eat a cherry and become super
        :param cherry_rects: cherry rectangles
        :return: new cherry rectangles
        """
        for cherry_rect in cherry_rects:
            if pygame.rect.Rect.colliderect(self.rect, cherry_rect):
                self.mode = PacmanState.EAT_GHOST
                self.score += 500
                cherry_rects.remove(cherry_rect)
        return cherry_rects

    def get_pixel_ahead(self, ahead=1):
        xy_ahead_a = []
        xy_ahead_b = []
        if self.direction == "right":
            xy_ahead_a = (self.rect.topright[0] + ahead, self.rect.topright[1])
            xy_ahead_b = (self.rect.bottomright[0] + ahead, self.rect.bottomright[1])
        if self.direction == "left":
            xy_ahead_a = (self.rect.topleft[0] - ahead, self.rect.topleft[1])
            xy_ahead_b = (self.rect.bottomleft[0] - ahead, self.rect.bottomleft[1])
        if self.direction == "up":
            xy_ahead_a = (self.rect.topright[0], self.rect.topright[1] - ahead)
            xy_ahead_b = (self.rect.topleft[0], self.rect.topleft[1] - ahead)
        if self.direction == "down":
            xy_ahead_a = (self.rect.bottomright[0], self.rect.bottomright[1] + ahead)
            xy_ahead_b = (self.rect.bottomleft[0], self.rect.bottomleft[1] + ahead)
        return xy_ahead_a, xy_ahead_b

    def movement_restrictions(self):
        xy_ahead_a, xy_ahead_b = self.get_pixel_ahead()
        color_ahead_a = self.game_window.get_at(xy_ahead_a)
        color_ahead_b = self.game_window.get_at(xy_ahead_b)
        # if both color are channel, then moving is true, else its false
        if color_ahead_a == WALL_COLOR or color_ahead_b == WALL_COLOR:
            self.moving = False

    def eat_coin(self, coin_rects, total_coins):
        # if collides, return true and remove the coin
        top_left = pixel_to_grid(self.rect.topleft)
        top_right = pixel_to_grid(self.rect.topright)
        bottom_left = pixel_to_grid(self.rect.bottomleft)
        bottom_right = pixel_to_grid(self.rect.bottomright)

        corners = [top_left, top_right, bottom_left, bottom_right]
        for corner in corners:
            if coin_rects[corner[1]][corner[0]] != 0 and pygame.Rect.colliderect(self.rect, coin_rects[corner[1]][corner[0]]):
                coin_rects[corner[1]][corner[0]] = 0
                total_coins -= 1
                self.score += 100

        return coin_rects, total_coins

    def is_alive(self, ghosts):
        """
        :param ghost_rect: a list of ghost rectangles to be looped through to check if collides with pacman
        :return: nothing
        """
        for ghost in ghosts:
            if pygame.rect.Rect.colliderect(self.rect, ghost.rect):
                if self.mode == PacmanState.EAT_GHOST:
                    self.score += 2000
                    ghosts.remove(ghost)
                    return ghosts, ghost
                else:
                    self.alive = False
                    return ghosts, None
        return ghosts, None

    def draw(self):
        self.game_window.blit(self.image[self.current_image], self.rect)
