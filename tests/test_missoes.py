from types import SimpleNamespace

import pygame as pg
import pytest

from src import ranking
from src.settings import CHANCES_INICIAIS, FPS, TAREFAS_POR_RODADA


def tecla(game, key, texto=""):
    pg.event.post(pg.event.Event(pg.KEYDOWN, key=key, unicode=texto))
    game.check_events()


def abrir(game, terminal):
    assert game.abrir_pergunta(terminal) is True
    return game.painel_pergunta


def enviar(game, resposta):
    game.painel_pergunta["digitado"] = resposta
    tecla(game, pg.K_RETURN)


def test_buscar_terminal_nao_altera_estado(game, terminal):
    pendentes = set(game.map.tarefas_pendentes)
    assert game.player.buscar_terminal_proximo() == terminal
    assert game.map.tarefas_pendentes == pendentes
    assert game.pontos == 0


@pytest.mark.parametrize("mouse", [False, True])
def test_interacao_abre_sem_concluir_ou_pontuar(game, terminal, mouse):
    pendentes = set(game.map.tarefas_pendentes)
    evento = (pg.event.Event(pg.MOUSEBUTTONDOWN, button=1, pos=(0, 0))
              if mouse else pg.event.Event(pg.KEYDOWN, key=pg.K_e, unicode="e"))
    pg.event.post(evento)
    game.check_events()
    assert game.painel_pergunta is not None
    assert game.painel_pergunta["terminal"] == terminal
    assert game.painel_pergunta["digitado"] == ""
    assert game.map.tarefas_pendentes == pendentes
    assert game.pontos == 0
    assert game.chances == CHANCES_INICIAIS


def test_fora_do_alcance_nao_abre(game):
    game.player.x, game.player.y = 8.5, 5.5
    pendentes = set(game.map.tarefas_pendentes)
    tecla(game, pg.K_e, "e")
    assert game.painel_pergunta is None
    assert game.map.tarefas_pendentes == pendentes


def test_terminal_resolvido_nao_pode_reabrir(game, terminal):
    game.map.concluir_tarefa(terminal)
    assert game.abrir_pergunta(terminal) is False
    assert game.painel_pergunta is None


def test_busca_respeita_limite_de_alcance(game, terminal):
    game.player.x = 2.3
    assert game.player.buscar_terminal_proximo(1.8) == terminal
    game.player.x = 2.31
    assert game.player.buscar_terminal_proximo(1.8) is None


def test_digitacao_backspace_e_limite(game, terminal):
    from src.tarefas import LIMITE_RESPOSTA

    abrir(game, terminal)
    for char in "wasd":
        tecla(game, ord(char), char)
    assert game.painel_pergunta["digitado"] == "wasd"
    tecla(game, pg.K_BACKSPACE)
    assert game.painel_pergunta["digitado"] == "was"
    for _ in range(LIMITE_RESPOSTA + 5):
        tecla(game, pg.K_x, "x")
    assert len(game.painel_pergunta["digitado"]) == LIMITE_RESPOSTA


def test_enter_vazio_nao_penaliza(game, terminal):
    abrir(game, terminal)
    enviar(game, "   ")
    assert game.em_tarefa
    assert game.pontos == 0
    assert game.chances == CHANCES_INICIAIS
    assert terminal in game.map.tarefas_pendentes


def test_acerto_normalizado_resolve_uma_vez(game, terminal):
    painel = abrir(game, terminal)
    enviar(game, "  " + painel["questao"]["resposta"].upper() + "  ")
    assert game.pontos == 1
    assert game.chances == CHANCES_INICIAIS
    assert terminal not in game.map.tarefas_pendentes
    assert terminal in game.map.tarefas_concluidas
    assert not game.em_tarefa
    tecla(game, pg.K_RETURN)
    assert game.pontos == 1


def test_erro_preserva_rodada_mapa_tempo_e_outros_terminais(game, terminal):
    mapa = game.map
    pendentes = set(mapa.tarefas_pendentes)
    posicao = game.player.pos
    tempo = game.tempo_restante
    abrir(game, terminal)
    enviar(game, "resposta_errada")
    assert game.pontos == 0
    assert game.chances == CHANCES_INICIAIS - 1
    assert game.map is mapa
    assert game.player.pos == posicao
    assert game.tempo_restante == tempo
    assert game.rodada == 1
    assert mapa.tarefas_pendentes == pendentes - {terminal}
    assert terminal not in mapa.tarefas_concluidas
    assert terminal in mapa.tarefas_erradas
    assert mapa.world_map[terminal] != 3
    tecla(game, pg.K_RETURN)
    assert game.chances == CHANCES_INICIAIS - 1


