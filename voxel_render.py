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


@njit(fastmath=True)
def ray_casting(screen_array, player_pos, player_angle, player_height, player_pitch,
                screen_width, screen_height, delta_angle, ray_distance, h_fov, scale_height):

    screen_array[:] = np.array([0, 0, 0])
    y_buffer = np.full(screen_width, screen_height)

    ray_angle = player_angle - h_fov
    for num_ray in range(screen_width):
        first_contact = False
        sin_a = math.sin(ray_angle)
        cos_a = math.cos(ray_angle)

        for depth in range(1, ray_distance):
            x = int(player_pos[0] + depth * cos_a)
            if 0 < x < map_width:
                y = int(player_pos[1] + depth * sin_a)
                if 0 < y < map_height:

                    # remove fisheye effects
                    depth *= math.cos(player_angle - ray_angle)
                    height_on_screen = int((player_height - height_map[x, y][0])/depth*scale_height + player_pitch)

                    # remove unnecessary drawings
                    if not first_contact:
                        y_buffer[num_ray] = min(height_on_screen, screen_height)
                        first_contact = True

                    # remove mirror bug
                    if height_on_screen < 0:
                        height_on_screen = 0

                    # draw vertical lines
                    if height_on_screen < y_buffer[num_ray]:
                        for screen_y in range(height_on_screen, y_buffer[num_ray]):
                            screen_array[num_ray, screen_y] = color_map[x, y]
                        y_buffer[num_ray] = height_on_screen
        ray_angle += delta_angle
    return screen_array


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
        self.screen_array = ray_casting(self.screen_array, self.player.pos, self.player.angle,
                                        self.player.height, self.player.pitch, self.app.width,
                                        self.app.height, self.delta_angle, self.ray_distance,
                                        self.h_fov, self.scale_height)

    def draw(self):
        self.app.screen.blit(pg.surfarray.make_surface(self.screen_array), (0, 0))

