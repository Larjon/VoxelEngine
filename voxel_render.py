import pygame as pg
from numba import njit
import numpy as np
import math

height_map_img = pg.image.load('img/height_map.jpg')
height_map = pg.surfarray.array3d(height_map_img)

color_map_img = pg.image.load('img/color_map.jpg')
color_map = pg.surfarray.array3d(color_map_img)

map_height = len(height_map[0])
map_width = len(height_map)


class VoxelRender:
    def __init__(self, app):
        self.app = app                                   # app - an instance od the APP class
        self.player = app.player                         # player - an instance of the Player class
        self.fov = math.pi/3                             # fov - field of view
        self.h_fov = self.fov/2
        self.num_rays = app.width                        # num_rays - numbers of rays
        self.delta_angle = self.fov / self.num_rays      # delta_angle - angle between rays
        self.ray_distance = 2000                         # ray_distance - ray length
        self.scale_height = 620                          # scale_height - scale factor
        self.screen_array = np.full((app.width, app.height, 3), (0, 0, 0))   # screen_array - 3D array to display Images

    def update(self):
        self.screen_array = np.random.randint(0, 255, size=self.screen_array.shape)

    def draw(self):
        self.app.screen.blit(pg.surfarray.make_surface(self.screen_array), (0, 0))

