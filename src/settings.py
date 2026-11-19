# Configurações centrais do jogo (tela, cores e caminhos de arquivos).
import math
# CONFIGURAÇÕES DO JOGO
RES = WIDTH, HEIGHT = 1600, 900
FPS = 60

PLAYER_POS = 1.5, 5 # mini_mapa
PLAYER_ANGLE = 0
PLAYER_SPEED = 0.004
PLAYER_ROT_SPEED = 0.002

FOV = math.pi / 3
HALF_FOV = FOV / 2
NUM_RAYS = WIDTH // 2
HALF_NUM_RAYS = NUM_RAYS // 2
DELTA_ANGLE = FOV / NUM_RAYS
MAX_DEPTH = 20

CAMINHO_RECORDE = "data/recorde.txt"
CAMINHO_SPRITES = "assets/imagens/spritesheet.bmp"