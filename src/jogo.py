import sys
import random
import math
import pygame as pg

if __package__:
    from .boss import confirma_tempo, spawn_boss, dano_boss
    from .dados import carregar_recorde, salvar_recorde
    from .ranking import salvar_melhor
    from .funcoes import calcular_pontos, jogador_perdeu, tomar_dano
    from .settings import *
    from .map import *
    from .player import *
    from .tela_inicial import Tela_inicial
    from .guia import Guia_jogo          # NOVO
    from .object_renderer import ObjectRenderer
    from .raycasting import RayCasting
else:
    from boss import confirma_tempo, spawn_boss, dano_boss
    from dados import carregar_recorde, salvar_recorde
    from ranking import salvar_melhor
    from settings import *
    from funcoes import calcular_pontos, jogador_perdeu, tomar_dano
    from map import *
    from player import *
    from tela_inicial import Tela_inicial
    from guia import Guia_jogo           # NOVO
    from object_renderer import ObjectRenderer
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
        self.estado = "menu"  # Pode ser "menu", "guia", "jogando" ou "game_over"
        self.tela_inicial = Tela_inicial(self)
        self.fonte_hud = pg.font.SysFont('arial', 24, bold=True)
        self.fonte_hud_destaque = pg.font.SysFont('arial', 32, bold=True)
        self.fonte_gameover = pg.font.SysFont('arial', 72, bold=True)
        self.rodada = 1
        self.chances = CHANCES_INICIAIS
        self.pontos = 0
        self.recorde = carregar_recorde(CAMINHO_RECORDE)
        self.tempo_limite_rodada = TEMPO_INICIAL_RODADA
        self.tempo_restante = TEMPO_INICIAL_RODADA
        self.aviso_chefe = ""
        self.painel_pergunta = None
        self.nome_jogador = ""  # preenchido pela Tela_inicial ao escolher "Jogar"
        self.tela_guia = Guia_jogo(self)      # NOVO
        self.tempo_boss  = 0.0
        self.boss_ativo = False
        self.boss = None
        self.tempo_cumprimento_boss = 0.0
    

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
        self.tempo_boss = 0.0
        self.boss_ativo = False 
        self.boss = None
        self.aviso_chefe = ""
        self.tempo_cumprimento_boss = 0.0
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
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)

    def escolher_posicao_boss(self):
        """Escolhe o centro de uma célula livre ao lado do jogador, ou None."""
        jogador_x, jogador_y = self.player.map_pos
        grade = self.map.mini_map
        candidatas = []

        for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
            x, y = jogador_x + dx, jogador_y + dy
            dentro_do_mapa = 0 <= y < len(grade) and 0 <= x < len(grade[y])
            if dentro_do_mapa and (x, y) not in self.map.world_map:
                candidatas.append((x + 0.5, y + 0.5))

        if not candidatas:
            return None
        return random.choice(candidatas)

    def criar_boss(self):
        """Guarda um único chefe se houver posição livre; informa se criou."""
        if self.estado != "jogando" or self.boss_ativo:
            return False

        posicao = self.escolher_posicao_boss()
        if posicao is None:
            return False

        self.boss = spawn_boss(posicao)
        self.boss_ativo = True
        self.tempo_cumprimento_boss = PRAZO_CUMPRIMENTO_BOSS
        self.atualizar_aviso_boss()
        return True

    def atualizar_aviso_boss(self):
        """Mostra o comando e o prazo restantes do encontro ativo."""
        if not self.boss_ativo:
            self.aviso_chefe = ""
            return
        tecla = pg.key.name(TECLA_CUMPRIMENTO_BOSS).upper()
        self.aviso_chefe = (
            f"Chefe: {tecla} para cumprimentar | "
            f"{self.tempo_cumprimento_boss:.1f}s"
        )

    def encerrar_encontro_boss(self):
        """Resolve o encontro e rearma os 30 segundos de espera."""
        if self.boss is not None:
            self.boss["ativo"] = False
        self.boss = None
        self.boss_ativo = False
        self.tempo_cumprimento_boss = 0.0
        self.tempo_boss = 0.0
        self.aviso_chefe = ""

    def cumprimentar_boss(self):
        """Aceita o cumprimento somente durante um encontro válido e próximo."""
        if (self.estado != "jogando" or self.painel_pergunta is not None
                or not self.boss_ativo or self.boss is None
                or self.tempo_cumprimento_boss <= 0):
            return False
        distancia = math.hypot(
            self.player.x - self.boss["x"], self.player.y - self.boss["y"]
        )
        if distancia > ALCANCE_CUMPRIMENTO_BOSS + 1e-9:
            return False
        self.encerrar_encontro_boss()
        return True

    def atualizar_boss(self, segundos):
        """Conta apenas o tempo de jogo ativo e consulta a regra de aparição."""
        if self.estado != "jogando" or self.painel_pergunta is not None:
            return False
        if self.boss_ativo:
            self.tempo_cumprimento_boss = max(
                0.0, self.tempo_cumprimento_boss - segundos
            )
            if self.tempo_cumprimento_boss <= 1e-9:
                # Resolve antes de descontar para impedir punição em outro quadro.
                self.encerrar_encontro_boss()
                dano_boss(self, PENALIDADE_BOSS)
            else:
                self.atualizar_aviso_boss()
            return False
        self.tempo_boss += segundos
        if confirma_tempo(self.tempo_boss, self.boss_ativo):
            return self.criar_boss()
        return False

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

    def perder_chance(self, quantidade=1, reiniciar_rodada=True):
        """Desconta chances do jogador e verifica se houve Game Over ou nova tentativa.

        Parâmetros:
            quantidade (int, opcional): Quantidade de chances perdidas (padrão: 1).
            reiniciar_rodada (bool): False para penalidade do chefe; mantém mapa e tarefas.
        """
        self.chances = tomar_dano(self.chances, quantidade)
        if jogador_perdeu(self.chances):
            self.encerrar_partida()
        elif reiniciar_rodada:
            # Ao estourar o tempo mas ainda ter chances, sorteia novo layout e reseta o tempo
            if self.boss_ativo:
                self.encerrar_encontro_boss()
            self.trocar_mapa("aleatorio")

    def encerrar_partida(self):
        """Salva o recorde e a melhor pontuação do jogador, libera o cursor e abre o Game Over

        Parâmetros:
            Nenhum.
        """
        self.encerrar_encontro_boss()
        self.painel_pergunta = None
        if self.pontos > self.recorde:
            self.recorde = self.pontos
            salvar_recorde(CAMINHO_RECORDE, self.recorde)
        # Grava no ranking.txt apenas se for a melhor pontuação deste jogador
        salvar_melhor(self.nome_jogador, self.pontos)
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
        if self.estado == "jogando" and self.painel_pergunta is None:
            self.player.update()
            self.raycasting.update()
            self.tempo_restante = max(0.0, self.tempo_restante - self.delta_time / 1000.0)
            if self.tempo_restante <= 0:
                self.perder_chance(1)
            else:
                self.atualizar_boss(self.delta_time / 1000.0)
            titulo_janela = (
                f'Rodada {self.rodada} ({self.map.nome_exibicao}) '
                f'| FPS: {self.clock.get_fps():.1f}'
            )
        else:
            titulo_janela = f'Try // Except | FPS: {self.clock.get_fps():.1f}'
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(titulo_janela)

    def _desenhar_caixa_hud(self, superficies, pos_x, pos_y, espacamento=8, alinhar_direita=False):
        """Desenha um bloco semitransparente para manter os textos da HUD legíveis.

        Parâmetros:
            superficies (list[pygame.Surface]): Textos já renderizados que compõem o bloco.
            pos_x (int): Coordenada X de referência (borda esquerda ou direita).
            pos_y (int): Coordenada Y do topo do bloco.
            espacamento (int, opcional): Espaço vertical em pixels entre linhas (padrão: 8).
            alinhar_direita (bool, opcional): Se True, usa `pos_x` como borda direita.
        """
        padding_x, padding_y = 14, 10
        largura_bloco = max(s.get_width() for s in superficies) + 2 * padding_x
        altura_bloco = (
            sum(s.get_height() for s in superficies)
            + espacamento * max(0, len(superficies) - 1)
            + 2 * padding_y
        )
        x_caixa = pos_x - largura_bloco if alinhar_direita else pos_x

        fundo = pg.Surface((largura_bloco, altura_bloco), pg.SRCALPHA)
        fundo.fill((0, 0, 0, 175))
        self.screen.blit(fundo, (x_caixa, pos_y))

        cursor_y = pos_y + padding_y
        for surf in superficies:
            self.screen.blit(surf, (x_caixa + padding_x, cursor_y))
            cursor_y += surf.get_height() + espacamento

    def desenhar_hud(self):
        """Desenha os indicadores separados da HUD (pontos, tarefas, chances e tempo).

        Também reserva o espaço central superior para avisos do chefe e o centro da tela
        para o painel de pergunta quando ativo.

        Parâmetros:
            Nenhum (usa `self.screen` e as fontes da HUD).
        """
        concluidas = self.map.total_tarefas - len(self.map.tarefas_pendentes)
        cor_chances = "red" if self.chances <= 1 else "yellow"
        cor_tempo = "red" if self.tempo_restante <= 10 else "white"

        # Bloco esquerdo: rodada, pontuação, recorde, tarefas e chances separados
        bloco_esquerdo = [
            self.fonte_hud.render(
                f"Rodada: {self.rodada}   |   Pontos: {self.pontos}   |   Recorde: {self.recorde}",
                True,
                "white",
            ),
            self.fonte_hud.render(
                f"Tarefas: {concluidas}/{self.map.total_tarefas}   |   Chances: {self.chances}/{CHANCES_INICIAIS}",
                True,
                cor_chances if self.chances <= 1 else "cyan",
            ),
        ]
        self._desenhar_caixa_hud(bloco_esquerdo, 20, 16)

        # Bloco direito: cronômetro da rodada destacado e separado
        tempo_surf = self.fonte_hud_destaque.render(
            f"Tempo: {self.tempo_restante:04.1f}s",
            True,
            cor_tempo,
        )
        self._desenhar_caixa_hud([tempo_surf], WIDTH - 20, 16, alinhar_direita=True)

        # Espaço previsto para avisos do chefe (abaixo da barra superior) e painel de pergunta
        if self.aviso_chefe:
            aviso_surf = self.fonte_hud_destaque.render(self.aviso_chefe, True, "orange")
            caixa_aviso = pg.Surface(
                (aviso_surf.get_width() + 28, aviso_surf.get_height() + 16),
                pg.SRCALPHA,
            )
            caixa_aviso.fill((0, 0, 0, 190))
            rect_aviso = caixa_aviso.get_rect(midtop=(HALF_WIDTH, 115))
            self.screen.blit(caixa_aviso, rect_aviso)
            self.screen.blit(aviso_surf, aviso_surf.get_rect(center=rect_aviso.center))

        if self.painel_pergunta is not None:
            self.desenhar_painel_pergunta()

    def desenhar_painel_pergunta(self):
        """Desenha o painel central reservado para as perguntas das tarefas.

        Parâmetros:
            Nenhum (lê `self.painel_pergunta` quando preenchido pelo módulo de missões).
        """
        largura_painel, altura_painel = 860, 320
        painel = pg.Surface((largura_painel, altura_painel), pg.SRCALPHA)
        painel.fill((15, 15, 25, 230))
        rect = painel.get_rect(center=(HALF_WIDTH, HALF_HEIGHT))
        self.screen.blit(painel, rect)
        pg.draw.rect(self.screen, "white", rect, 2)

        texto = self.fonte_hud.render(str(self.painel_pergunta), True, "white")
        self.screen.blit(texto, texto.get_rect(center=rect.center))

    def desenhar_game_over(self):
        """Desenha a tela de fim de jogo com pontuação final e opção de voltar ao menu.

        Parâmetros:
            Nenhum (usa `self.screen`).
        """
        self.screen.fill("black")
        titulo = self.fonte_gameover.render("GAME OVER", True, "red")
        resumo = self.fonte_hud_destaque.render(
            f"Rodada alcançada: {self.rodada} | Pontos: {self.pontos} | Recorde: {self.recorde}",
            True,
            "white",
        )
        instrucao = self.fonte_hud.render(
            "Pressione ENTER ou ESPAÇO para voltar ao menu",
            True,
            "gray",
        )
        self.screen.blit(titulo, titulo.get_rect(center=(HALF_WIDTH, HALF_HEIGHT - 90)))
        self.screen.blit(resumo, resumo.get_rect(center=(HALF_WIDTH, HALF_HEIGHT)))
        self.screen.blit(instrucao, instrucao.get_rect(center=(HALF_WIDTH, HALF_HEIGHT + 70)))

    def draw(self):
        """Desenha a tela atual (menu, guia ou visão 3D) e atualiza o display.

        Parâmetros:
            Nenhum.
        """
        if self.estado == "menu":
            self.tela_inicial.draw()
        elif self.estado == 'game_over':
            self.desenhar_game_over()
        elif self.estado == "guia":           # NOVO
            self.tela_guia.draw()             # NOVO
        else:
            self.object_renderer.draw()
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
            if event.type == pg.QUIT:
                self.sair()
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                if self.estado == "guia":
                    self.tela_guia.voltar()
                elif self.estado == "menu" and self.tela_inicial.digitando:
                    self.tela_inicial.digitando = False  # ESC cancela só a edição do nome
                else:
                    self.sair()
            elif self.estado == 'menu':
                self.tela_inicial.tratar_evento(event)
            elif self.estado == 'guia':
                self.tela_guia.tratar_evento(event)
            elif self.estado == 'game_over':
                if event.type == pg.KEYDOWN and event.key in (pg.K_RETURN, pg.K_SPACE):
                    self.estado = "menu"
            elif self.estado == 'jogando':
                if (event.type == pg.KEYDOWN and event.key == TECLA_CUMPRIMENTO_BOSS
                        and self.cumprimentar_boss()):
                    continue  # O evento de cumprimento já foi consumido.
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
                        self.trocar_mapa("aleatorio")                        # NOVO

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
