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

# Caminhos absolutos para arquivos persistentes e recursos
CAMINHO_RECORDE = str(BASE_DIR / "data" / "recorde.txt")
CAMINHO_SPRITES = str(BASE_DIR / "assets" / "imagens" / "spritesheet.bmp")
