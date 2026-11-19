import sys
import pygame as pg

if __package__:
    from .settings import *
    from .map import *
    from .player import *
    from .tela_inicial import Tela_inicial
    from .raycasting import RayCasting
else:
    from settings import *
    from map import *
    from player import *
    from tela_inicial import Tela_inicial
    from raycasting import RayCasting


class Game:
    """Classe principal que controla o loop, estados e módulos do jogo."""

    def __init__(self):
        """Inicializa o Pygame, a janela e começa exibindo a tela inicial."""
        pg.init()
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.estado = "menu"  # Controla se estamos no "menu" ou "jogando"
        self.tela_inicial = Tela_inicial(self)

    def new_game(self):
        """Cria uma nova partida instanciando mapa, jogador e raycasting."""
        self.map = Map(self)
        self.player = Player(self)
        self.raycasting = RayCasting(self)

    def iniciar_jogo(self):
        """Inicia uma partida, muda o estado e ativa o controle de câmera pelo mouse."""
        self.new_game()
        self.estado = "jogando"
        pg.mouse.set_visible(False)
        pg.event.set_grab(True)
        pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        pg.mouse.get_rel()  # Zera o deslocamento acumulado antes do 1º frame

    def sair(self):
        """Libera o cursor do mouse, encerra o Pygame e fecha o programa."""
        pg.event.set_grab(False)
        pg.mouse.set_visible(True)
        pg.quit()
        sys.exit()

    def update(self):
        """Atualiza a lógica da partida quando ativa e calcula o delta_time."""
        if self.estado == "jogando":
            self.player.update()
            self.raycasting.update()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps():.1f}')

    def draw(self):
        """Desenha a tela atual (menu ou visão 3D) e atualiza o display."""
        if self.estado == 'menu':
            self.tela_inicial.draw()
        else:
            self.screen.fill('black')
            self.raycasting.draw()
        pg.display.flip()  # Atualiza a janela apenas após todo o desenho do frame

    def check_events(self):
        """Processa eventos de encerramento e repassa teclas ao menu quando ativo."""
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.sair()
            if self.estado == 'menu':
                self.tela_inicial.tratar_evento(event)

    def run(self):
        """Executa o loop principal do jogo indefinidamente até o usuário sair."""
        while True:
            self.check_events()
            self.update()
            self.draw()


def executar_jogo():
    """Cria a instância de Game e inicia o loop principal."""
    game = Game()
    game.run()


if __name__ == '__main__':
    executar_jogo()
