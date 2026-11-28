import math
import pygame as pg

if __package__:
    from .settings import *
else:
    from settings import *


# Mapeia cada número do mapa para o nome do arquivo esperado em assets/imagens/texturas/
ARQUIVOS_TEXTURAS = {
    1: "1.png",  # Parede comum do escritório
    2: "2.png",  # Terminal/computador com tarefa pendente
    3: "3.png",  # Terminal/computador com tarefa concluída
    4: "4.png",  # Terminal resolvido com erro
}


class ObjectRenderer:
    """Carrega as texturas das paredes e renderiza as fatias 3D do cenário.

    Quando os arquivos de imagem ainda não existem na pasta `assets/imagens/texturas/`,
    gera texturas padrão equivalentes para o jogo continuar funcionando sem erro.

    Parâmetros (no construtor):
        game (Game): Instância principal do jogo, usada para acessar `screen` e `raycasting`.
    """

    def __init__(self, game):
        """Inicializa o renderizador e carrega (ou cria) as texturas das paredes.

        Parâmetros:
            game (Game): Instância principal do jogo.
        """
        self.game = game
        self.screen = game.screen
        self.texturas_parede = self.carregar_texturas_parede()
        self.origem_sprite_boss = CAMINHO_BOSS if CAMINHO_BOSS.is_file() else None
        if self.origem_sprite_boss:
            self.sprite_boss = pg.image.load(str(CAMINHO_BOSS)).convert_alpha()
        else:
            self.sprite_boss = pg.Surface((64, 112), pg.SRCALPHA)
            pg.draw.rect(self.sprite_boss, (35, 40, 50), (10, 40, 44, 70))
            pg.draw.ellipse(self.sprite_boss, (205, 183, 158), (16, 4, 32, 42))
            pg.draw.polygon(self.sprite_boss, (170, 45, 50), [(28, 44), (36, 44), (32, 76)])
        self._projecao_boss = None
        self._tamanho_boss = None

    def carregar_texturas_parede(self):
        """Carrega as texturas de `CAMINHO_TEXTURAS` ou usa texturas padrão de escritório.

        Parâmetros:
            Nenhum.

        Retorno:
            dict[int, pygame.Surface]: Dicionário `{tipo_bloco: superficie_256x256}`.
        """
        texturas = {}
        for tipo_bloco, nome_arquivo in ARQUIVOS_TEXTURAS.items():
            caminho = self._encontrar_arquivo_textura(nome_arquivo)
            if caminho is not None:
                imagem = pg.image.load(str(caminho)).convert_alpha()
                texturas[tipo_bloco] = pg.transform.scale(imagem, (TEXTURE_SIZE, TEXTURE_SIZE))
            else:
                texturas[tipo_bloco] = self._criar_textura_padrao(tipo_bloco)
        return texturas

    def _encontrar_arquivo_textura(self, nome_arquivo):
        """Procura a imagem pelo nome padrão ou com extensões alternativas (.png, .jpg, .bmp).

        Parâmetros:
            nome_arquivo (str): Nome base configurado em `ARQUIVOS_TEXTURAS`.

        Retorno:
            Path | None: Caminho do arquivo encontrado, ou `None` se não existir.
        """
        caminho_exato = CAMINHO_TEXTURAS / nome_arquivo
        if caminho_exato.exists():
            return caminho_exato

        raiz_nome = caminho_exato.stem
        for extensao in (".png", ".jpg", ".jpeg", ".bmp"):
            candidato = CAMINHO_TEXTURAS / f"{raiz_nome}{extensao}"
            if candidato.exists():
                return candidato
        return None

    def _criar_textura_padrao(self, tipo_bloco):
        """Gera uma textura procedural 256x256 temporária enquanto não há imagens em disco.

        Parâmetros:
            tipo_bloco (int): Código do bloco no mapa (`1` parede, `2` tarefa, `3` concluída).

        Retorno:
            pygame.Surface: Superfície pronta no tamanho `(TEXTURE_SIZE, TEXTURE_SIZE)`.
        """
        superficie = pg.Surface((TEXTURE_SIZE, TEXTURE_SIZE))
        superficie.fill(COR_PAREDE_ESCRITORIO)

        # Rodapé e friso horizontal para dar aspecto de divisória de escritório
        pg.draw.rect(superficie, (110, 100, 85), (0, TEXTURE_SIZE - 28, TEXTURE_SIZE, 28))
        pg.draw.line(superficie, (145, 134, 114), (0, 32), (TEXTURE_SIZE, 32), 3)
        pg.draw.rect(superficie, (140, 128, 108), (0, 0, TEXTURE_SIZE, TEXTURE_SIZE), 4)

        if tipo_bloco in (2, 3, 4):
            # Desenha uma tela de terminal/computador no centro da parede
            cor_tela = {2: COR_TAREFA_PENDENTE, 3: COR_TAREFA_CONCLUIDA,
                        4: COR_TAREFA_ERRADA}[tipo_bloco]
            pg.draw.rect(superficie, (35, 38, 44), (44, 58, 168, 118))
            pg.draw.rect(superficie, cor_tela, (56, 70, 144, 94))
            pg.draw.rect(superficie, (45, 48, 56), (108, 176, 40, 22))
            pg.draw.rect(superficie, (60, 64, 72), (82, 198, 92, 10))

        return superficie

    def desenhar_fundo(self):
        """Desenha o teto e o piso do escritório ao fundo da cena 3D.

        Parâmetros:
            Nenhum.
        """
        self.screen.fill(COR_TETO, (0, 0, WIDTH, HALF_HEIGHT))
        self.screen.fill(COR_CHAO, (0, HALF_HEIGHT, WIDTH, HALF_HEIGHT))

    def desenhar_paredes(self):
        """Recorta e renderiza as fatias texturizadas de acordo com os raios calculados.

        Parâmetros:
            Nenhum (lê `self.game.raycasting.ray_casting_result`).
        """
        for raio, profundidade, altura_projetada, bloco_tipo, offset, fator_face in (
            self.game.raycasting.ray_casting_result
        ):
            textura = self.texturas_parede.get(bloco_tipo, self.texturas_parede[1])
            x_textura = min(TEXTURE_SIZE - SCALE, max(0, int(offset * (TEXTURE_SIZE - SCALE))))
            altura_coluna = max(1, int(altura_projetada))

            if altura_coluna <= HEIGHT:
                coluna = textura.subsurface(x_textura, 0, SCALE, TEXTURE_SIZE)
                coluna = pg.transform.scale(coluna, (SCALE, altura_coluna))
                pos_y = HALF_HEIGHT - altura_coluna // 2
            else:
                # Quando muito perto da parede, recorta só a faixa visível para manter o FPS
                altura_visivel = max(1, int(TEXTURE_SIZE * HEIGHT / altura_coluna))
                y_textura = max(0, min(TEXTURE_SIZE - altura_visivel, HALF_TEXTURE_SIZE - altura_visivel // 2))
                coluna = textura.subsurface(x_textura, y_textura, SCALE, altura_visivel)
                coluna = pg.transform.scale(coluna, (SCALE, HEIGHT))
                pos_y = 0

            # Aplica sombreamento por distância e diferença entre faces verticais/horizontais
            sombra = max(25, min(255, int((255 / (1 + max(profundidade, 0) ** 5 * 0.00002)) * fator_face)))
            if sombra < 255:
                coluna.fill((sombra, sombra, sombra), special_flags=pg.BLEND_RGB_MULT)

            self.screen.blit(coluna, (raio * SCALE, pos_y))

    def desenhar_boss(self):
        """Projeta o sprite e testa profundidade por coluna contra as paredes.

        O ângulo usa a mesma distribuição dos raios do cenário. Nenhum recurso
        é lido do disco nesta etapa; só a projeção muda quando o tamanho muda.
        Retorna quantas colunas passaram no teste de profundidade.
        """
        boss = getattr(self.game, "boss", None)
        if not boss or not boss.get("ativo"):
            return 0
        player = self.game.player
        dx, dy = boss["x"] - player.x, boss["y"] - player.y
        frente = math.cos(player.angle) * dx + math.sin(player.angle) * dy
        lado = -math.sin(player.angle) * dx + math.cos(player.angle) * dy
        if frente <= 0.05:
            return 0
        angulo = math.atan2(lado, frente)
        altura = max(1, min(HEIGHT * 3, round(SCREEN_DIST * 0.95 / frente)))
        largura = max(1, round(altura * self.sprite_boss.get_width() / self.sprite_boss.get_height()))
        centro = round((angulo + HALF_FOV) / DELTA_ANGLE * SCALE)
        esquerda = centro - largura // 2
        topo = round(HALF_HEIGHT + SCREEN_DIST * 0.5 / frente) - altura
        if esquerda >= WIDTH or esquerda + largura <= 0:
            return 0
        tamanho = largura, altura
        if tamanho != self._tamanho_boss:
            self._projecao_boss = pg.transform.scale(self.sprite_boss, tamanho)
            self._tamanho_boss = tamanho
        colunas = 0
        for raio, profundidade, *_resto in self.game.raycasting.ray_casting_result:
            x = raio * SCALE
            if esquerda <= x < esquerda + largura and frente < profundidade:
                origem_x = x - esquerda
                faixa = min(SCALE, largura - origem_x)
                self.screen.blit(self._projecao_boss, (x, topo), (origem_x, 0, faixa, altura))
                colunas += 1
        return colunas

    def desenhar_susto(self, progresso):
        """Sobreposição com zoom contínuo, sem pausa bloqueante ou flashes."""
        self.screen.fill((48, 7, 17))
        largura, altura = self.sprite_boss.get_size()
        rosto = self.sprite_boss.subsurface((largura // 4, altura // 32, largura // 2, altura // 3))
        lado = round(HEIGHT * (0.85 + min(1.0, max(0.0, progresso)) * .45))
        imagem = pg.transform.scale(rosto, (lado, lado))
        self.screen.blit(imagem, imagem.get_rect(center=(HALF_WIDTH, HALF_HEIGHT)))

    def draw(self):
        """Renderiza o cenário 3D completo (fundo + paredes texturizadas).

        Parâmetros:
            Nenhum.
        """
        self.desenhar_fundo()
        self.desenhar_paredes()
        self.desenhar_boss()
