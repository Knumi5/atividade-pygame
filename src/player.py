import math
import pygame as pg

if __package__:
    from .settings import *
else:
    from settings import *


class Player:
    """Controla posição, movimentação, colisão e rotação da câmera do jogador.

    Parâmetros (no construtor):
        game (Game): Instância principal do jogo, usada para acessar `delta_time`,
            `map` (colisões) e `screen`.
    """

    def __init__(self, game):
        """Inicializa o jogador na posição e ângulo definidos em settings.

        Parâmetros:
            game (Game): Instância principal do jogo.
        """
        self.game = game
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE

    def movement(self):
        """Calcula o deslocamento com W/A/S/D relativo à direção atual do olhar.

        Parâmetros:
            Nenhum (lê o estado do teclado via Pygame e usa `self.game.delta_time`).
        """
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
        """Atualiza o ângulo de visão conforme o movimento horizontal do mouse.

        Parâmetros:
            Nenhum (lê posição e deslocamento do cursor via `pg.mouse`).
        """
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
        """Verifica se uma célula do mapa está livre para o jogador passar.

        Parâmetros:
            x (int): Coordenada inteira da coluna no mapa.
            y (int): Coordenada inteira da linha no mapa.

        Retorno:
            bool: True se a célula `(x, y)` estiver livre; False se houver parede.
        """
        return (x, y) not in self.game.map.world_map

    def checar_colisao_parede(self, dx, dy):
        """Aplica o movimento nos eixos X e Y separadamente para deslizar nas paredes.

        Parâmetros:
            dx (float): Deslocamento desejado no eixo X (em células do mapa).
            dy (float): Deslocamento desejado no eixo Y (em células do mapa).
        """
        if self.checar_parede(int(self.x + dx), int(self.y)):
            self.x += dx
        if self.checar_parede(int(self.x), int(self.y + dy)):
            self.y += dy

    def draw(self):
        """Desenha o jogador no mapa 2D (usado apenas em visualização 2D).

        Parâmetros:
            Nenhum (desenha diretamente em `self.game.screen`).
        """
        pg.draw.circle(self.game.screen, 'green', (self.x * 100, self.y * 100), 15)

    def update(self):
        """Atualiza o movimento pelo teclado e a rotação da câmera pelo mouse.

        Parâmetros:
            Nenhum.
        """
        self.movement()
        self.mouse_control()

    @property
    def pos(self):
        """Retorna a posição exata do jogador no mapa.

        Parâmetros:
            Nenhum (propriedade somente leitura).

        Retorno:
            tuple[float, float]: Coordenadas `(x, y)` em células do mapa.
        """
        return self.x, self.y

    @property
    def map_pos(self):
        """Retorna a célula inteira em que o jogador se encontra.

        Parâmetros:
            Nenhum (propriedade somente leitura).

        Retorno:
            tuple[int, int]: Índices inteiros `(x, y)` da célula atual.
        """
        return int(self.x), int(self.y)
