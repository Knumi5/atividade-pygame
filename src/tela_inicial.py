import pygame as pg
import math


class Tela_inicial:
    def __init__(self, game):
        self.game = game
        self.fonte_titulo = pg.font.SysFont('arial', 72, bold=True)
        self.fonte_opcao = pg.font.SysFont('arial', 40)
        self.opcoes = ["Jogar", "Guia", "Consultar rankings", "Sair do jogo"]
        self.selecionada = 0

    def tratar_evento(self, evento):
        '''
        Essa função faz o jogador ter que usar as teclas (w, s) para
        navegar pelas opções da tela inicial e para seleciona-la pressione (space)

        '''
        if evento.type == pg.KEYDOWN:
            if evento.key in (pg.K_UP, pg.K_w):
                self.selecionada = (self.selecionada - 1) % len(self.opcoes)
            elif evento.key in (pg.K_DOWN, pg.K_s):
                    self.selecionada = (self.selecionada + 1) % len(self.opcoes)
            elif evento.key in (pg.K_RETURN, pg.K_SPACE):
                 self.confirmar()

    def confirmar(self):
        if self.opcoes[self.selecionada] == "Jogar":
            # Chama a função de iniciar_jogo() de jogo.py
            self.game.iniciar_jogo()
        elif self.opcoes[self.selecionada] == "Sair do jogo":
             self.game.sair()

    def draw(self):
        tela = self.game.screen
        largura, altura = tela.get_size()
        tela.fill("black")

        titulo = self.fonte_titulo.render("Try // Except", True, "white")
        tela.blit(titulo, titulo.get_rect(center=(largura // 2, altura // 4)))

        for i, texto in enumerate(self.opcoes):
            if i == self.selecionada:
                cor = "yellow"
            else:
                cor = "gray"

            surf = self.fonte_opcao.render(texto, True, cor)
            tela.blit(surf, surf.get_rect(center=(largura // 2, altura // 2 + i * 70)))

         