import sys
import pygame as pg

if __package__:
    from .dados import carregar_recorde, salvar_recorde
    from .funcoes import calcular_pontos, jogador_perdeu, tomar_dano
    from .settings import *
    from .map import *
    from .player import *
    from .tela_inicial import Tela_inicial
    from .raycasting import RayCasting
else:
    from dados import carregar_recorde, salvar_recorde
    from funcoes import calcular_pontos, jogador_perdeu, tomar_dano
    from settings import *
    from map import *
    from player import *
    from tela_inicial import Tela_inicial
    from raycasting import RayCasting


class Game:
    """Classe principal que controla o loop, estados, rodadas infinitas e módulos do jogo.

    Parâmetros (no construtor):
        Nenhum.
    """

    def __init__(self):
        """Inicializa o Pygame, a janela, as fontes de HUD e começa na tela inicial.

        Parâmetros:
            Nenhum.
        """
        pg.init()
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.estado = "menu"  # Pode ser "menu", "jogando" ou "game_over"
        self.tela_inicial = Tela_inicial(self)
        self.fonte_hud = pg.font.SysFont('arial', 26, bold=True)
        self.fonte_gameover = pg.font.SysFont('arial', 64, bold=True)

        self.rodada = 1
        self.chances = CHANCES_INICIAIS
        self.pontos = 0
        self.recorde = carregar_recorde(CAMINHO_RECORDE)
        self.tempo_limite_rodada = TEMPO_INICIAL_RODADA
        self.tempo_restante = TEMPO_INICIAL_RODADA

    def new_game(self, nome_mapa="aleatorio"):
        """Reinicia os dados da partida (rodada 1, 5 chances, 0 pontos) e abre a 1ª rodada.

        Parâmetros:
            nome_mapa (str, opcional): Chave do layout em `MAPAS` ou `"aleatorio"`
                (padrão: `"aleatorio"`).
        """
        self.rodada = 1
        self.chances = CHANCES_INICIAIS
        self.pontos = 0
        self.recorde = carregar_recorde(CAMINHO_RECORDE)
        self.map = None
        self.iniciar_rodada(nome_mapa)

    def iniciar_rodada(self, nome_mapa="aleatorio"):
        """Carrega um layout (aleatório por padrão), reposiciona o jogador e ajusta o tempo.

        Parâmetros:
            nome_mapa (str, opcional): Chave do layout em `MAPAS` ou `"aleatorio"`.
        """
        # Reduz o tempo disponível a cada rodada concluída até o limite mínimo
        self.tempo_limite_rodada = max(
            TEMPO_MINIMO_RODADA,
            TEMPO_INICIAL_RODADA - (self.rodada - 1) * REDUCAO_TEMPO_RODADA,
        )
        self.tempo_restante = self.tempo_limite_rodada

        if self.map is None:
            self.map = Map(self, nome_mapa, qtd_tarefas=TAREFAS_POR_RODADA)
        else:
            self.map.carregar_mapa(nome_mapa, qtd_tarefas=TAREFAS_POR_RODADA)

        self.player = Player(self)
        self.raycasting = RayCasting(self)

    def iniciar_jogo(self, nome_mapa="aleatorio"):
        """Inicia uma partida a partir do menu e ativa o controle de câmera pelo mouse.

        Parâmetros:
            nome_mapa (str, opcional): Identificador do layout inicial ou `"aleatorio"`.
        """
        self.new_game(nome_mapa)
        self.estado = "jogando"
        pg.mouse.set_visible(False)
        pg.event.set_grab(True)
        pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        pg.mouse.get_rel()  # Zera o deslocamento acumulado antes do 1º frame

    def trocar_mapa(self, nome_mapa):
        """Troca imediatamente para outro layout do cenário sem perder a rodada atual.

        Parâmetros:
            nome_mapa (str): Chave do layout desejado em `MAPAS` ou `"aleatorio"`.
        """
        self.iniciar_rodada(nome_mapa)
        pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        pg.mouse.get_rel()

    def perder_chance(self, quantidade=1):
        """Desconta chances do jogador e verifica se houve Game Over ou nova tentativa.

        Parâmetros:
            quantidade (int, opcional): Quantidade de chances perdidas (padrão: 1).
        """
        self.chances = tomar_dano(self.chances, quantidade)
        if jogador_perdeu(self.chances):
            self.encerrar_partida()
        else:
            # Ao estourar o tempo mas ainda ter chances, sorteia novo layout e reseta o tempo
            self.trocar_mapa("aleatorio")

    def encerrar_partida(self):
        """Salva o recorde se superado, libera o cursor e entra na tela de Game Over.

        Parâmetros:
            Nenhum.
        """
        if self.pontos > self.recorde:
            self.recorde = self.pontos
            salvar_recorde(CAMINHO_RECORDE, self.recorde)
        self.estado = "game_over"
        pg.event.set_grab(False)
        pg.mouse.set_visible(True)

    def sair(self):
        """Libera o cursor do mouse, encerra o Pygame e fecha o programa.

        Parâmetros:
            Nenhum.
        """
        pg.event.set_grab(False)
        pg.mouse.set_visible(True)
        pg.quit()
        sys.exit()

    def update(self):
        """Atualiza jogador, raycasting e cronômetro da rodada quando em `"jogando"`.

        Parâmetros:
            Nenhum.
        """
        if self.estado == "jogando":
            self.player.update()
            self.raycasting.update()
            self.tempo_restante = max(0.0, self.tempo_restante - self.delta_time / 1000.0)
            if self.tempo_restante <= 0:
                self.perder_chance(1)
            titulo_janela = (
                f'Rodada {self.rodada} ({self.map.nome_exibicao}) '
                f'| FPS: {self.clock.get_fps():.1f}'
            )
        else:
            titulo_janela = f'Try // Except | FPS: {self.clock.get_fps():.1f}'
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(titulo_janela)

    def desenhar_hud(self):
        """Desenha as informações da rodada (rodada, tarefas, tempo, chances e pontuação).

        Parâmetros:
            Nenhum (usa `self.screen` e `self.fonte_hud`).
        """
        concluidas = self.map.total_tarefas - len(self.map.tarefas_pendentes)
        cor_tempo = "red" if self.tempo_restante <= 10 else "white"
        linhas = [
            (f"Rodada: {self.rodada} | Pontos: {self.pontos} | Recorde: {self.recorde}", "white"),
            (f"Tarefas: {concluidas}/{self.map.total_tarefas} | Chances: {self.chances}/{CHANCES_INICIAIS}", "yellow"),
            (f"Tempo: {self.tempo_restante:.1f}s", cor_tempo),
        ]
        for indice, (texto, cor) in enumerate(linhas):
            surf = self.fonte_hud.render(texto, True, cor)
            self.screen.blit(surf, (20, 15 + indice * 30))

    def desenhar_game_over(self):
        """Desenha a tela de fim de jogo com pontuação final e opção de voltar ao menu.

        Parâmetros:
            Nenhum (usa `self.screen`).
        """
        self.screen.fill("black")
        titulo = self.fonte_gameover.render("GAME OVER", True, "red")
        resumo = self.fonte_hud.render(
            f"Rodada alcançada: {self.rodada} | Pontos: {self.pontos} | Recorde: {self.recorde}",
            True,
            "white",
        )
        instrucao = self.fonte_hud.render(
            "Pressione ENTER ou ESPAÇO para voltar ao menu",
            True,
            "gray",
        )
        self.screen.blit(titulo, titulo.get_rect(center=(HALF_WIDTH, HALF_HEIGHT - 80)))
        self.screen.blit(resumo, resumo.get_rect(center=(HALF_WIDTH, HALF_HEIGHT)))
        self.screen.blit(instrucao, instrucao.get_rect(center=(HALF_WIDTH, HALF_HEIGHT + 60)))

    def draw(self):
        """Desenha a tela atual (menu, visão 3D + HUD ou game over) e atualiza o display.

        Parâmetros:
            Nenhum.
        """
        if self.estado == 'menu':
            self.tela_inicial.draw()
        elif self.estado == 'game_over':
            self.desenhar_game_over()
        else:
            self.screen.fill('black')
            self.raycasting.draw()
            self.desenhar_hud()
        pg.display.flip()  # Atualiza a janela apenas após todo o desenho do frame

    def check_events(self):
        """Processa eventos de encerramento, menu, game over e interação com tarefas.

        Parâmetros:
            Nenhum.
        """
        teclas_mapas = {
            pg.K_1: ORDEM_MAPAS[0],
            pg.K_2: ORDEM_MAPAS[1],
            pg.K_3: ORDEM_MAPAS[2],
            pg.K_4: ORDEM_MAPAS[3],
            pg.K_5: ORDEM_MAPAS[4],
        }
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.sair()
            if self.estado == 'menu':
                self.tela_inicial.tratar_evento(event)
            elif self.estado == 'game_over':
                if event.type == pg.KEYDOWN and event.key in (pg.K_RETURN, pg.K_SPACE):
                    self.estado = "menu"
            elif self.estado == 'jogando':
                interagiu = (
                    (event.type == pg.MOUSEBUTTONDOWN and event.button == 1)
                    or (event.type == pg.KEYDOWN and event.key == pg.K_e)
                )
                if interagiu and self.player.interagir_tarefa():
                    self.pontos = calcular_pontos(self.pontos, 1)
                    # Ao concluir todas as tarefas, avança a rodada e sorteia outro layout
                    if not self.map.tarefas_pendentes:
                        self.rodada += 1
                        self.trocar_mapa("aleatorio")
                elif event.type == pg.KEYDOWN:
                    if event.key in teclas_mapas:
                        self.trocar_mapa(teclas_mapas[event.key])
                    elif event.key == pg.K_m:
                        self.trocar_mapa("aleatorio")

    def run(self):
        """Executa o loop principal do jogo indefinidamente até o usuário sair.

        Parâmetros:
            Nenhum.
        """
        while True:
            self.check_events()
            self.update()
            self.draw()


def executar_jogo():
    """Cria a instância de `Game` e inicia o loop principal.

    Parâmetros:
        Nenhum.
    """
    game = Game()
    game.run()


if __name__ == '__main__':
    executar_jogo()
