import random
import pygame as pg

if __package__:
    from .settings import TAREFAS_POR_RODADA
else:
    from settings import TAREFAS_POR_RODADA

_ = False  # Espaço livre onde o jogador pode caminhar
T = 2      # Parede com terminal/tarefa pendente (3 = tarefa concluída)

# 5 variações de layout para o mesmo cenário 16x9 (mudam apenas as paredes internas).
# Os terminais de tarefa (T = 2) são posicionados dinamicamente nas paredes externas.
MAPAS = {
    "layout_1": {
        "nome_exibicao": "Layout 1 - Escritório Original",
        "pos_inicial": (1.5, 5.0),
        "grade": [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, _, _, 1, _, _, _, 1, _, _, _, _, _, _, _, 1],
            [1, _, _, 1, _, _, _, 1, _, _, _, _, _, _, _, 1],
            [1, _, _, 1, 1, _, 1, 1, _, _, 1, _, _, _, _, 1],
            [1, _, _, _, _, _, _, _, _, _, 1, _, _, _, _, 1],
            [1, _, _, _, _, _, _, _, _, _, 1, _, _, _, _, 1],
            [1, _, _, _, _, _, _, _, _, _, 1, 1, 1, 1, 1, 1],
            [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ],
    },
    "layout_2": {
        "nome_exibicao": "Layout 2 - Baias Centrais",
        "pos_inicial": (1.5, 5.0),
        "grade": [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, _, _, _, _, _, 1, _, _, 1, _, _, _, _, _, 1],
            [1, _, 1, 1, _, _, _, _, _, _, _, _, 1, 1, _, 1],
            [1, _, 1, _, _, 1, 1, _, _, 1, 1, _, _, 1, _, 1],
            [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
            [1, _, _, _, _, 1, 1, _, _, 1, 1, _, _, _, _, 1],
            [1, _, 1, _, _, _, _, _, _, _, _, _, _, 1, _, 1],
            [1, _, 1, 1, _, _, _, 1, 1, _, _, _, 1, 1, _, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ],
    },
    "layout_3": {
        "nome_exibicao": "Layout 3 - Salas Interligadas",
        "pos_inicial": (1.5, 5.0),
        "grade": [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, _, _, _, 1, _, _, _, _, 1, _, _, _, _, _, 1],
            [1, _, 1, _, 1, _, 1, 1, _, 1, _, 1, 1, 1, _, 1],
            [1, _, 1, _, _, _, 1, _, _, _, _, 1, _, _, _, 1],
            [1, _, 1, 1, 1, _, 1, _, 1, 1, _, 1, _, 1, _, 1],
            [1, _, _, _, _, _, _, _, 1, _, _, _, _, 1, _, 1],
            [1, 1, 1, _, 1, 1, 1, _, 1, _, 1, 1, _, 1, _, 1],
            [1, _, _, _, _, _, _, _, _, _, 1, _, _, _, _, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ],
    },
    "layout_4": {
        "nome_exibicao": "Layout 4 - Corredores em Zigue-Zague",
        "pos_inicial": (1.5, 5.0),
        "grade": [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, _, _, _, 1, _, _, _, 1, _, _, _, 1, _, _, 1],
            [1, _, 1, _, 1, _, 1, _, 1, _, 1, _, 1, _, _, 1],
            [1, _, 1, _, _, _, 1, _, _, _, 1, _, _, _, 1, 1],
            [1, _, 1, 1, 1, _, 1, 1, 1, _, 1, 1, _, _, _, 1],
            [1, _, _, _, 1, _, _, _, 1, _, _, _, _, 1, _, 1],
            [1, _, 1, _, 1, 1, _, _, 1, 1, 1, _, 1, 1, _, 1],
            [1, _, 1, _, _, _, _, 1, _, _, _, _, _, _, _, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ],
    },
    "layout_5": {
        "nome_exibicao": "Layout 5 - Sala Central",
        "pos_inicial": (1.5, 5.0),
        "grade": [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, _, _, _, _, _, 1, _, _, 1, _, _, _, _, _, 1],
            [1, _, 1, 1, 1, _, 1, _, _, 1, _, 1, 1, 1, _, 1],
            [1, _, 1, _, _, _, _, _, _, _, _, _, _, 1, _, 1],
            [1, _, _, _, 1, 1, 1, _, _, 1, 1, 1, _, _, _, 1],
            [1, _, 1, _, 1, _, _, _, _, _, _, 1, _, 1, _, 1],
            [1, _, 1, _, _, _, 1, 1, 1, 1, _, _, _, 1, _, 1],
            [1, _, _, _, 1, _, _, _, _, _, _, 1, _, _, _, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ],
    },
}

ORDEM_MAPAS = list(MAPAS.keys())
mini_map = MAPAS["layout_1"]["grade"]  # Mantido para compatibilidade


def listar_mapas():
    """Retorna a lista de chaves dos layouts disponíveis para o cenário.

    Parâmetros:
        Nenhum.

    Retorno:
        list[str]: Identificadores dos layouts cadastrados em `MAPAS`.
    """
    return list(ORDEM_MAPAS)


class Map:
    """Gerencia o layout ativo do cenário 16x9 e sorteia os terminais de tarefa nas bordas.

    Parâmetros (no construtor):
        game (Game): Instância principal do jogo, usada para acessar a tela (`screen`).
        nome_mapa (str, opcional): Chave de `MAPAS` ou `"aleatorio"` para sortear um layout
            sem repetir o anterior (padrão: `"aleatorio"`).
        qtd_tarefas (int, opcional): Quantidade de tarefas (1 a 7) a posicionar nas paredes
            externas (padrão: `TAREFAS_POR_RODADA`).
    """

    def __init__(self, game, nome_mapa="aleatorio", qtd_tarefas=TAREFAS_POR_RODADA):
        """Inicializa o layout selecionado e posiciona os terminais de tarefa.

        Parâmetros:
            game (Game): Instância principal do jogo.
            nome_mapa (str, opcional): Nome do layout em `MAPAS` ou `"aleatorio"`.
            qtd_tarefas (int, opcional): Quantidade de tarefas para esta rodada.
        """
        self.game = game
        self.nome_mapa = ""
        self.nome_exibicao = ""
        self.pos_inicial = (1.5, 5.0)
        self.mini_map = []
        self.world_map = {}
        self.tarefas_pendentes = set()
        self.tarefas_concluidas = set()
        self.tarefas_erradas = set()
        self.total_tarefas = 0
        self.carregar_mapa(nome_mapa, qtd_tarefas=qtd_tarefas)

    def carregar_mapa(self, nome_mapa="aleatorio", qtd_tarefas=TAREFAS_POR_RODADA):
        """Carrega um layout de `MAPAS` e sorteia `qtd_tarefas` terminais nas bordas externas.

        Parâmetros:
            nome_mapa (str, opcional): Chave do layout em `MAPAS` ou `"aleatorio"`.
            qtd_tarefas (int, opcional): Quantidade de tarefas (entre 1 e 7) na rodada.

        Levanta:
            ValueError: Se `nome_mapa` não existir em `MAPAS`.
        """
        if nome_mapa == "aleatorio":
            opcoes = [m for m in ORDEM_MAPAS if m != self.nome_mapa] or ORDEM_MAPAS
            nome_mapa = random.choice(opcoes)
        if nome_mapa not in MAPAS:
            raise ValueError(f"Mapa desconhecido: '{nome_mapa}'. Opções: {ORDEM_MAPAS}")

        dados_mapa = MAPAS[nome_mapa]
        self.nome_mapa = nome_mapa
        self.nome_exibicao = dados_mapa["nome_exibicao"]
        self.pos_inicial = dados_mapa["pos_inicial"]
        self.mini_map = dados_mapa["grade"]
        self.world_map = {}
        self.tarefas_pendentes = set()
        self.tarefas_concluidas = set()
        self.tarefas_erradas = set()
        self.get_map()
        self.sortear_tarefas(qtd_tarefas)

    def get_map(self):
        """Converte a matriz `mini_map` no dicionário `world_map[(x, y)] = valor`.

        Parâmetros:
            Nenhum (usa apenas `self.mini_map`).
        """
        for linha_y, linha in enumerate(self.mini_map):
            for coluna_x, valor in enumerate(linha):
                if valor:
                    self.world_map[(coluna_x, linha_y)] = valor

    def sortear_tarefas(self, qtd_tarefas):
        """Escolhe posições nas paredes externas (adjacentes a chão livre) para virar `T = 2`.

        Parâmetros:
            qtd_tarefas (int): Número desejado de terminais de tarefa para a rodada.
        """
        altura = len(self.mini_map)
        largura = len(self.mini_map[0])
        candidatas = []

        # Percorre apenas as bordas externas (excluindo os 4 cantos) com acesso direto por dentro
        for x in range(1, largura - 1):
            if not self.mini_map[1][x]:
                candidatas.append((x, 0))
            if not self.mini_map[altura - 2][x]:
                candidatas.append((x, altura - 1))

        for y in range(1, altura - 1):
            if not self.mini_map[y][1]:
                candidatas.append((0, y))
            if not self.mini_map[y][largura - 2]:
                candidatas.append((largura - 1, y))

        quantidade = max(1, min(qtd_tarefas, len(candidatas)))
        for pos in random.sample(candidatas, quantidade):
            self.world_map[pos] = T
            self.tarefas_pendentes.add(pos)

        self.total_tarefas = len(self.tarefas_pendentes)

    def concluir_tarefa(self, pos):
        """Marca um terminal de tarefa como concluído (`3`) e o remove das pendentes.

        Parâmetros:
            pos (tuple[int, int]): Coordenada `(x, y)` do bloco de tarefa no mapa.

        Retorno:
            bool: True se a tarefa estava pendente e foi concluída; False caso contrário.
        """
        return self.resolver_tarefa(pos, acertou=True)

    def resolver_tarefa(self, pos, acertou):
        """Resolve uma tarefa uma única vez, distinguindo acerto de erro.

        O total inicial da rodada é preservado. A HUD pode contar resoluções
        e acertos separadamente, sem apresentar um erro como tarefa acertada.
        """
        if pos not in self.tarefas_pendentes:
            return False
        self.tarefas_pendentes.remove(pos)
        if acertou:
            self.tarefas_concluidas.add(pos)
            self.world_map[pos] = 3
        else:
            self.tarefas_erradas.add(pos)
            self.world_map[pos] = 4
        return True

    def draw(self):
        """Desenha a grade 2D das paredes e tarefas na tela (útil para depuração em 2D).

        Parâmetros:
            Nenhum (usa `self.game.screen` e `self.world_map`).
        """
        for pos, valor in self.world_map.items():
            cores = {T: 'cyan', 3: 'green', 4: 'red'}
            cor = cores.get(valor, 'darkgrey')
            pg.draw.rect(
                self.game.screen,
                cor,
                (pos[0] * 100, pos[1] * 100, 100, 100),
                2,
            )
