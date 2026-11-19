import math
import pygame as pg

if __package__:
    from .settings import *
else:
    from settings import *


class Player:
    """Controla posição, movimentação, colisão e rotação da câmera do jogador."""

    def __init__(self, game):
        """Inicializa o jogador na posição e ângulo definidos em settings."""
        self.game = game
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE

    def movement(self):
        """Calcula o deslocamento com W/A/S/D relativo à direção atual do olhar."""
        seno_a = math.sin(self.angle)
        cosseno_a = math.cos(self.angle)
        dx, dy = 0, 0
        velocidade = PLAYER_SPEED * self.game.delta_time
        velocidade_seno = velocidade * seno_a
        velocidade_cosseno = velocidade * cosseno_a

        teclas = pg.key.get_pressed()
        if teclas[pg.K_w]:
            dx += velocidade_cosseno
            dy += velocidade_seno
        if teclas[pg.K_s]:
            dx -= velocidade_cosseno
            dy -= velocidade_seno
        if teclas[pg.K_a]:
            dx += velocidade_seno
            dy -= velocidade_cosseno
        if teclas[pg.K_d]:
            dx -= velocidade_seno
            dy += velocidade_cosseno

        self.checar_colisao_parede(dx, dy)

    def mouse_control(self):
        """Atualiza o ângulo de visão conforme o movimento horizontal do mouse."""
        mouse_x, _ = pg.mouse.get_pos()
        self.rel = pg.mouse.get_rel()[0]
        # Evita giros abruptos caso o sistema reporte um salto grande do cursor
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
        self.angle += self.rel * MOUSE_SENSITIVITY * self.game.delta_time
        self.angle %= math.tau  # Mantém o ângulo entre 0 e 2*pi

        # Recentraliza o cursor nas bordas para permitir rotação contínua de 360 graus
        if mouse_x < MOUSE_BORDER_LEFT or mouse_x > MOUSE_BORDER_RIGHT:
            pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
            pg.mouse.get_rel()

    def checar_parede(self, x, y):
        """Retorna True se a célula (x, y) estiver livre (sem parede)."""
        return (x, y) not in self.game.map.world_map

    def checar_colisao_parede(self, dx, dy):
        """Move nos eixos X e Y separadamente para permitir deslizar nas paredes."""
        if self.checar_parede(int(self.x + dx), int(self.y)):
            self.x += dx
        if self.checar_parede(int(self.x), int(self.y + dy)):
            self.y += dy

    def draw(self):
        """Desenha o jogador no mapa 2D (usado apenas em visualização 2D)."""
        pg.draw.circle(self.game.screen, 'green', (self.x * 100, self.y * 100), 15)

    def update(self):
        """Atualiza o movimento no teclado e a rotação da câmera pelo mouse."""
        self.movement()
        self.mouse_control()

    @property
    def pos(self):
        """Retorna a posição exata (x, y) do jogador no mapa."""
        return self.x, self.y

    @property
    def map_pos(self):
        """Retorna a célula inteira (x, y) em que o jogador se encontra."""
        return int(self.x), int(self.y)
