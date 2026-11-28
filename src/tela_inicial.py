import pygame as pg
try:
    from .ranking import limpar_nome, LIMITE_NOME
except ImportError:
    from ranking import limpar_nome, LIMITE_NOME

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
        self.opcoes = ["Nome", "Jogar", "Guia", "Consultar rankings", "Sair do jogo"]
        self.selecionada = 0
        self.nome = ""
        self.digitando = False
        self.aviso = ""

    def tratar_evento(self, evento):
        """Navega pelas opções com W/S ou setas e confirma com Enter ou Espaço.

        Parâmetros:
            evento (pygame.event.Event): Evento capturado no loop de eventos do Pygame.
        """
        if self.digitando:
            if evento.type == pg.KEYDOWN:
                self.tratar_digitacao(evento)
            return
        if evento.type == pg.KEYDOWN:
            if evento.key in (pg.K_UP, pg.K_w):
                self.selecionada = (self.selecionada - 1) % len(self.opcoes)
            elif evento.key in (pg.K_DOWN, pg.K_s):
                self.selecionada = (self.selecionada + 1) % len(self.opcoes)
            elif evento.key in (pg.K_RETURN, pg.K_SPACE):
                self.confirmar()

    def tratar_digitacao(self, evento):
        """Aplica uma tecla ao nome em edição.

        Parâmetros:
            evento (pygame.event.Event): Evento KEYDOWN do Pygame.
        """
        if evento.key in (pg.K_RETURN, pg.K_KP_ENTER):
            self.nome = limpar_nome(self.nome)
            self.digitando = False

            if self.nome:
                self.selecionada = self.opcoes.index("Jogar")
        elif evento.key == pg.K_BACKSPACE:
            self.nome = self.nome[:-1]
        elif evento.unicode and evento.unicode.isprintable() and evento.unicode != ";":

            if len(self.nome) < LIMITE_NOME:
                self.nome += evento.unicode

        self.aviso = ""    
        
    def confirmar(self):
        """Executa a ação correspondente à opção atualmente selecionada.

        Parâmetros:
            Nenhum (usa `self.opcoes[self.selecionada]`).
        """
        opcao_atual = self.opcoes[self.selecionada]
        if opcao_atual == "Nome":
            self.digitando = True
            self.aviso = ""
        elif opcao_atual == "Jogar":
            if not limpar_nome(self.nome):
                self.selecionada = self.opcoes.index("Nome")
                self.digitando = True
                self.aviso = "Digite um nome para jogar"
                return
            self.game.nome_jogador = limpar_nome(self.nome)
            self.game.iniciar_jogo()
        elif opcao_atual == "Sair do jogo":
            self.game.sair()
        elif opcao_atual == "Guia":                  # NOVO
            self.game.estado = "guia"                # NOVO

    def texto_opcao(self, indice):
        """Monta o texto exibido para uma opção (o campo de nome mostra o valor digitado).

        Parâmetros:
            indice (int): Posição da opção em `self.opcoes`.
        """
        opcao = self.opcoes[indice]
        if opcao != "Nome":
            return opcao
        if self.nome or self.digitando:
            return f"Nome: {self.nome}"
        return "Nome: (Enter para digitar)"

    def draw(self):
        """Desenha o título do jogo, a lista de opções e o aviso na tela.

        Parâmetros:
            Nenhum (desenha diretamente em `self.game.screen`).
        """
        tela = self.game.screen
        largura, altura = tela.get_size()
        tela.fill("black")

        titulo = self.fonte_titulo.render("Try // Except", True, "white")
        tela.blit(titulo, titulo.get_rect(center=(largura // 2, altura // 4)))

        for indice in range(len(self.opcoes)):
            cor = "yellow" if indice == self.selecionada else "gray"
            superficie = self.fonte_opcao.render(self.texto_opcao(indice), True, cor)
            tela.blit(
                superficie,
                superficie.get_rect(center=(largura // 2, altura // 2 + indice * 70)),
            )

        # Aviso (ex.: "Digite um nome para jogar") abaixo da última opção
        if self.aviso:
            y_aviso = altura // 2 + len(self.opcoes) * 70
            aviso_surf = self.fonte_opcao.render(self.aviso, True, "red")
            tela.blit(aviso_surf, aviso_surf.get_rect(center=(largura // 2, y_aviso)))

   