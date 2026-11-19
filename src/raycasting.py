import pygame as pg
import math
from settings import *

class RayCasting:
    def __init__(self, game):
        self.game = game

    def ray_cast(self):
        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos
        ray_angle = self.game.player.angle - HALF_FOV + 0.001
        for ray in range(NUM_RAYS):
            seno_a = math.sin(ray_angle)
            cosseno_a = math.cos(ray_angle)

            #RAIOS COM INTERSEÇÕES HORIZONTAIS:

            if seno_a > 0:
                y_hor, dy = (y_map + 1, 1)
            else:
                y_hor, dy = (y_map -1e-6, -1)
            
            profundidade_horizontal = (y_hor - oy) / seno_a
            x_hor = ox + profundidade_horizontal * cosseno_a

            delta_profundidade = dy / seno_a
            dx = delta_profundidade * cosseno_a

            for i in range(MAX_DEPTH):
                tile_hor = int(x_hor), int(y_hor)
                if tile_hor in self.game.map.world_map:
                    break
                x_hor += dx
                y_hor += dy
                profundidade_horizontal += delta_profundidade
            
            #RAIOS COM INTERSEÇÕES VERTICAIS:
            if cosseno_a > 0:
                x_vert, dx = (x_map + 1, 1)
            else:
                x_vert, dx = (x_map -1e-6, -1)
            profundidade_vertical = (x_vert - ox) / cosseno_a

            y_vert = oy + profundidade_vertical * seno_a
            delta_profundidade = dx / cosseno_a
            dy = delta_profundidade * seno_a

            for i in range(MAX_DEPTH):
                tile_vert = int(x_vert), int(y_vert)
                if tile_vert in self.game.map.world_map:
                    break
                x_vert += dx
                y_vert += dy
                profundidade_vertical += profundidade_vertical

            # PROFUNDIDADE

        if profundidade_vertical < profundidade_horizontal:
            profundidade = profundidade_vertical
        else:
            profundidade = profundidade_horizontal

        
            
            ray_angle += DELTA_ANGLE
    def update(self):
        self.ray_cast()