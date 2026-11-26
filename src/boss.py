'''
Função focada na criação do boss
Desenvolvedor: Kill 
Tempo dedicado: 1 hora
Funcionalidades: 
- Locomoção 
- Spawn
- Dano 
- Temporizador
- Localizador de jogador
OBS: pass permite que eu teste funções isoladas sem precisar implementar ainda
'''

import pygame as pg
import random



# Define se o boss pode ou nao ser spawnado
def confirma_tempo(tempo, boss): 
    if  tempo >= 30 and boss == False:
        return True
    else: 
        return False

# Spawna o boss
def spawn_boss(posicao):
    """Cria os dados do chefe em uma posição (x, y) já validada pelo Game."""
    x, y = posicao
    return {"x": float(x), "y": float(y), "ativo": True}


def dano_boss():
    pass

def localizar_jogador():
    pass

def locomoção_boss():
    pass

