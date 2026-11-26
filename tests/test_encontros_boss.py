"""Cenários de Q04-Q07, definidos antes da implementação do encontro."""
import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

import pygame as pg
import pytest

from src import jogo, ranking, settings
from src.map import MAPAS


class RelogioControlado:
    def tick(self, _fps):
        return 16

    def get_fps(self):
        return 60.0


@pytest.fixture
def encontro(tmp_path, monkeypatch):
    monkeypatch.setattr(jogo, "CAMINHO_RECORDE", str(tmp_path / "recorde.txt"))
    monkeypatch.setattr(ranking, "ARQUIVO", str(tmp_path / "ranking.txt"))
    instancia = jogo.Game()
    instancia.nome_jogador = "Teste Boss"
    instancia.iniciar_jogo("layout_1")
    instancia.clock = RelogioControlado()
    # Isola os limites do chefe do limite da rodada, salvo nos testes de transição.
    instancia.tempo_restante = 1000.0
    pg.event.clear()
    yield instancia
    pg.quit()


def avancar(game, segundos):
    game.delta_time = round(segundos * 1000)
    game.update()


def aparecer(game):
    avancar(game, 30.0)
    assert game.boss_ativo is True
    return game.boss


def pressionar(game, tecla=pg.K_f):
    pg.event.post(pg.event.Event(pg.KEYDOWN, key=tecla, unicode=pg.key.name(tecla)))
    game.check_events()


@pytest.mark.parametrize("segundos", [0.0, 15.0, 29.9])
def test_antes_30_segundos_nao_cria(encontro, segundos):
    avancar(encontro, segundos)
    assert encontro.boss is None
    assert encontro.boss_ativo is False


def test_update_consulta_regra_de_autorizacao(encontro, monkeypatch):
    consultas = []
    original = jogo.confirma_tempo
    def consultar(tempo, ativo):
        consultas.append((tempo, ativo))
        return original(tempo, ativo)
    monkeypatch.setattr(jogo, "confirma_tempo", consultar)
    avancar(encontro, 29.9)
    assert consultas == [(pytest.approx(29.9), False)]


@pytest.mark.parametrize("intervalos", [(30.0,), (30.1,), (29.9, 0.1), (29.99, 0.02)])
def test_atingir_ou_ultrapassar_30_cria(encontro, intervalos):
    for segundos in intervalos:
        avancar(encontro, segundos)
    assert encontro.boss_ativo is True
    assert encontro.boss["ativo"] is True
    celula = int(encontro.boss["x"]), int(encontro.boss["y"])
    assert celula not in encontro.map.world_map


def test_varios_quadros_nao_duplicam_chefe(encontro, monkeypatch):
    chamadas = []
    original = jogo.spawn_boss
    def criar(posicao):
        chamadas.append(posicao)
        return original(posicao)
    monkeypatch.setattr(jogo, "spawn_boss", criar)
    chefe = aparecer(encontro)
    # O prazo ainda não expira nesses quadros.
    for _ in range(20):
        avancar(encontro, 0.016)
    assert len(chamadas) == 1
    assert encontro.boss is chefe


def test_sem_espaco_tenta_novamente_sem_ativar(encontro):
    posicao = encontro.escolher_posicao_boss()
    celula_livre = int(posicao[0]), int(posicao[1])
    px, py = encontro.player.map_pos
    for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
        encontro.map.world_map[(px + dx, py + dy)] = 1
    avancar(encontro, 30.0)
    assert encontro.boss is None
    assert encontro.boss_ativo is False
    assert encontro.aviso_chefe == ""
    del encontro.map.world_map[celula_livre]
    avancar(encontro, 0.1)
    assert encontro.boss_ativo is True


@pytest.mark.parametrize("estado", ["menu", "guia", "game_over"])
def test_fora_da_partida_nao_conta_nem_cria(encontro, estado):
    encontro.estado = estado
    encontro.tempo_boss = 29.9
    avancar(encontro, 2.0)
    assert encontro.tempo_boss == 29.9
    assert encontro.boss is None


def test_pergunta_pausa_espera_e_retorno_nao_acumula_punicao(encontro):
    encontro.tempo_boss = 29.9
    encontro.painel_pergunta = {"pergunta": "teste"}
    rodada = encontro.tempo_restante
    avancar(encontro, 60.0)
    assert encontro.tempo_boss == 29.9
    assert encontro.tempo_restante == rodada
    assert encontro.boss is None
    encontro.painel_pergunta = None
    avancar(encontro, 0.1)
    assert encontro.boss_ativo is True


