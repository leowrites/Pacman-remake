from pathfinding.finder.a_star import AStarFinder
from pathfinding.finder.best_first import BestFirst
from pathfinding.core.grid import Grid
from pygame import time, event
from util.utility import (UNIT_SIZE, grid_to_pixel)
from collections import deque

class Ghost:
    def __init__(self, init_location, image, aggression, game_window, mode):
        self.respawn_cooldown = 300
        self.init_location = init_location
        self.location = init_location
        self.aggression = aggression
        self.game_window = game_window
        self.mode = mode
        self.moving = True
        self.image = image
        self.surface = image
        self.velocity_x = self.velocity_y = 1
        self.game_window = game_window
        self.direction = 'right'
        self.spawn_location = grid_to_pixel(self.location[0], self.location[1])
        self.rect = self.surface.get_rect(center=self.spawn_location)
        self.path = deque([])
        self.name = ''
        self.aim = []

    def draw(self):
        self.game_window.blit(self.surface, self.rect)

    def find_path(self, grid, final):
        start = grid.node(self.location[0], self.location[1])
        end = grid.node(final[0], final[1])
        #  come back to this (maybe use gbfs? and parallelize?)
        finder = BestFirst()
        self.path = deque(finder.find_path(start, end, grid)[0])
        Grid.cleanup(grid)

    def move(self, grid, final):
        # follows the path by multiplying next cord into pixels
        try:
            if not self.path:
                self.find_path(grid, final)
            next_x, next_y = grid_to_pixel(self.path[0][0], self.path[0][1])
            if self.rect.centerx == next_x and self.rect.centery == next_y:
                self.path.popleft()
            elif self.rect.centerx < next_x:
                self.rect.centerx += self.velocity_x
            elif self.rect.centerx > next_x:
                self.rect.centerx -= self.velocity_x
            elif self.rect.centery > next_y:
                self.rect.centery -= self.velocity_y
            elif self.rect.centery < next_y:
                self.rect.centery += self.velocity_y

            self.location = [round((self.rect.x - 15) / 30),
                             round((self.rect.y - 15) / 30)]
        except IndexError:
            print("{}: no path found! Cord:{}".format(self.name, final))

    def respawn_timer(self):
        # TYPE = event.custom_type()
        # time.set_timer(event.Event(TYPE, {}))
        if self.respawn_cooldown > 0:
            self.respawn_cooldown -= 1
            self.surface = self.image
            self.rect = self.surface.get_rect(center=self.spawn_location)
            self.moving = False
            return False
        else:
            self.location = [round((self.rect.x - 15) / UNIT_SIZE), 
                             round((self.rect.y - 15) / UNIT_SIZE)]
            self.moving = True
            self.respawn_cooldown = 500
            return True
