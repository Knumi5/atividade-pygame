import pygame as pg

_ = False  # Espaço livre onde o jogador pode caminhar
# 0 será usado para marcar tarefas no mapa.

# Grade 2D do cenário: cada célula tem tamanho 1x1 no espaço lógico do jogo
mini_map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, _, _, 1, _, _, _, 1, _, _, _, _, _, _, _, 1],
    [1, _, _, 1, _, _, _, 1, _, _, _, _, _, _, _, 1],
    [1, _, _, 1, 1, _, 1, 1, _, _, 1, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, 1, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, 1, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, 1, 1, 1, 1, 1, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]


class Map:
    """Representa o mapa do jogo a partir da grade 2D (mini_map).

    Parâmetros (no construtor):
        game (Game): Instância principal do jogo, usada para acessar a tela (`screen`).
    """

    def __init__(self, game):
        """Inicializa o mapa e constrói o dicionário de paredes.

        Parâmetros:
            game (Game): Instância principal do jogo.
        """
        self.game = game
        self.mini_map = mini_map
        self.world_map = {}
        self.get_map()

    def get_map(self):
        """Converte a matriz `mini_map` no dicionário `world_map[(x, y)] = valor`.

        Parâmetros:
            Nenhum (usa apenas `self.mini_map`).
        """
        for linha_y, linha in enumerate(self.mini_map):
            for coluna_x, valor in enumerate(linha):
                if valor:
                    self.world_map[(coluna_x, linha_y)] = valor

    def draw(self):
        """Desenha a grade 2D das paredes na tela (útil para depuração em 2D).

        Parâmetros:
            Nenhum (usa `self.game.screen` e `self.world_map`).
        """
        for pos in self.world_map:
            pg.draw.rect(
                self.game.screen,
                'darkgrey',
                (pos[0] * 100, pos[1] * 100, 100, 100),
                2,
            )
