"""Ambiente isolado para testar os fluxos do Pygame sem abrir uma janela."""
import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

import pygame as pg
import pytest

from src import jogo, ranking


@pytest.fixture
def game(tmp_path, monkeypatch):
    monkeypatch.setattr(jogo, "CAMINHO_RECORDE", str(tmp_path / "recorde.txt"))
    monkeypatch.setattr(ranking, "ARQUIVO", str(tmp_path / "ranking.txt"))
    instancia = jogo.Game()
    instancia.nome_jogador = "Ricardo"
    instancia.iniciar_jogo("layout_1")

    # Posições reais das paredes, com chão acessível ao lado de cada terminal.
    for pos in instancia.map.tarefas_pendentes:
        instancia.map.world_map[pos] = 1
    instancia.map.tarefas_pendentes = {(0, 4), (15, 4), (5, 0)}
    instancia.map.total_tarefas = 3
    for pos in instancia.map.tarefas_pendentes:
        instancia.map.world_map[pos] = 2
    pg.event.clear()
    yield instancia
    pg.quit()


@pytest.fixture
def terminal(game):
    game.player.x, game.player.y = 1.5, 4.5
    return (0, 4)
