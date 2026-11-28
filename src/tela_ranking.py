
import pygame as pg

if __package__:
    from .ranking import melhores
    from .settings import WIDTH, HEIGHT
else:
    from ranking import melhores
    from settings import WIDTH, HEIGHT


class Tela_Ranking:

    def __init__(self, game):
        self.game = game
        self.fonte_titulo = pg.font.SysFont("arial", 55, bold=True)
        self.fonte_item = pg.font.SysFont("arial", 30, bold=True)
        self.fonte_instrucao = pg.font.SysFont("arial", 22)

    def draw(self):
        screen = self.game.screen
        screen.fill((15, 25, 20))

        titulo = self.fonte_titulo.render(
            "RANKING",
            True,
            (255, 215, 0)
        )
        screen.blit(
            titulo,
            titulo.get_rect(center=(WIDTH // 2, 90))
        )

        """ Cabeçalho """
        cabecalho = self.fonte_item.render(
            "POS.       JOGADOR             PONTOS",
            True,
            (100, 220, 130)
        )
        screen.blit(
            cabecalho,
            cabecalho.get_rect(center=(WIDTH // 2, 180))
        )

        """ Carrega os 10 melhores jogadores """
        jogadores = melhores(10)

        if not jogadores:
            texto = self.fonte_item.render(
                "Nenhuma pontuação registrada ainda!",
                True,
                "white"
            )
            screen.blit(
                texto,
                texto.get_rect(center=(WIDTH // 2, 300))
            )

        else:
            for i, (nome, pontos) in enumerate(jogadores):
                y = 240 + i * 55

                if i == 0:
                    cor = (255, 215, 0)
                elif i == 1:
                    cor = (192, 192, 192)
                elif i == 2:
                    cor = (205, 127, 50)
                else:
                    cor = (255, 255, 255)

                texto = self.fonte_item.render(
                    f"{i + 1:02d}          {nome:<12}          {pontos}",
                    True,
                    cor
                )

                screen.blit(
                    texto,
                    texto.get_rect(center=(WIDTH // 2, y))
                )

        instrucao = self.fonte_instrucao.render(
            "Pressione ESC para voltar",
            True,
            (180, 180, 180)
        )

        screen.blit(
            instrucao,
            instrucao.get_rect(center=(WIDTH // 2, HEIGHT - 60))
        )

        pg.display.flip()

    def tratar_evento(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.game.estado = "menu"
