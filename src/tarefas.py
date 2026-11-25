"""Perguntas e regras de resposta, independentes da janela do Pygame."""
import random

LIMITE_RESPOSTA = 40

PERGUNTAS = (
    {"id": "q01", "enunciado": "Qual função exibe mensagens no console em Python?", "resposta": "print"},
    {"id": "q02", "enunciado": "Qual palavra-chave inicia uma condição em Python?", "resposta": "if"},
    {"id": "q03", "enunciado": "Qual palavra-chave define uma função em Python?", "resposta": "def"},
    {"id": "q04", "enunciado": "Qual função retorna a quantidade de elementos de uma lista?", "resposta": "len"},
    {"id": "q05", "enunciado": "Qual palavra-chave percorre os itens de uma sequência em Python?", "resposta": "for"},
)


def normalizar_resposta(texto):
    """Remove espaços externos e ignora diferença entre maiúsculas e minúsculas."""
    return texto.strip().lower()


def validar_resposta(pergunta, resposta):
    """Compara a resposta sem alterar os dados da pergunta ou a pontuação."""
    return normalizar_resposta(resposta) == normalizar_resposta(pergunta["resposta"])


def distribuir_perguntas(terminais):
    """Associa perguntas aos terminais da rodada, sem repetir antes de usar o banco.

    O resultado é guardado pelo jogo até a rodada acabar. Assim, cancelar e
    reabrir um terminal não troca sua pergunta. Se houver mais de cinco
    terminais, o banco é reutilizado sem limitar a quantidade de tarefas.
    """
    perguntas = list(PERGUNTAS)
    random.shuffle(perguntas)
    return {
        terminal: perguntas[indice % len(perguntas)]
        for indice, terminal in enumerate(sorted(terminais))
    }
