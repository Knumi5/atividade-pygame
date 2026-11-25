import pytest


def test_cinco_perguntas_distintas_e_validas():
    from src.tarefas import PERGUNTAS

    assert len(PERGUNTAS) == 5
    assert len({q["id"] for q in PERGUNTAS}) == 5
    for pergunta in PERGUNTAS:
        assert pergunta["enunciado"].strip()
        assert pergunta["resposta"].strip()
        assert pergunta["resposta"] == pergunta["resposta"].strip().lower()


@pytest.mark.parametrize("texto,esperado", [
    (" PRINT ", "print"), ("If", "if"), ("\tDEF\n", "def"),
    ("", ""), ("   ", ""), (" print() ", "print()"),
])
def test_normalizacao(texto, esperado):
    from src.tarefas import normalizar_resposta

    assert normalizar_resposta(texto) == esperado


@pytest.mark.parametrize("resposta,correta", [
    ("print", True), (" PRINT ", True), ("input", False), ("", False),
])
def test_validacao_da_resposta(resposta, correta):
    from src.tarefas import validar_resposta

    pergunta = {"id": "exemplo", "enunciado": "Como exibir?", "resposta": "print"}
    assert validar_resposta(pergunta, resposta) is correta


def test_distribuicao_atende_todos_os_terminais_sem_alterar_o_banco():
    from src.tarefas import PERGUNTAS, distribuir_perguntas

    banco_original = [dict(q) for q in PERGUNTAS]
    terminais = {(i, 0) for i in range(7)}
    resultado = distribuir_perguntas(terminais)
    assert set(resultado) == terminais
    assert all(q in PERGUNTAS for q in resultado.values())
    assert list(PERGUNTAS) == banco_original
    assert distribuir_perguntas(set()) == {}


def test_cinco_terminais_recebem_cinco_perguntas_diferentes():
    from src.tarefas import distribuir_perguntas

    resultado = distribuir_perguntas({(i, 0) for i in range(5)})
    assert len({q["id"] for q in resultado.values()}) == 5
