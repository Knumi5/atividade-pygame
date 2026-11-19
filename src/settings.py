# Configurações centrais do jogo (tela, cores e caminhos de arquivos).
import math
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# CONFIGURAÇÕES DO JOGO
RES = WIDTH, HEIGHT = 1600, 900
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
FPS = 60

PLAYER_POS = 1.5, 5 # mini_mapa
PLAYER_ANGLE = 0
PLAYER_SPEED = 0.004
PLAYER_ROT_SPEED = 0.002

MOUSE_SENSITIVITY = 0.0003
MOUSE_MAX_REL = 40
MOUSE_BORDER_LEFT = 100
MOUSE_BORDER_RIGHT = WIDTH - MOUSE_BORDER_LEFT

FOV = math.pi / 3
HALF_FOV = FOV / 2
NUM_RAYS = WIDTH // 2
HALF_NUM_RAYS = NUM_RAYS // 2
DELTA_ANGLE = FOV / NUM_RAYS
MAX_DEPTH = 20

SCREEN_DIST = HALF_WIDTH / math.tan(HALF_FOV)
SCALE = WIDTH // NUM_RAYS

CAMINHO_RECORDE = str(BASE_DIR / "data" / "recorde.txt")
CAMINHO_SPRITES = str(BASE_DIR / "assets" / "imagens" / "spritesheet.bmp")