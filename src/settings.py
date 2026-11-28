# Configurações centrais do jogo (tela, jogador, mouse, raycasting e caminhos).
import math
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Configurações da janela e taxa de quadros
RES = WIDTH, HEIGHT = 1600, 900
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
FPS = 60

# Configurações iniciais e velocidade do jogador
PLAYER_POS = 1.5, 5  # Posição inicial (x, y) em células do mini_map
PLAYER_ANGLE = 0     # Ângulo inicial em radianos
PLAYER_SPEED = 0.004
PLAYER_ROT_SPEED = 0.002

# Regras das rodadas infinitas (pontuação / leaderboard)
CHANCES_INICIAIS = 5
TAREFAS_POR_RODADA = 3       # Configurável entre 1 e 7 tarefas por rodada
TEMPO_INICIAL_RODADA = 45.0  # Tempo (em segundos) da 1ª rodada
REDUCAO_TEMPO_RODADA = 3.0   # Segundos reduzidos a cada rodada vencida
TEMPO_MINIMO_RODADA = 15.0   # Limite mínimo de tempo por rodada

# Regras do cumprimento do chefe, confirmadas para Q05/Q06.
TECLA_CUMPRIMENTO_BOSS = ord("f")
ALCANCE_CUMPRIMENTO_BOSS = 1.8
PRAZO_CUMPRIMENTO_BOSS = 5.0
PENALIDADE_BOSS = 1
VELOCIDADE_BOSS = 1.4        # Células por segundo
RAIO_BOSS = 0.18
DISTANCIA_PARADA_BOSS = 0.85
VOLUME_INICIAL = 0.25
DURACAO_JUMPSCARE = 1.2

# Configurações de controle da câmera pelo mouse
MOUSE_SENSITIVITY = 0.0003
MOUSE_MAX_REL = 40   # Limita saltos bruscos do cursor por frame
MOUSE_BORDER_LEFT = 100
MOUSE_BORDER_RIGHT = WIDTH - MOUSE_BORDER_LEFT

# Configurações do raycasting e projeção 3D
FOV = math.pi / 3                  # Campo de visão (60 graus)
HALF_FOV = FOV / 2
NUM_RAYS = WIDTH // 2              # Quantidade de raios lançados por frame
HALF_NUM_RAYS = NUM_RAYS // 2
DELTA_ANGLE = FOV / NUM_RAYS       # Diferença angular entre raios vizinhos
MAX_DEPTH = 20                     # Alcance máximo de cada raio (em células)
SCREEN_DIST = HALF_WIDTH / math.tan(HALF_FOV)  # Distância até o plano de projeção
SCALE = WIDTH // NUM_RAYS          # Largura em pixels de cada coluna 3D

# Cores do cenário 3D (estilo escritório)
COR_TETO = (38, 42, 48)
COR_CHAO = (50, 56, 66)
COR_PAREDE_ESCRITORIO = (175, 162, 138)  # Bege corporativo
COR_TAREFA_PENDENTE = (0, 200, 255)      # Terminal azul/ciano
COR_TAREFA_CONCLUIDA = (0, 220, 100)     # Terminal verde
COR_TAREFA_ERRADA = (190, 65, 60)        # Terminal resolvido com erro

# Caminhos absolutos para arquivos persistentes e recursos
CAMINHO_RECORDE = str(BASE_DIR / "data" / "recorde.txt")
CAMINHO_SPRITES = str(BASE_DIR / "assets" / "imagens" / "spritesheet.bmp")
CAMINHO_TEXTURAS = BASE_DIR / "assets" / "imagens" / "texturas"
CAMINHO_BOSS = BASE_DIR / "assets" / "imagens" / "chefe.png"
CAMINHO_TRILHA = BASE_DIR / "assets" / "sons" / "escritorio_loop.wav"
CAMINHO_SUSTO = BASE_DIR / "assets" / "sons" / "chefe_susto.wav"

# Dimensões padrão das texturas de parede (em pixels)
TEXTURE_SIZE = 256
HALF_TEXTURE_SIZE = TEXTURE_SIZE // 2