def test_erro_sem_chances_encerra_e_preserva_persistencia(game, terminal):
    game.chances = 1
    game.pontos = 4
    abrir(game, terminal)
    enviar(game, "resposta_errada")
    assert game.estado == "game_over"
    assert game.chances == 0
    assert game.rodada == 1
    assert not game.em_tarefa
    assert game.recorde == 4
    assert ranking.carregar()["Ricardo"] == 4
    game.draw()


@pytest.mark.parametrize("acertou", [False, True])
def test_ultimo_terminal_avanca_rodada_uma_vez(game, terminal, acertou):
    game.map.tarefas_pendentes = {terminal}
    game.map.total_tarefas = 1
    painel = abrir(game, terminal)
    resposta = painel["questao"]["resposta"] if acertou else "errada"
    enviar(game, resposta)
    assert game.rodada == 2
    assert game.pontos == int(acertou)
    assert game.chances == CHANCES_INICIAIS - int(not acertou)
    assert len(game.map.tarefas_pendentes) == TAREFAS_POR_RODADA
    assert not game.map.tarefas_concluidas
    assert not game.map.tarefas_erradas
    tecla(game, pg.K_RETURN)
    assert game.rodada == 2


def test_tres_acertos_concluem_a_rodada(game):
    for terminal in sorted(game.map.tarefas_pendentes):
        painel = abrir(game, terminal)
        enviar(game, painel["questao"]["resposta"])
    assert game.rodada == 2
    assert game.pontos == 3
    assert game.chances == CHANCES_INICIAIS


def test_pergunta_pausa_mundo_mas_mantem_relogio_de_quadros(game, terminal, monkeypatch):
    abrir(game, terminal)
    tempo = game.tempo_restante
    atualizacoes = []
    ticks = []
    monkeypatch.setattr(game.player, "update", lambda: atualizacoes.append("player"))
    monkeypatch.setattr(game.raycasting, "update", lambda: atualizacoes.append("raycast"))
    game.clock = SimpleNamespace(tick=lambda fps: ticks.append(fps) or 16, get_fps=lambda: 60)
    game.delta_time = 2000
    game.update()
    assert game.tempo_restante == tempo
    assert atualizacoes == []
    assert ticks == [FPS]
    assert game.delta_time == 16


def test_atalhos_na_pergunta_nao_trocam_mapa(game, terminal):
    abrir(game, terminal)
    nome = game.map.nome_mapa
    pendentes = set(game.map.tarefas_pendentes)
    game.tempo_restante = 7
    for char in "m12345":
        tecla(game, ord(char), char)
    assert game.map.nome_mapa == nome
    assert game.map.tarefas_pendentes == pendentes
    assert game.tempo_restante == 7
    assert game.painel_pergunta["digitado"] == "m12345"


def test_escape_cancela_preservando_a_partida(game, terminal):
    abrir(game, terminal)
    pendentes = set(game.map.tarefas_pendentes)
    posicao = game.player.pos
    tempo = game.tempo_restante
    tecla(game, pg.K_ESCAPE)
    assert game.estado == "jogando"
    assert not game.em_tarefa
    assert game.map.tarefas_pendentes == pendentes
    assert game.player.pos == posicao
    assert game.tempo_restante == tempo
    assert game.pontos == 0
    assert game.chances == CHANCES_INICIAIS


def test_reabrir_nao_troca_questao_nem_reaproveita_texto(game, terminal):
    for _ in range(3):
        painel = abrir(game, terminal)
        questao = painel["questao"]["id"]
        assert painel["digitado"] == ""
        tecla(game, pg.K_x, "x")
        tecla(game, pg.K_ESCAPE)
        painel = abrir(game, terminal)
        assert painel["questao"]["id"] == questao
        tecla(game, pg.K_ESCAPE)
    assert game.pontos == 0
    assert terminal in game.map.tarefas_pendentes


def test_fechar_limpa_deslocamento_acumulado_do_mouse(game, terminal, monkeypatch):
    abrir(game, terminal)
    leituras = []
    monkeypatch.setattr(pg.mouse, "get_rel", lambda: leituras.append(True) or (0, 0))
    game.fechar_pergunta()
    assert leituras


