import math
import pygame as pg

if __package__:
    from .settings import *
else:
    from settings import *


class RayCasting:
    """Calcula a distância até as paredes via raycasting (DDA) e projeta o cenário em 3D.

    Parâmetros (no construtor):
        game (Game): Instância principal do jogo, usada para acessar `player`, `map` e `screen`.
    """

    def __init__(self, game):
        """Inicializa o sistema de raycasting ligado à instância principal do jogo.

        Parâmetros:
            game (Game): Instância principal do jogo.
        """
        self.game = game
        self.ray_casting_result = []

    def ray_cast(self):
        """Lança `NUM_RAYS` raios no campo de visão e calcula a altura projetada de cada coluna.

        Parâmetros:
            Nenhum (lê posição/ângulo de `self.game.player` e paredes de `self.game.map`).
        """
        self.ray_casting_result = []
        textura_vertical, textura_horizontal = 1, 1
        origem_x, origem_y = self.game.player.pos
        celula_x, celula_y = self.game.player.map_pos

        # Pequeno deslocamento inicial evita divisão exata por zero em ângulos retos
        angulo_raio = self.game.player.angle - HALF_FOV + 0.0001
        for raio in range(NUM_RAYS):
            seno_a = math.sin(angulo_raio)
            cosseno_a = math.cos(angulo_raio)

            # Interseções com linhas horizontais da grade
            y_hor, passo_y = (celula_y + 1, 1) if seno_a > 0 else (celula_y - 1e-6, -1)
            profundidade_horizontal = (y_hor - origem_y) / seno_a
            x_hor = origem_x + profundidade_horizontal * cosseno_a

            passo_profundidade = passo_y / seno_a
            passo_x = passo_profundidade * cosseno_a

            for _ in range(MAX_DEPTH):
                bloco_horizontal = int(x_hor), int(y_hor)
                if bloco_horizontal in self.game.map.world_map:
                    textura_horizontal = self.game.map.world_map[bloco_horizontal]
                    break
                x_hor += passo_x
                y_hor += passo_y
                profundidade_horizontal += passo_profundidade

            # Interseções com linhas verticais da grade
            x_vert, passo_x = (celula_x + 1, 1) if cosseno_a > 0 else (celula_x - 1e-6, -1)
            profundidade_vertical = (x_vert - origem_x) / cosseno_a
            y_vert = origem_y + profundidade_vertical * seno_a

            passo_profundidade = passo_x / cosseno_a
            passo_y = passo_profundidade * seno_a

            for _ in range(MAX_DEPTH):
                bloco_vertical = int(x_vert), int(y_vert)
                if bloco_vertical in self.game.map.world_map:
                    textura_vertical = self.game.map.world_map[bloco_vertical]
                    break
                x_vert += passo_x
                y_vert += passo_y
                profundidade_vertical += passo_profundidade

            # Escolhe a interseção mais próxima do jogador, o tipo do bloco, o offset e a face
            if profundidade_vertical < profundidade_horizontal:
                profundidade = profundidade_vertical
                bloco_tipo = textura_vertical
                fator_face = 1.0
                y_vert %= 1
                offset = y_vert if cosseno_a > 0 else (1 - y_vert)
            else:
                profundidade = profundidade_horizontal
                bloco_tipo = textura_horizontal
                fator_face = 0.85  # Escurece levemente faces horizontais para destacar quinas
                x_hor %= 1
                offset = (1 - x_hor) if seno_a > 0 else x_hor

            # Garante offset dentro de [0, 1) para recortar a textura sem estourar bordas
            offset = max(0.0, min(0.9999, offset))

            # Corrige o efeito olho de peixe (distorção nas bordas do FOV)
            profundidade *= math.cos(self.game.player.angle - angulo_raio)

            # Converte a distância da parede em altura em pixels na tela
            altura_projetada = SCREEN_DIST / (profundidade + 0.0001)
            self.ray_casting_result.append(
                (raio, profundidade, altura_projetada, bloco_tipo, offset, fator_face)
            )

            angulo_raio += DELTA_ANGLE

    def draw(self):
        """Desenha as colunas 3D em cor sólida (fallback caso ObjectRenderer não seja usado).

        Parâmetros:
            Nenhum (usa os resultados salvos em `self.ray_casting_result` e `self.game.screen`).
        """
        for raio, profundidade, altura_projetada, bloco_tipo, _offset, fator_face in self.ray_casting_result:
            # Quanto maior a distância, mais escura fica a parede
            sombra = (1 / (1 + max(profundidade, 0) ** 5 * 0.00002)) * fator_face
            if bloco_tipo == 2:
                cor_base = COR_TAREFA_PENDENTE
            elif bloco_tipo == 3:
                cor_base = COR_TAREFA_CONCLUIDA
            elif bloco_tipo == 4:
                cor_base = COR_TAREFA_ERRADA
            else:
                cor_base = COR_PAREDE_ESCRITORIO

            cor = (
                int(cor_base[0] * sombra),
                int(cor_base[1] * sombra),
                int(cor_base[2] * sombra),
            )

            pg.draw.rect(
                self.game.screen,
                cor,
                (raio * SCALE, HALF_HEIGHT - altura_projetada // 2, SCALE, altura_projetada),
            )

    def update(self):
        """Recalcula todos os raios para o frame atual.

        Parâmetros:
            Nenhum.
        """
        self.ray_cast()
