import pygame as pg
import sys
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
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.estado = "menu" # menu ou jogando
        self.tela_inicial = Tela_inicial(self) 
        # self.new_game() --> sai daqui: só roda quando clicar em Jogar  
        # a função "iniciar_jogo()" inicia o jogo 

    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)
        self.raycasting = RayCasting(self)

    def iniciar_jogo(self):
        self.new_game()
        self.estado = "jogando"
        pg.mouse.set_visible(False)
        pg.event.set_grab(True)
        pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        pg.mouse.get_rel()

    def sair(self):
        pg.event.set_grab(False)
        pg.mouse.set_visible(True)
        pg.quit()
        sys.exit()

    def update(self):
        if self.estado == "jogando":
            self.player.update()
            self.raycasting.update()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps():.1f}')

    def draw(self):
        if self.estado == 'menu':
            self.tela_inicial.draw()
        else:
            self.screen.fill('black')
            self.raycasting.draw()
        pg.display.flip()   # flip depois de desenhar
        
    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.sair()
            if self.estado == 'menu':
                self.tela_inicial.tratar_evento(event)

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()

def executar_jogo():
    game = Game()
    game.run()


if __name__ == '__main__':
    executar_jogo()