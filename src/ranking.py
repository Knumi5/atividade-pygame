import os

# O arquivo fica na mesma pasta deste código, não importa de onde o jogo seja executado.
ARQUIVO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ranking.txt")
LIMITE_NOME = 12
MAIOR_E_MELHOR = True  # Troque para False se a pontuação for um tempo (menor = melhor)

def limpar_nome(nome):
    """Remove caracteres que quebrariam o arquivo e limita o tamanho do nome.

    Parâmetros:
        nome (str): Nome digitado pelo jogador.

    Retorna:
        str: Nome limpo (sem ";", sem quebras de linha, sem espaços sobrando).
    """
    nome = nome.replace(";", " ").replace("\n", " ").replace("\r", " ")
    return " ".join(nome.split())[:LIMITE_NOME]

def _e_melhor(novo, antigo):
    """Compara duas pontuações de acordo com `MAIOR_E_MELHOR`.

    Parâmetros:
        novo (int): Pontuação recém-feita.
        antigo (int): Melhor pontuação já registrada.
    """
    return novo > antigo if MAIOR_E_MELHOR else novo < antigo

def _ordenar(dados):
    """Ordena {nome: pontos} do melhor para o pior, desempatando por nome (A-Z).

    Parâmetros:
        dados (dict): {nome: melhor_pontuacao}.

    Retorna:
        list[tuple[str, int]]: Lista de (nome, pontuacao) ordenada.
    """
    sinal = -1 if MAIOR_E_MELHOR else 1
    return sorted(dados.items(), key=lambda par: (sinal * par[1], par[0].casefold()))


def carregar():
    """Lê o arquivo de ranking.

    Parâmetros:
        Nenhum.

    Retorna:
        dict: {nome: melhor_pontuacao}. Se o arquivo não existir, retorna {}.
        Linhas com formato inválido são ignoradas.
    """
    dados = {}
    try:
        with open(ARQUIVO, "r", encoding="utf-8") as arq:
            for linha in arq:
                nome, separador, pontos = linha.rstrip("\r\n").rpartition(";")
                if not separador:
                    continue
                try:
                    pontos = int(pontos)
                except ValueError:
                    continue
                nome = nome.strip()
                if nome and (nome not in dados or _e_melhor(pontos, dados[nome])):
                    dados[nome] = pontos
    except FileNotFoundError:
        pass
    return dados


def _gravar(dados):
    """Grava o dicionário no arquivo, do melhor para o pior.

    Escreve primeiro num arquivo temporário e depois o substitui, para o ranking
    não ficar corrompido se o jogo fechar no meio da gravação.

    Parâmetros:
        dados (dict): {nome: melhor_pontuacao}.
    """
    ordenado = _ordenar(dados)
    temporario = ARQUIVO + ".tmp"
    with open(temporario, "w", encoding="utf-8") as arq:
        for nome, pontos in ordenado:
            arq.write(f"{nome};{pontos}\n")
    os.replace(temporario, ARQUIVO)


def salvar_melhor(nome, pontos):
    """Registra a pontuação do jogador se ela for a melhor dele até agora.

    Parâmetros:
        nome (str): Nome do jogador.
        pontos (int): Pontuação feita na partida.

    Retorna:
        bool: True se a pontuação virou o novo recorde do jogador (ou se ele
        ainda não estava no arquivo); False caso contrário.
    """
    nome = limpar_nome(nome)
    if not nome:
        return False
    dados = carregar()
    if nome in dados and not _e_melhor(pontos, dados[nome]):
        return False
    dados[nome] = pontos
    _gravar(dados)
    return True


def melhores(quantidade=10):
    """Lista os melhores colocados (útil para a futura tela de rankings).

    Parâmetros:
        quantidade (int): Quantos jogadores retornar.

    Retorna:
        list[tuple[str, int]]: Lista de (nome, pontuacao) do melhor para o pior.
    """
    return _ordenar(carregar())[:quantidade]