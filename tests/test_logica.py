"""OS TESTES DAS FUNÇÕES DEVERÃO FICAR AQUI. """

"""testes pra ver se o jogo roda liso liso liso"""

from src.settings import (
    RES,
    WIDTH,
    HEIGHT,
    FPS,
    CHANCES_INICIAIS,
    TAREFAS_POR_RODADA,
    TEMPO_INICIAL_RODADA,
    REDUCAO_TEMPO_RODADA,
    TEMPO_MINIMO_RODADA
)


def test_resolucao_janela():
    assert RES == (1600, 900)


def test_largura_janela():
    assert WIDTH == 1600


def test_altura_janela():
    assert HEIGHT == 900


def test_fps():
    assert FPS == 60


def test_chances_iniciais():
    assert CHANCES_INICIAIS == 5


def test_tarefas_por_rodada():
    assert TAREFAS_POR_RODADA == 3


def test_tempo_inicial():
    assert TEMPO_INICIAL_RODADA == 45.0


def test_reducao_tempo():
    assert REDUCAO_TEMPO_RODADA == 3.0


def test_tempo_minimo():
    assert TEMPO_MINIMO_RODADA == 15.0


def test_tempo_inicial_maior_que_minimo():
    assert TEMPO_INICIAL_RODADA > TEMPO_MINIMO_RODADA

""" testes pra ver pts,colisão,se perdeu kkkk, se tomou dano pq atrasou """

import pygame
import pytest

from src.funcoes import (
    calcular_pontos,
    tomar_dano,
    jogador_perdeu,
    limitar_valor,
    verificar_colisao
)


""" Testes de pontuação """
def test_calcular_pontos():
    assert calcular_pontos(100, 50) == 150


def test_calcular_pontos_zero():
    assert calcular_pontos(100, 0) == 100


def test_calcular_pontos_negativos():
    assert calcular_pontos(100, -20) == 80


""" Testes de vida e dano"""

def test_tomar_dano():
    assert tomar_dano(100, 30) == 70


def test_tomar_dano_total():
    assert tomar_dano(100, 100) == 0


def test_tomar_dano_excedente():
    assert tomar_dano(100, 150) == -50


# Testes de fim de jogo
def test_jogador_perdeu():
    assert jogador_perdeu(0) is True


def test_jogador_perdeu_vidas_negativas():
    assert jogador_perdeu(-1) is True


def test_jogador_ainda_tem_vidas():
    assert jogador_perdeu(3) is False


# Testes de limite de valores
def test_limitar_valor_minimo():
    assert limitar_valor(-10, 0, 100) == 0


def test_limitar_valor_maximo():
    assert limitar_valor(150, 0, 100) == 100


def test_limitar_valor_dentro_intervalo():
    assert limitar_valor(50, 0, 100) == 50


""" Testes de colisão """ 

def test_verificar_colisao():
    retangulo_1 = pygame.Rect(0, 0, 50, 50)
    retangulo_2 = pygame.Rect(25, 25, 50, 50)

    assert verificar_colisao(retangulo_1, retangulo_2) is True


def test_nao_verificar_colisao():
    retangulo_1 = pygame.Rect(0, 0, 50, 50)
    retangulo_2 = pygame.Rect(100, 100, 50, 50)

    assert verificar_colisao(retangulo_1, retangulo_2) is False


def test_retangulos_apenas_encostados():
    retangulo_1 = pygame.Rect(0, 0, 50, 50)
    retangulo_2 = pygame.Rect(50, 0, 50, 50)

    assert verificar_colisao(retangulo_1, retangulo_2) is False


"""testes relacionados a mapas"""

import pytest

from src.map import Map, MAPAS, ORDEM_MAPAS, T
from src.settings import TAREFAS_POR_RODADA


""" Testa se todos os mapas estão cadastrados """
def test_existencia_dos_mapas():
    assert len(MAPAS) == 5
    assert len(ORDEM_MAPAS) == 5


""" Testa o carregamento de cada layout """
@pytest.mark.parametrize("nome_mapa", ORDEM_MAPAS)
def test_carregar_mapa(nome_mapa):
    mapa = Map(None, nome_mapa)

    assert mapa.nome_mapa == nome_mapa
    assert mapa.mini_map == MAPAS[nome_mapa]["grade"]
    assert mapa.pos_inicial == MAPAS[nome_mapa]["pos_inicial"]


""" Testa as dimensões dos mapas """
@pytest.mark.parametrize("nome_mapa", ORDEM_MAPAS)
def test_dimensoes_mapa(nome_mapa):
    mapa = Map(None, nome_mapa)

    assert len(mapa.mini_map) == 9
    assert all(len(linha) == 16 for linha in mapa.mini_map)


""" Testa a quantidade de tarefas sorteadas """
def test_quantidade_tarefas():
    mapa = Map(None, "layout_1", qtd_tarefas=3)

    assert mapa.total_tarefas == 3
    assert len(mapa.tarefas_pendentes) == 3


""" Testa se as tarefas estão registradas no mundo """
def test_tarefas_registradas_no_mapa():
    mapa = Map(None, "layout_1", qtd_tarefas=3)

    for posicao in mapa.tarefas_pendentes:
        assert mapa.world_map[posicao] == T


""" Testa se não existem tarefas repetidas """
def test_tarefas_sem_repeticao():
    mapa = Map(None, "layout_1", qtd_tarefas=7)

    assert len(mapa.tarefas_pendentes) == len(set(mapa.tarefas_pendentes))


""" Testa se um mapa desconhecido gera erro """
def test_mapa_inexistente():
    with pytest.raises(ValueError):
        Map(None, "layout_inexistente")


""" Testa a escolha de um mapa aleatório """
def test_mapa_aleatorio():
    mapa = Map(None, "aleatorio")

    assert mapa.nome_mapa in ORDEM_MAPAS


""" Testa se o mapa aleatório evita repetir o anterior """
def test_mapa_aleatorio_sem_repeticao():
    mapa = Map(None, "layout_1")
    mapa.carregar_mapa("aleatorio")

    assert mapa.nome_mapa != "layout_1"


""" Testa a conclusão de uma tarefa """
def test_concluir_tarefa():
    mapa = Map(None, "layout_1", qtd_tarefas=3)

    posicao = next(iter(mapa.tarefas_pendentes))

    resultado = mapa.concluir_tarefa(posicao)

    assert resultado is True
    assert posicao not in mapa.tarefas_pendentes
    assert mapa.world_map[posicao] == 3


""" Testa se uma tarefa já concluída não pode ser concluída novamente """
def test_concluir_tarefa_duas_vezes():
    mapa = Map(None, "layout_1", qtd_tarefas=3)

    posicao = next(iter(mapa.tarefas_pendentes))

    mapa.concluir_tarefa(posicao)
    resultado = mapa.concluir_tarefa(posicao)

    assert resultado is False


""" Testa se uma posição que não é tarefa retorna False """
def test_concluir_posicao_invalida():
    mapa = Map(None, "layout_1", qtd_tarefas=3)

    resultado = mapa.concluir_tarefa((100, 100))

    assert resultado is False


""" Testa se o total de tarefas diminui após conclusão """
def test_diminuir_tarefas_pendentes():
    mapa = Map(None, "layout_1", qtd_tarefas=3)

    posicao = next(iter(mapa.tarefas_pendentes))
    mapa.concluir_tarefa(posicao)

    assert len(mapa.tarefas_pendentes) == 2

"""Para testar somente  uma coisa use:"""
"""python -m pytest tests/test_logica.py -k adicione_aqui_o_nome_da_funçáo"""