import pygame as pg

class Guia_jogo:
    '''Exibe o guia do jogo (comandos e objetivos) com rolagem de texto'''

    CONTEUDO = [
        ("titulo", "Objetivo:"),
        ("comando", "W", "andar para frente"),
        ("comando", "S", "andar para trás"),
        ("comando", "D", "andar para a direita"),
        ("comando", "A", "andar para a esquerda"),
        ("comando", "Mouse", "mover a câmera"),
        ("comando", "Mouse 1 / E", "interagir com as tarefas"),
        ("texto", "Ache as tarefas pelo mapa e termine-as antes do tempo acabar!"),
        ("texto", "As tarefas não são indicadas, então explore cada canto e use o mouse "
        "para olhar ao redor."),
        ("texto", "Ao chegar perto de uma tarefa, aperte Mouse 1 ou E para interagir com ela."),
        
        ("texto", "O chefe aparece após 30 segundos de jogo ativo. Aproxime-se e pressione F para cumprimentá-lo."),
        ("texto", "Você tem 5 segundos para cumprir a exigência, a até 1,8 célula de distância. Se não cumprir, perde uma chance, sem reiniciar a rodada."),
        ("texto", "Durante uma pergunta, os cronômetros ficam pausados. Depois do encontro, uma nova espera de 30 segundos começa.")]

    def __init__(self, game):
        self.game = game
        self.fonte_titulo = pg.font.SysFont('arial', 64, bold=True)
        self.fonte_secao = pg.font.SysFont('arial', 38, bold=True)
        self.fonte_texto = pg.font.SysFont('arial', 28)
        self.fonte_dica = pg.font.SysFont('arial', 22)
        self.scroll = 0
        self.passo_scroll = 40
        self.montar_layout()

    def quebrar_linhas(self, texto, fonte, largura_max):
        linhas, atual = [], ""
        for palavra in texto.split():
            teste = f"{atual} {palavra}".strip()
            if fonte.size(teste)[0] <= largura_max:
                atual = teste
            else:
                linhas.append(atual)

        if atual:
            linhas.append(atual)
        return linhas

    def montar_layout(self):
        largura, altura = self.game.screen.get_size()
        self.margem = int(largura * 0.10)
        largura_util = largura - 2 * self.margem
        coluna_acao = self.margem + 220

        self.topo = 140
        self.base = altura -50
        self.itens = []
        y = 0

        for item in self.CONTEUDO:
            tipo = item[0]
            if tipo == "titulo":
                y += 18
                surf = self.fonte_secao.render(item[1], True, "yellow")
                self.itens.append((surf, self.margem, y))
                y += surf.get_height() + 10
            elif tipo == "comando":
                tecla = self.fonte_texto.render(item[1], True, "yellow")
                acao = self.fonte_texto.render("- " + item[2], True, "white")
                self.itens.append((tecla, self.margem + 20, y))
                self.itens.append((acao, coluna_acao, y))
                y += tecla.get_height() + 8
            else:
                for linha in self.quebrar_linhas(item[1], self.fonte_texto, largura_util):
                    surf = self.fonte_texto.render(linha, True, "white")
                    self.itens.append((surf, self.margem, y))
                    y += surf.get_height() + 4
                y += 12

        self.altura_conteudo = y
        self.scroll_max = max(0, self.altura_conteudo - (self.base - self.topo))

    def tratar_evento(self, evento):
        if evento.type == pg.KEYDOWN:
            if evento.key in (pg.K_BACKSPACE, pg.K_RETURN):
                self.voltar()
            elif evento.key in (pg.K_DOWN, pg.K_s):
                self.rolar(self.passo_scroll)
            elif evento.type == pg.MOUSEWHEEL:
                self._rolar(-evento.y * self.passo_scroll)

    def rolar(self, delta):
        self.scroll = max(0, min(self.scroll_max, self.scroll + delta))

    def voltar(self):
        """Retorna ao menu principal e reinicia a posição da rolagem.

        Parâmetros:
            Nenhum.
        """
        self.scroll = 0
        self.game.estado = "menu"

    def draw(self):
        tela = self.game.screen
        largura, altura = tela.get_size()
        tela.fill("black")

        titulo = self.fonte_titulo.render("Guia", True, "white")
        tela.blit(titulo, titulo.get_rect(center=(largura // 2, 70)))

        area = pg.Rect(0, self.topo, largura, self.base - self.topo)
        tela.set_clip(area)
        for surf, x, y in self.itens:
            tela.blit(surf, (x, self.topo + y - self.scroll))
        tela.set_clip(None)

        dica = "ESC / Backspace: voltar"
        if self.scroll_max > 0:
            dica += "   |   Setas ou roda do mouse: rolar"
        surf = self.fonte_dica.render(dica, True, "gray")
        tela.blit(surf, surf.get_rect(center=(largura // 2, altura - 25)))
