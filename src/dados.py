def salvar_recorde(caminho_arquivo, pontuacao):
    """Salva a pontuação recorde em um arquivo de texto.

    Parâmetros:
        caminho_arquivo (str | Path): Caminho do arquivo onde o recorde será gravado.
        pontuacao (int | float): Valor da pontuação a ser salva.
    """
    with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
        arquivo.write(str(pontuacao))


def carregar_recorde(caminho_arquivo):
    """Carrega o recorde salvo; retorna 0 se o arquivo não existir ou estiver vazio.

    Parâmetros:
        caminho_arquivo (str | Path): Caminho do arquivo de recorde a ser lido.

    Retorno:
        int: Pontuação recorde carregada, ou 0 caso não exista valor válido.
    """
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.read().strip()

            if conteudo == "":
                return 0

            return int(conteudo)

    except FileNotFoundError:
        return 0