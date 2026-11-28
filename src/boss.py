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
'''

import math
from collections import deque

if __package__:
    from .settings import VELOCIDADE_BOSS, RAIO_BOSS, DISTANCIA_PARADA_BOSS
else:
    from settings import VELOCIDADE_BOSS, RAIO_BOSS, DISTANCIA_PARADA_BOSS



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


def dano_boss(game, quantidade=1):
    """Aplica a penalidade do encontro sem reiniciar a rodada."""
    game.perder_chance(quantidade, reiniciar_rodada=False)

def localizar_jogador(player):
    """Retorna a posição atual do jogador em células do mapa."""
    return player.pos


def encontrar_caminho(inicio, destino, world_map, grade):
    """BFS cardinal: caminho mínimo por chão livre, incluindo início e destino."""
    def livre(celula):
        x, y = celula
        return (0 <= y < len(grade) and 0 <= x < len(grade[y])
                and celula not in world_map)

    if not livre(inicio) or not livre(destino):
        return []
    fila = deque([inicio])
    anteriores = {inicio: None}
    while fila:
        atual = fila.popleft()
        if atual == destino:
            caminho = []
            while atual is not None:
                caminho.append(atual)
                atual = anteriores[atual]
            return caminho[::-1]
        x, y = atual
        for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
            proxima = (x + dx, y + dy)
            if livre(proxima) and proxima not in anteriores:
                anteriores[proxima] = atual
                fila.append(proxima)
    return []


def linha_livre(origem, destino, world_map):
    """Verifica visibilidade com amostras curtas, inclusive nas extremidades."""
    dx, dy = destino[0] - origem[0], destino[1] - origem[1]
    passos = max(1, math.ceil(math.hypot(dx, dy) / 0.025))
    return all(
        (math.floor(origem[0] + dx * i / passos),
         math.floor(origem[1] + dy * i / passos)) not in world_map
        for i in range(passos + 1)
    )


def mover_boss(boss, posicao_jogador, world_map, grade, segundos):
    """Segue centros de células com colisão e subpassos; nunca anda em diagonal.

    A rota fica no próprio encontro e é refeita quando o jogador muda de célula.
    Sem caminho, o chefe aguarda. O Game descarta a rota ao trocar de mapa.
    """
    if not boss or not boss.get("ativo") or segundos <= 0:
        return False
    origem = (boss["x"], boss["y"])
    if (math.dist(origem, posicao_jogador) <= DISTANCIA_PARADA_BOSS
            and linha_livre(origem, posicao_jogador, world_map)):
        return False
    alvo = tuple(math.floor(v) for v in posicao_jogador)
    if boss.get("_alvo") != alvo or not boss.get("_rota"):
        inicio = tuple(math.floor(v) for v in origem)
        caminho = encontrar_caminho(inicio, alvo, world_map, grade)
        boss["_rota"] = [(x + 0.5, y + 0.5) for x, y in caminho]
        boss["_alvo"] = alvo

    orcamento = VELOCIDADE_BOSS * segundos
    while orcamento > 1e-9 and boss["_rota"]:
        x, y = boss["x"], boss["y"]
        tx, ty = boss["_rota"][0]
        distancia = math.hypot(tx - x, ty - y)
        if distancia <= 1e-8:
            boss["_rota"].pop(0)
            continue
        passo = min(orcamento, distancia, 0.05)
        nx, ny = x + (tx - x) / distancia * passo, y + (ty - y) / distancia * passo
        livre = all(
            0 <= math.floor(ny + dy) < len(grade)
            and 0 <= math.floor(nx + dx) < len(grade[math.floor(ny + dy)])
            and (math.floor(nx + dx), math.floor(ny + dy)) not in world_map
            for dx in (-RAIO_BOSS, RAIO_BOSS) for dy in (-RAIO_BOSS, RAIO_BOSS)
        )
        if not livre:
            boss.pop("_rota", None)
            break
        boss["x"], boss["y"] = nx, ny
        orcamento -= passo
        if (math.dist((nx, ny), posicao_jogador) <= DISTANCIA_PARADA_BOSS
                and linha_livre((nx, ny), posicao_jogador, world_map)):
            break
    return origem != (boss["x"], boss["y"])


def locomoção_boss(boss, player, mapa, segundos):
    """Interface do módulo para o Game; velocidades usam segundos, não frames."""
    return mover_boss(boss, localizar_jogador(player), mapa.world_map, mapa.mini_map, segundos)