def test_nova_partida_limpa_painel_e_resultados(game, terminal):
    abrir(game, terminal)
    game.painel_pergunta["digitado"] = "resposta antiga"
    game.pontos = 2
    game.chances = 2
    game.iniciar_jogo("layout_1")
    assert game.painel_pergunta is None
    assert game.pontos == 0
    assert game.chances == CHANCES_INICIAIS
    assert game.rodada == 1
    assert len(game.map.tarefas_pendentes) == TAREFAS_POR_RODADA


def test_painel_exibe_enunciado_mas_nao_resposta_interna(game, terminal):
    painel = abrir(game, terminal)
    painel["questao"] = {"id": "visual", "enunciado": "Qual palavra exibe mensagens?", "resposta": "RESPOSTA_SECRETA"}
    textos = []

    class FonteObservada:
        def __init__(self, fonte):
            self.fonte = fonte

        def render(self, texto, *args):
            textos.append(texto)
            return self.fonte.render(texto, *args)

        def __getattr__(self, nome):
            return getattr(self.fonte, nome)

    game.fonte_hud = FonteObservada(game.fonte_hud)
    game.fonte_hud_destaque = FonteObservada(game.fonte_hud_destaque)
    game.desenhar_painel_pergunta()
    assert any("Qual palavra" in texto for texto in textos)
    assert not any("RESPOSTA_SECRETA" in texto for texto in textos)
    assert not any("'terminal':" in texto for texto in textos)


def test_hud_distingue_resolvidas_e_acertos(game, terminal):
    abrir(game, terminal)
    enviar(game, "errada")
    assert game.map.total_tarefas - len(game.map.tarefas_pendentes) == 1
    assert len(game.map.tarefas_concluidas) == 0
    assert len(game.map.tarefas_erradas) == 1
    game.draw()


def test_quit_continua_funcionando_com_pergunta_aberta(game, terminal, monkeypatch):
    abrir(game, terminal)

    def sair():
        raise SystemExit

    monkeypatch.setattr(game, "sair", sair)
    pg.event.post(pg.event.Event(pg.QUIT))
    with pytest.raises(SystemExit):
        game.check_events()


def test_menu_preserva_entrada_de_nome_de_fernando(game):
    game.estado = "menu"
    tela = game.tela_inicial
    tela.selecionada = tela.opcoes.index("Nome")
    tela.confirmar()
    for char in "Ricardo":
        tecla(game, ord(char.lower()), char)
    tecla(game, pg.K_RETURN)
    assert not tela.digitando
    assert tela.nome == "Ricardo"
    tecla(game, pg.K_RETURN)
    assert game.estado == "jogando"
    assert game.nome_jogador == "Ricardo"


def test_timeout_fora_do_painel_preserva_comportamento_existente(game):
    game.tempo_restante = 0.001
    game.delta_time = 100
    game.pontos = 2
    game.update()
    assert game.chances == CHANCES_INICIAIS - 1
    assert game.rodada == 1
    assert game.pontos == 2
    assert game.tempo_restante == game.tempo_limite_rodada
    assert len(game.map.tarefas_pendentes) == TAREFAS_POR_RODADA


def test_timeout_na_ultima_chance_encerra_partida(game):
    game.chances = 1
    game.tempo_restante = 0.001
    game.delta_time = 100
    game.update()
    assert game.estado == "game_over"
    assert game.chances == 0


def test_pergunta_aberta_impede_abrir_outro_terminal(game, terminal):
    painel = abrir(game, terminal)
    outro = next(pos for pos in game.map.tarefas_pendentes if pos != terminal)
    assert game.abrir_pergunta(outro) is False
    assert game.painel_pergunta is painel


def test_resposta_larga_fica_dentro_do_campo(game, terminal):
    from src.tarefas import LIMITE_RESPOSTA

    abrir(game, terminal)
    game.painel_pergunta["digitado"] = "W" * LIMITE_RESPOSTA
    larguras = []

    class FonteObservada:
        def __init__(self, fonte):
            self.fonte = fonte

        def render(self, texto, *args):
            surf = self.fonte.render(texto, *args)
            if texto.startswith("> "):
                larguras.append(surf.get_width())
            return surf

        def __getattr__(self, nome):
            return getattr(self.fonte, nome)

    game.fonte_hud = FonteObservada(game.fonte_hud)
    game.desenhar_painel_pergunta()
    assert larguras
    assert max(larguras) <= 860 - 64 - 24
    assert len(game.painel_pergunta["digitado"]) == LIMITE_RESPOSTA
