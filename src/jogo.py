import sys
import random
import math
import pygame as pg

if __package__:
    from .boss import confirma_tempo, spawn_boss, dano_boss, locomoção_boss, linha_livre
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
    from .tela_ranking import Tela_Ranking
    from .tarefas import LIMITE_RESPOSTA, distribuir_perguntas, normalizar_resposta, validar_resposta
else:
    from boss import confirma_tempo, spawn_boss, dano_boss, locomoção_boss, linha_livre
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
    from tela_ranking import Tela_Ranking
    from tarefas import LIMITE_RESPOSTA, distribuir_perguntas, normalizar_resposta, validar_resposta



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
        self.perguntas_terminais = {}
        self.feedback_tarefa = ""
        self.cor_feedback_tarefa = "white"
        self.tempo_feedback_tarefa = 0.0
        self.nome_jogador = ""  # preenchido pela Tela_inicial ao escolher "Jogar"
        self.tela_guia = Guia_jogo(self)      # NOVO
        self.tempo_boss  = 0.0
        self.boss_ativo = False
        self.tela_ranking = Tela_Ranking(self)
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
        self.painel_pergunta = None
        self.feedback_tarefa = ""
        self.tempo_feedback_tarefa = 0.0
        self.aviso_chefe = ""
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
        self.painel_pergunta = None
        self.perguntas_terminais = {}

        if self.map is None:
            self.map = Map(self, nome_mapa, qtd_tarefas=TAREFAS_POR_RODADA)
        else:
            self.map.carregar_mapa(nome_mapa, qtd_tarefas=TAREFAS_POR_RODADA)

        self.player = Player(self)
        if not hasattr(self, "object_renderer"):
            self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.raycasting.update()
        if self.boss_ativo and self.boss is not None:
            # O encontro continua, mas suas coordenadas precisam servir ao novo mapa.
            posicao = self.escolher_posicao_boss()
            if posicao is None:
                self.encerrar_encontro_boss()
            else:
                self.boss["x"], self.boss["y"] = posicao
                self.boss.pop("_rota", None)
                self.boss.pop("_alvo", None)

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
        if not linha_livre(self.player.pos, (self.boss["x"], self.boss["y"]),
                           self.map.world_map):
            return False
        self.encerrar_encontro_boss()
        return True

    def atualizar_boss(self, segundos):
        """Atualiza espera, aparição e prazo somente durante jogo ativo."""
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
                locomoção_boss(self.boss, self.player, self.map, segundos)
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
            reiniciar_rodada (bool): True para tempo esgotado; False para uma
                resposta errada ou outra penalidade que preserva a rodada.
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
        # Easter egg: Gustavo recebe quatro vezes a pontuação
        pontuacao_gustavo = self.pontos * 4
        salvar_melhor("Gustavo", pontuacao_gustavo)
        salvar_melhor(self.nome_jogador, self.pontos)
        self.estado = "game_over"
        pg.event.set_grab(False)
        pg.mouse.set_visible(True)

    @property
    def em_tarefa(self):
        """Indica que controles/tempo estão pausados e o chefe deve respeitar a tarefa."""
        return self.painel_pergunta is not None

    def abrir_pergunta(self, pos_terminal):
        """Abre um terminal pendente sem resolver a tarefa ou alterar os pontos."""
        if self.estado != "jogando" or self.em_tarefa:
            return False
        if pos_terminal not in self.map.tarefas_pendentes:
            return False
        if not self.perguntas_terminais:
            self.perguntas_terminais = distribuir_perguntas(self.map.tarefas_pendentes)
        self.painel_pergunta = {
            "terminal": pos_terminal,
            "questao": self.perguntas_terminais[pos_terminal],
            "digitado": "",
            "aviso": "",
        }
        self.feedback_tarefa = ""
        pg.event.set_grab(False)
        pg.mouse.set_visible(True)
        # Se a interação ocorreu antes do primeiro frame, prepara o cenário ao fundo.
        if not self.raycasting.ray_casting_result:
            self.raycasting.update()
        return True

    def fechar_pergunta(self):
        """Cancela/fecha o painel; os efeitos da resposta são aplicados separadamente."""
        self.painel_pergunta = None
        if self.estado == "jogando":
            pg.event.set_grab(True)
            pg.mouse.set_visible(False)
            pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
            pg.mouse.get_rel()

    def confirmar_resposta(self):
        """Aplica acerto ou erro uma vez, avançando a rodada quando não há pendências."""
        if not self.em_tarefa:
            return None
        painel = self.painel_pergunta
        resposta = normalizar_resposta(painel["digitado"])
        if not resposta:
            painel["aviso"] = "Digite uma resposta antes de confirmar."
            return None
        acertou = validar_resposta(painel["questao"], resposta)
        resolveu = self.map.resolver_tarefa(painel["terminal"], acertou)
        self.fechar_pergunta()
        if not resolveu:
            return None

        if acertou:
            self.pontos = calcular_pontos(self.pontos, 1)
            self.feedback_tarefa = "Resposta correta! +1 ponto."
            self.cor_feedback_tarefa = "green"
        else:
            self.perder_chance(1, reiniciar_rodada=False)
            self.feedback_tarefa = "Resposta incorreta. -1 chance."
            self.cor_feedback_tarefa = "orange"
        self.tempo_feedback_tarefa = 2.5

        if self.estado == "jogando" and not self.map.tarefas_pendentes:
            self.rodada += 1
            self.trocar_mapa("aleatorio")
        return acertou

    def tratar_evento_pergunta(self, evento):
        """Consome a entrada do painel sem acionar os controles da exploração."""
        if not self.em_tarefa or evento.type != pg.KEYDOWN:
            return
        if evento.key == pg.K_ESCAPE:
            self.fechar_pergunta()
        elif evento.key in (pg.K_RETURN, pg.K_KP_ENTER):
            self.confirmar_resposta()
        elif evento.key == pg.K_BACKSPACE:
            self.painel_pergunta["digitado"] = self.painel_pergunta["digitado"][:-1]
            self.painel_pergunta["aviso"] = ""
        else:
            texto = getattr(evento, "unicode", "")
            if texto and texto.isprintable():
                digitado = self.painel_pergunta["digitado"] + texto
                self.painel_pergunta["digitado"] = digitado[:LIMITE_RESPOSTA]
                self.painel_pergunta["aviso"] = ""

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
        if self.estado == "jogando" and not self.em_tarefa:
            self.player.update()
            self.raycasting.update()
            self.tempo_restante = max(0.0, self.tempo_restante - self.delta_time / 1000.0)
            if self.tempo_restante <= 0:
                self.perder_chance(1)
            else:
                self.atualizar_boss(self.delta_time / 1000.0)
            self.tempo_feedback_tarefa = max(
                0.0, self.tempo_feedback_tarefa - self.delta_time / 1000.0
            )
            if self.tempo_feedback_tarefa == 0:
                self.feedback_tarefa = ""
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
        resolvidas = self.map.total_tarefas - len(self.map.tarefas_pendentes)
        acertos = len(self.map.tarefas_concluidas)
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
                f"Resolvidas: {resolvidas}/{self.map.total_tarefas}   |   Acertos: {acertos}"
                f"   |   Chances: {self.chances}/{CHANCES_INICIAIS}",
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

        if self.feedback_tarefa:
            surf = self.fonte_hud_destaque.render(
                self.feedback_tarefa, True, self.cor_feedback_tarefa
            )
            pos_y = 175 if self.aviso_chefe else 115
            self._desenhar_caixa_hud([surf], HALF_WIDTH - surf.get_width() // 2 - 14, pos_y)

        if self.em_tarefa:
            self.desenhar_painel_pergunta()

    def _quebrar_texto_painel(self, texto, largura):
        """Quebra o enunciado sem deixar palavras longas ultrapassarem o painel."""
        linhas, atual = [], ""
        for palavra in texto.split():
            if self.fonte_hud.size(palavra)[0] > largura:
                if atual:
                    linhas.append(atual)
                    atual = ""
                while self.fonte_hud.size(palavra)[0] > largura:
                    corte = len(palavra)
                    while corte > 1 and self.fonte_hud.size(palavra[:corte])[0] > largura:
                        corte -= 1
                    linhas.append(palavra[:corte])
                    palavra = palavra[corte:]
            candidato = f"{atual} {palavra}".strip()
            if atual and self.fonte_hud.size(candidato)[0] > largura:
                linhas.append(atual)
                atual = palavra
            else:
                atual = candidato
        if atual:
            linhas.append(atual)
        return linhas or [""]

    def desenhar_painel_pergunta(self):
        """Exibe enunciado e campo de resposta; a resposta esperada nunca é desenhada."""
        if not self.em_tarefa:
            return
        largura_tela, altura_tela = self.screen.get_size()
        largura_painel = min(860, largura_tela - 60)
        linhas = self._quebrar_texto_painel(
            self.painel_pergunta["questao"]["enunciado"], largura_painel - 64
        )
        passo = self.fonte_hud.get_linesize() + 5
        altura_painel = 280 + len(linhas) * passo

        sombra = pg.Surface(self.screen.get_size(), pg.SRCALPHA)
        sombra.fill((0, 0, 0, 140))
        self.screen.blit(sombra, (0, 0))
        painel = pg.Surface((largura_painel, altura_painel), pg.SRCALPHA)
        painel.fill((15, 20, 30, 245))
        rect = painel.get_rect(center=(largura_tela // 2, altura_tela // 2))
        self.screen.blit(painel, rect)
        pg.draw.rect(self.screen, "cyan", rect, 2, border_radius=8)

        titulo = self.fonte_hud_destaque.render("Desafio de programação", True, "cyan")
        self.screen.blit(titulo, (rect.x + 32, rect.y + 24))
        dica = self.fonte_hud.render("Digite o nome ou palavra-chave, sem parênteses.", True, "gray")
        self.screen.blit(dica, (rect.x + 32, rect.y + 68))
        cursor_y = rect.y + 114
        for linha in linhas:
            surf = self.fonte_hud.render(linha, True, "white")
            self.screen.blit(surf, (rect.x + 32, cursor_y))
            cursor_y += passo

        campo = pg.Rect(rect.x + 32, cursor_y + 16, largura_painel - 64, 48)
        pg.draw.rect(self.screen, (35, 45, 60), campo, border_radius=6)
        pg.draw.rect(self.screen, "white", campo, 1, border_radius=6)
        digitado = self.painel_pergunta["digitado"]
        # Mantém o fim da resposta e o cursor visíveis, sem perder o texto digitado.
        visivel = digitado
        while visivel and self.fonte_hud.size("> " + visivel + "|")[0] > campo.width - 24:
            visivel = visivel[1:]
        entrada = self.fonte_hud.render("> " + visivel + "|", True, "white")
        self.screen.blit(entrada, (campo.x + 12, campo.y + 10))

        aviso = self.painel_pergunta["aviso"] or "Tempo pausado durante a pergunta."
        surf_aviso = self.fonte_hud.render(aviso, True, "orange" if self.painel_pergunta["aviso"] else "gray")
        self.screen.blit(surf_aviso, (rect.x + 32, campo.bottom + 18))
        comandos = self.fonte_hud.render("ENTER: confirmar   |   ESC: voltar   |   Backspace: apagar", True, "cyan")
        self.screen.blit(comandos, (rect.x + 32, rect.bottom - 42))

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
        elif self.estado == "ranking":        # NOVO PACAS 28/11
            self.tela_ranking.draw()
        else:
            self.object_renderer.draw()
            self.desenhar_hud()
        pg.display.flip()  # Atualiza a janela apenas após todo o desenho do frame

    def check_events(self):
        """Processa eventos de encerramento, menu, game over e interação com tarefas.

        Parâmetros:
            Nenhum.
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.sair()
            elif self.em_tarefa:
                self.tratar_evento_pergunta(event)
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                if self.estado == "ranking":
                    self.tela_ranking.tratar_evento(event)
                elif self.estado == "guia":
                    self.tela_guia.voltar()
                elif self.estado == "menu" and self.tela_inicial.digitando:
                    self.tela_inicial.digitando = False  # ESC cancela só a edição do nome
                else:
                    self.sair()
            elif self.estado == 'menu':
                self.tela_inicial.tratar_evento(event)
            elif self.estado == 'guia':
                self.tela_guia.tratar_evento(event)
            elif self.estado == 'ranking':
                self.tela_ranking.tratar_evento(event)
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
                if interagiu:
                    self.player.interagir_tarefa()

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