def test_aparicao_valida_exibe_aviso(encontro):
    aparecer(encontro)
    assert "chefe" in encontro.aviso_chefe.lower()


def test_regras_confirmadas_pelo_usuario():
    assert settings.TECLA_CUMPRIMENTO_BOSS == pg.K_f
    assert settings.ALCANCE_CUMPRIMENTO_BOSS == 1.8
    assert settings.PRAZO_CUMPRIMENTO_BOSS == 5.0
    assert settings.PENALIDADE_BOSS == 1


@pytest.mark.parametrize("distancia,aceito", [(0.5, True), (1.8, True), (1.801, False), (4.0, False)])
def test_cumprimento_respeita_alcance(encontro, distancia, aceito):
    chefe = aparecer(encontro)
    encontro.player.x = chefe["x"] + distancia
    encontro.player.y = chefe["y"]
    assert encontro.cumprimentar_boss() is aceito
    assert encontro.boss_ativo is (not aceito)


def test_sem_chefe_cumprimento_nao_tem_efeito(encontro):
    estado = encontro.chances, encontro.pontos, encontro.tempo_boss
    assert encontro.cumprimentar_boss() is False
    assert (encontro.chances, encontro.pontos, encontro.tempo_boss) == estado


def test_cumprimento_no_prazo_nao_pune(encontro):
    chefe = aparecer(encontro)
    chances = encontro.chances
    avancar(encontro, 4.0)
    pressionar(encontro)
    assert encontro.boss is None
    assert encontro.boss_ativo is False
    assert chefe["ativo"] is False
    assert encontro.aviso_chefe == ""
    assert encontro.chances == chances
    avancar(encontro, 1.1)
    assert encontro.chances == chances


def test_evento_f_cumprimenta_sem_interagir_com_terminal(encontro, monkeypatch):
    aparecer(encontro)
    def terminal_nao_deve_ser_acionado():
        pytest.fail("O cumprimento não deve resolver um terminal")
    monkeypatch.setattr(encontro.player, "interagir_tarefa", terminal_nao_deve_ser_acionado)
    pressionar(encontro)
    assert encontro.boss_ativo is False


def test_mesma_tecla_nao_cumprimenta_e_resolve_terminal(encontro, monkeypatch):
    aparecer(encontro)
    monkeypatch.setattr(jogo, "TECLA_CUMPRIMENTO_BOSS", pg.K_e)
    def terminal_nao_deve_ser_acionado():
        pytest.fail("O evento já foi consumido pelo cumprimento")
    monkeypatch.setattr(encontro.player, "interagir_tarefa", terminal_nao_deve_ser_acionado)
    pressionar(encontro, pg.K_e)
    assert encontro.boss_ativo is False


def test_outra_tecla_nao_cumprimenta(encontro):
    aparecer(encontro)
    pressionar(encontro, pg.K_g)
    assert encontro.boss_ativo is True


def test_tecla_repetida_nao_resolve_outro_encontro(encontro):
    aparecer(encontro)
    chances = encontro.chances
    pressionar(encontro)
    pressionar(encontro)
    assert encontro.boss is None
    assert encontro.tempo_boss == 0.0
    assert encontro.chances == chances


def test_encerrar_rearma_espera_completa(encontro):
    aparecer(encontro)
    assert encontro.cumprimentar_boss() is True
    assert encontro.tempo_boss == 0.0
    avancar(encontro, 29.9)
    assert encontro.boss is None
    avancar(encontro, 0.1)
    assert encontro.boss_ativo is True


def test_prazo_comeca_na_criacao_e_tem_contador_proprio(encontro):
    aparecer(encontro)
    assert encontro.tempo_cumprimento_boss == 5.0
    assert encontro.tempo_boss == 30.0
    assert encontro.tempo_restante == 970.0


def test_prazo_decrementa_sem_mudar_contador_de_espera(encontro):
    aparecer(encontro)
    espera = encontro.tempo_boss
    rodada = encontro.tempo_restante
    avancar(encontro, 1.5)
    assert encontro.tempo_cumprimento_boss == 3.5
    assert encontro.tempo_boss == espera
    assert encontro.tempo_restante == rodada - 1.5


def test_prazo_so_comeca_quando_ha_posicao_valida(encontro):
    px, py = encontro.player.map_pos
    for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
        encontro.map.world_map[(px + dx, py + dy)] = 1
    avancar(encontro, 30.0)
    assert encontro.boss is None
    assert encontro.tempo_cumprimento_boss == 0.0


