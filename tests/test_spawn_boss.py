"""Critérios do Q03: posição válida, criação única e integração com o Game."""
import os
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

import pygame as pg
import pytest

from src import jogo
from src.boss import spawn_boss
from src.map import MAPAS


@pytest.fixture
def game(tmp_path, monkeypatch):
    monkeypatch.setattr(jogo, "CAMINHO_RECORDE", str(tmp_path / "recorde.txt"))
    instancia = jogo.Game()
    instancia.nome_jogador = "Teste Q03"
    instancia.iniciar_jogo("layout_1")
    yield instancia
    pg.quit()


def preparar_grade(game, livres, jogador=(1, 1), largura=3, altura=3):
    livres = set(livres) | {jogador}
    grade = [[int((x, y) not in livres) for x in range(largura)]
             for y in range(altura)]
    paredes = {(x, y): 1 for y in range(altura) for x in range(largura)
               if (x, y) not in livres}
    game.map = SimpleNamespace(mini_map=grade, world_map=paredes)
    game.player = SimpleNamespace(map_pos=jogador)


@pytest.mark.parametrize("posicao", [(1, 2), (2.5, 4.5)])
def test_factory_recebe_posicao_e_devolve_dados(posicao):
    boss = spawn_boss(posicao=posicao)
    assert boss == {"x": float(posicao[0]), "y": float(posicao[1]), "ativo": True}
    assert isinstance(boss["x"], float)
    assert isinstance(boss["y"], float)


def test_factory_devolve_dicionarios_independentes():
    primeiro = spawn_boss((1.5, 2.5))
    segundo = spawn_boss((1.5, 2.5))
    assert primeiro is not segundo
    primeiro["ativo"] = False
    assert segundo["ativo"] is True


@pytest.mark.parametrize("livre", [(1, 0), (1, 2), (0, 1), (2, 1)])
def test_escolhe_cada_direcao_ortogonal_no_centro(game, livre):
    preparar_grade(game, [livre])
    assert game.escolher_posicao_boss() == (livre[0] + 0.5, livre[1] + 0.5)


@pytest.mark.parametrize("jogador,livre", [
    ((0, 0), (1, 0)), ((2, 0), (2, 1)),
    ((0, 2), (0, 1)), ((2, 2), (1, 2)),
])
def test_bordas_nao_viram_posicoes_fora_do_mapa(game, jogador, livre):
    preparar_grade(game, [livre], jogador=jogador)
    assert game.escolher_posicao_boss() == (livre[0] + 0.5, livre[1] + 0.5)


def test_diagonal_nao_e_opcao_de_spawn(game):
    preparar_grade(game, [(0, 0), (2, 0), (0, 2), (2, 2)])
    assert game.escolher_posicao_boss() is None


def test_world_map_bloqueia_paredes_e_terminais(game):
    preparar_grade(game, [(1, 0), (1, 2), (0, 1), (2, 1)])
    game.map.world_map.update({(1, 0): 1, (1, 2): 2, (0, 1): 3})
    assert game.escolher_posicao_boss() == (2.5, 1.5)


@pytest.mark.parametrize("nome_mapa", list(MAPAS))
def test_posicao_valida_nos_cinco_mapas_sem_alterar_cenario(game, nome_mapa):
    game.iniciar_rodada(nome_mapa)
    paredes = dict(game.map.world_map)
    tarefas = set(game.map.tarefas_pendentes)
    pos_jogador = game.player.pos
    x, y = game.escolher_posicao_boss()
    celula = int(x), int(y)
    px, py = game.player.map_pos
    assert 0 <= celula[1] < len(game.map.mini_map)
    assert 0 <= celula[0] < len(game.map.mini_map[celula[1]])
    assert celula not in game.map.world_map
    assert abs(celula[0] - px) + abs(celula[1] - py) == 1
    assert (x, y) == (celula[0] + 0.5, celula[1] + 0.5)
    assert game.map.world_map == paredes
    assert game.map.tarefas_pendentes == tarefas
    assert game.player.pos == pos_jogador


def test_criacao_guarda_os_dados_e_ativa_chefe(game):
    preparar_grade(game, [(2, 1)])
    assert game.criar_boss() is True
    assert game.boss == {"x": 2.5, "y": 1.5, "ativo": True}
    assert game.boss_ativo is True


def test_sem_vizinha_livre_nao_chama_factory_nem_ativa(game, monkeypatch):
    preparar_grade(game, [])
    def nao_deveria_criar(_):
        pytest.fail("A factory não deve ser chamada sem posição livre")
    monkeypatch.setattr(jogo, "spawn_boss", nao_deveria_criar, raising=False)
    assert game.escolher_posicao_boss() is None
    assert game.criar_boss() is False
    assert game.boss is None
    assert game.boss_ativo is False


def test_segunda_tentativa_preserva_o_mesmo_chefe(game, monkeypatch):
    assert game.criar_boss() is True
    chefe = game.boss
    def nao_deveria_criar(_):
        pytest.fail("Não deve criar outro chefe quando já existe um ativo")
    monkeypatch.setattr(jogo, "spawn_boss", nao_deveria_criar)
    assert game.criar_boss() is False
    assert game.boss is chefe
    assert game.boss_ativo is True


def test_nova_partida_limpa_chefe_contador_e_aviso(game):
    assert game.criar_boss() is True
    game.tempo_boss = 31.0
    game.aviso_chefe = "Aviso da partida anterior"
    game.new_game("layout_1")
    assert game.boss is None
    assert game.boss_ativo is False
    assert game.tempo_boss == 0.0
    assert game.aviso_chefe == ""


def test_partida_comeca_sem_criar_chefe_automaticamente(game):
    assert game.boss is None
    assert game.boss_ativo is False
    assert game.tempo_boss == 0.0


def test_criacao_preserva_tarefas_pontos_e_chances(game):
    tarefas = set(game.map.tarefas_pendentes)
    estado = game.pontos, game.chances, game.tempo_restante, game.player.pos
    assert game.criar_boss() is True
    assert game.map.tarefas_pendentes == tarefas
    assert (game.pontos, game.chances, game.tempo_restante, game.player.pos) == estado


def test_quadro_texturizado_continua_funcionando_com_dados_do_chefe(game):
    assert game.criar_boss() is True
    game.update()
    game.draw()
    assert set(game.object_renderer.texturas_parede) == {1, 2, 3}


def test_import_direto_do_modulo_tambem_funciona():
    pasta_src = Path(__file__).resolve().parents[1] / "src"
    resultado = subprocess.run(
        [sys.executable, "-c", "import jogo; from boss import confirma_tempo, spawn_boss"],
        cwd=pasta_src, capture_output=True, text=True, timeout=15,
    )
    assert resultado.returncode == 0, resultado.stderr
