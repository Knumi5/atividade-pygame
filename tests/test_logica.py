
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
