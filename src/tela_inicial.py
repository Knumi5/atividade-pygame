import pygame as pg


class Tela_inicial:
    """Gerencia a exibição e navegação pelo teclado na tela inicial do jogo.

    Parâmetros (no construtor):
        game (Game): Instância principal do jogo, usada para acessar `screen`,
            `iniciar_jogo()` e `sair()`.
    """

    def __init__(self, game):
        """Configura fontes e opções do menu principal.

        Parâmetros:
            game (Game): Instância principal do jogo.
        """
        self.game = game
        self.fonte_titulo = pg.font.SysFont('arial', 72, bold=True)
        self.fonte_opcao = pg.font.SysFont('arial', 40)
        self.opcoes = ["Jogar", "Guia", "Consultar rankings", "Sair do jogo"]
        self.selecionada = 0

    def tratar_evento(self, evento):
        """Navega pelas opções com W/S ou setas e confirma com Enter ou Espaço.

        Parâmetros:
            evento (pygame.event.Event): Evento capturado no loop de eventos do Pygame.
        """
        if evento.type == pg.KEYDOWN:
            if evento.key in (pg.K_UP, pg.K_w):
                self.selecionada = (self.selecionada - 1) % len(self.opcoes)
            elif evento.key in (pg.K_DOWN, pg.K_s):
                self.selecionada = (self.selecionada + 1) % len(self.opcoes)
            elif evento.key in (pg.K_RETURN, pg.K_SPACE):
                self.confirmar()

    def confirmar(self):
        """Executa a ação correspondente à opção atualmente selecionada.

        Parâmetros:
            Nenhum (usa `self.opcoes[self.selecionada]`).
        """
        opcao_atual = self.opcoes[self.selecionada]
        if opcao_atual == "Jogar":
            self.game.iniciar_jogo()
        elif opcao_atual == "Sair do jogo":
            self.game.sair()

    def draw(self):
        """Desenha o título do jogo e a lista de opções na tela.

        Parâmetros:
            Nenhum (desenha diretamente em `self.game.screen`).
        """
        tela = self.game.screen
        largura, altura = tela.get_size()
        tela.fill("black")

        titulo = self.fonte_titulo.render("Try // Except", True, "white")
        tela.blit(titulo, titulo.get_rect(center=(largura // 2, altura // 4)))

        for indice, texto in enumerate(self.opcoes):
            cor = "yellow" if indice == self.selecionada else "gray"
            superficie = self.fonte_opcao.render(texto, True, cor)
            tela.blit(
                superficie,
                superficie.get_rect(center=(largura // 2, altura // 2 + indice * 70)),
            )
