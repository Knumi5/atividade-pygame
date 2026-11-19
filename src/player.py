if __package__:
    from .settings import *
else:
    from settings import *
import pygame as pg
import math


class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE

    def movement(self):
        seno_a = math.sin(self.angle)
        cosseno_a = math.cos(self.angle)
        dx, dy = 0, 0
        speed = PLAYER_SPEED * self.game.delta_time
        speed_sen = speed * seno_a
        speed_cos = speed * cosseno_a

        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            dx += speed_cos
            dy += speed_sen
        if keys[pg.K_s]:
            dx += - speed_cos
            dy += - speed_sen
        if keys[pg.K_a]:
            dx += speed_sen
            dy += -speed_cos
        if keys[pg.K_d]:
            dx += -speed_sen
            dy += speed_cos

        self.checar_colisao_parede(dx, dy)

    def mouse_control(self):
        mx, _ = pg.mouse.get_pos()
        self.rel = pg.mouse.get_rel()[0]
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
        self.angle += self.rel * MOUSE_SENSITIVITY * self.game.delta_time
        self.angle %= math.tau  # tau = 2 * pi

        if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
            pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
            pg.mouse.get_rel()

    def checar_parede(self, x, y):
        return (x, y) not in self.game.map.world_map

    def checar_colisao_parede(self, dx, dy):
        if self.checar_parede(int(self.x + dx), int( self.y)):
            self.x += dx
        if self.checar_parede(int(self.x), int(self.y + dy)):
            self.y += dy

    def draw(self):
        # pg.draw.line(self.game.screen, 'yellow', (self.x * 100, self.y * 100), (self.x * 100 + WIDTH * math.cos(self.angle), self.y * 100 + WIDTH * math.sin(self.angle)), 2) 
        pg.draw.circle(self.game.screen, 'green', (self.x * 100, self.y * 100), 15)

    def update(self):
        self.movement()
        self.mouse_control()

    @property
    def pos(self):
        return self.x, self.y
    @property
    def map_pos(self):
        return int(self.x), int(self.y)