def test_prazo_expirado_nao_aceita_cumprimento(encontro):
    aparecer(encontro)
    encontro.tempo_cumprimento_boss = 0.0
    assert encontro.cumprimentar_boss() is False


def test_expiracao_aplica_uma_penalidade_e_preserva_rodada(encontro):
    aparecer(encontro)
    mapa = encontro.map
    tarefas = set(mapa.tarefas_pendentes)
    jogador = encontro.player.pos
    chances = encontro.chances
    pontos = encontro.pontos
    avancar(encontro, 5.0)
    assert encontro.chances == chances - 1
    assert encontro.map is mapa
    assert encontro.map.tarefas_pendentes == tarefas
    assert encontro.player.pos == jogador
    assert encontro.pontos == pontos
    assert encontro.boss is None
    assert encontro.boss_ativo is False
    assert encontro.aviso_chefe == ""
    assert encontro.tempo_cumprimento_boss == 0.0
    assert encontro.tempo_boss == 0.0
    for _ in range(10):
        avancar(encontro, 0.1)
    assert encontro.chances == chances - 1


def test_penalidade_com_ultima_chance_salva_ranking_e_game_over(encontro):
    aparecer(encontro)
    encontro.chances = 1
    encontro.pontos = 7
    avancar(encontro, 5.0)
    assert encontro.chances == 0
    assert encontro.estado == "game_over"
    assert encontro.boss is None
    assert encontro.recorde == 7
    assert ranking.carregar()["Teste Boss"] == 7
    avancar(encontro, 60.0)
    assert encontro.chances == 0
    encontro.draw()


def test_pergunta_pausa_prazo_e_impede_cumprimento(encontro):
    aparecer(encontro)
    encontro.painel_pergunta = {"pergunta": "teste"}
    chances = encontro.chances
    avancar(encontro, 60.0)
    assert encontro.tempo_cumprimento_boss == 5.0
    assert encontro.cumprimentar_boss() is False
    assert encontro.chances == chances
    encontro.painel_pergunta = None
    avancar(encontro, 4.9)
    assert encontro.chances == chances
    avancar(encontro, 0.1)
    assert encontro.chances == chances - 1


def test_nova_partida_limpa_todo_estado_do_encontro(encontro):
    aparecer(encontro)
    avancar(encontro, 2.0)
    encontro.new_game("layout_1")
    assert encontro.boss is None
    assert encontro.boss_ativo is False
    assert encontro.tempo_boss == 0.0
    assert encontro.tempo_cumprimento_boss == 0.0
    assert encontro.aviso_chefe == ""


@pytest.mark.parametrize("nome_mapa", list(MAPAS))
def test_troca_de_mapa_preserva_encontro_em_posicao_valida(encontro, nome_mapa):
    chefe = aparecer(encontro)
    avancar(encontro, 1.0)
    prazo = encontro.tempo_cumprimento_boss
    encontro.iniciar_rodada(nome_mapa)
    assert encontro.boss is chefe
    assert encontro.boss_ativo is True
    assert encontro.tempo_cumprimento_boss == prazo
    celula = int(chefe["x"]), int(chefe["y"])
    px, py = encontro.player.map_pos
    assert celula not in encontro.map.world_map
    assert abs(celula[0] - px) + abs(celula[1] - py) == 1


def test_timeout_da_rodada_nao_duplica_penalidade_do_chefe(encontro):
    aparecer(encontro)
    encontro.tempo_restante = 1.0
    chances = encontro.chances
    avancar(encontro, 5.0)
    assert encontro.chances == chances - 1
    assert encontro.boss is None
    assert encontro.tempo_boss == 0.0


def test_espera_acumula_entre_rodadas_curta(encontro):
    avancar(encontro, 20.0)
    encontro.iniciar_rodada("layout_2")
    avancar(encontro, 10.0)
    assert encontro.boss_ativo is True


def test_ciclo_completo_eventos_hud_e_game_over(encontro):
    aparecer(encontro)
    encontro.draw()
    pressionar(encontro)
    assert encontro.boss is None
    encontro.draw()
    avancar(encontro, 30.0)
    assert encontro.boss_ativo is True
    encontro.chances = 2
    avancar(encontro, 5.0)
    assert encontro.estado == "jogando"
    assert encontro.chances == 1
    encontro.draw()
    avancar(encontro, 30.0)
    avancar(encontro, 5.0)
    assert encontro.estado == "game_over"
    assert encontro.chances == 0
    encontro.draw()
