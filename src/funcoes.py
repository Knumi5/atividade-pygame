def calcular_pontos(pontos_atual, pontos_ganhos):
    """Soma os pontos ganhos à pontuação atual.

    Parâmetros:
        pontos_atual (int | float): Pontuação acumulada até o momento.
        pontos_ganhos (int | float): Pontos obtidos na ação atual.

    Retorno:
        int | float: Nova pontuação total.
    """
    return pontos_atual + pontos_ganhos


def tomar_dano(vida_atual, dano):
    """Reduz a vida atual com base no dano recebido.

    Parâmetros:
        vida_atual (int | float): Quantidade atual de vida/chances.
        dano (int | float): Quantidade de dano a descontar.

    Retorno:
        int | float: Vida restante após o dano.
    """
    return vida_atual - dano


def jogador_perdeu(vidas):
    """Indica se o jogador ficou sem vidas.

    Parâmetros:
        vidas (int | float): Quantidade restante de vidas do jogador.

    Retorno:
        bool: True se `vidas <= 0`; caso contrário, False.
    """
    return vidas <= 0


def limitar_valor(valor, minimo, maximo):
    """Mantém um valor dentro do intervalo `[minimo, maximo]`.

    Parâmetros:
        valor (int | float): Número que será limitado.
        minimo (int | float): Limite inferior permitido.
        maximo (int | float): Limite superior permitido.

    Retorno:
        int | float: O próprio `valor`, ou o limite mais próximo caso ultrapasse.
    """
    if valor < minimo:
        return minimo
    if valor > maximo:
        return maximo
    return valor


def verificar_colisao(retangulo_1, retangulo_2):
    """Verifica se há sobreposição entre dois retângulos do Pygame.

    Parâmetros:
        retangulo_1 (pygame.Rect): Primeiro retângulo de colisão.
        retangulo_2 (pygame.Rect): Segundo retângulo de colisão.

    Retorno:
        bool: True se os retângulos colidirem; False caso contrário.
    """
    return retangulo_1.colliderect(retangulo_2)