"""Critérios de R06-R09, preparados antes da implementação."""
import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

import copy
import math
from pathlib import Path
from types import SimpleNamespace

import pygame as pg
import pytest


@pytest.fixture
def final_game(tmp_path, monkeypatch):
    from src import jogo, ranking
    monkeypatch.setattr(jogo, "CAMINHO_RECORDE", str(tmp_path / "recorde.txt"))
    monkeypatch.setattr(ranking, "ARQUIVO", str(tmp_path / "ranking.txt"))
    game = jogo.Game()
    game.nome_jogador = "Teste Final"
    game.iniciar_jogo("layout_1")
    game.tempo_restante = 1000.0
    pg.event.clear()
    yield game
    pg.quit()


def avancar(game, segundos):
    game.delta_time = round(segundos * 1000)
    game.update()


def mapa_de_teste():
    grade = [[1,1,1,1,1,1,1],
             [1,0,1,0,0,0,1],
             [1,0,1,0,1,0,1],
             [1,0,0,0,1,0,1],
             [1,1,1,1,1,1,1]]
    walls={(x,y):1 for y,row in enumerate(grade) for x,v in enumerate(row) if v}
    return grade,walls


def test_caminho_contorna_parede_sem_diagonais():
    from src.boss import encontrar_caminho
    grade,walls=mapa_de_teste()
    path=encontrar_caminho((1,1),(5,1),walls,grade)
    assert path[0]==(1,1) and path[-1]==(5,1)
    assert all(cell not in walls for cell in path)
    assert all(abs(a[0]-b[0])+abs(a[1]-b[1])==1 for a,b in zip(path,path[1:]))


def test_sem_caminho_chefe_permanece_parado():
    from src.boss import mover_boss
    grade,walls=mapa_de_teste()
    walls[(1,2)]=1
    boss={"x":1.5,"y":1.5,"ativo":True}
    for _ in range(20):
        mover_boss(boss,(5.5,1.5),walls,grade,.05)
    assert (boss["x"],boss["y"])==(1.5,1.5)


def test_aproximacao_nao_atravessa_paredes_ou_quinas():
    from src.boss import mover_boss
    grade,walls=mapa_de_teste()
    boss={"x":1.5,"y":1.5,"ativo":True}
    for _ in range(240):
        mover_boss(boss,(5.5,1.5),walls,grade,.05)
        for dx in (-.18,.18):
            for dy in (-.18,.18):
                assert (math.floor(boss["x"]+dx),math.floor(boss["y"]+dy)) not in walls
    assert math.hypot(boss["x"]-5.5,boss["y"]-1.5)<1.0


def test_passo_longo_tambem_nao_tunela_parede():
    from src.boss import mover_boss
    grade,walls=mapa_de_teste()
    boss={"x":1.5,"y":1.5,"ativo":True}
    mover_boss(boss,(5.5,1.5),walls,grade,2.0)
    assert (int(boss["x"]),int(boss["y"])) not in walls
    assert boss["y"]>1.5


def preparar_projecao(game, profundidade=20.0):
    from src.settings import NUM_RAYS
    game.player.x,game.player.y,game.player.angle=1.5,4.5,0.0
    game.boss={"x":4.5,"y":4.5,"ativo":True}
    game.boss_ativo=True
    game.raycasting.ray_casting_result=[(i,profundidade,100,1,.5,1) for i in range(NUM_RAYS)]
    game.screen.fill("black")


def test_chefe_visivel_em_perspectiva(final_game):
    preparar_projecao(final_game)
    before=pg.image.tostring(final_game.screen,"RGB")
    assert final_game.object_renderer.desenhar_boss()>0
    assert pg.image.tostring(final_game.screen,"RGB")!=before


def test_parede_oculta_chefe(final_game):
    preparar_projecao(final_game,1.0)
    before=pg.image.tostring(final_game.screen,"RGB")
    assert final_game.object_renderer.desenhar_boss()==0
    assert pg.image.tostring(final_game.screen,"RGB")==before


def test_chefe_atras_da_camera_nao_e_desenhado(final_game):
    preparar_projecao(final_game)
    final_game.boss["x"]=0.5
    assert final_game.object_renderer.desenhar_boss()==0


def test_oclusao_parcial_respeita_cada_coluna(final_game):
    preparar_projecao(final_game)
    total=final_game.object_renderer.desenhar_boss()
    rays=final_game.raycasting.ray_casting_result
    for i in range(len(rays)//2):
        rays[i]=(i,1.0,100,1,.5,1)
    parcial=final_game.object_renderer.desenhar_boss()
    assert 0<parcial<total


def test_desenho_nao_recarrega_recursos_por_quadro(final_game,monkeypatch):
    preparar_projecao(final_game)
    def nao_carregar(*_args,**_kwargs):
        pytest.fail("Os recursos precisam estar carregados antes do desenho")
    monkeypatch.setattr(pg.image,"load",nao_carregar)
    final_game.object_renderer.desenhar_boss()
    final_game.object_renderer.desenhar_boss()


def test_pergunta_real_congela_entidade_e_prazos(final_game):
    assert final_game.criar_boss()
    terminal=next(iter(final_game.map.tarefas_pendentes))
    assert final_game.abrir_pergunta(terminal)
    boss=copy.deepcopy(final_game.boss)
    state=(final_game.tempo_boss,final_game.tempo_cumprimento_boss,final_game.tempo_restante,final_game.player.pos)
    avancar(final_game,20.0)
    assert final_game.boss==boss
    assert state==(final_game.tempo_boss,final_game.tempo_cumprimento_boss,final_game.tempo_restante,final_game.player.pos)
    final_game.fechar_pergunta()
    chances=final_game.chances
    avancar(final_game,.016)
    assert final_game.chances==chances


def test_nao_cumprimenta_atraves_de_parede(final_game):
    assert final_game.criar_boss()
    final_game.player.x,final_game.player.y=1.5,4.5
    final_game.boss.update(x=3.0,y=4.5)
    final_game.map.world_map[(2,4)]=1
    assert final_game.cumprimentar_boss() is False


def test_ranking_desenha_e_esc_volta_ao_menu(final_game):
    final_game.estado="ranking"
    final_game.draw()
    pg.event.post(pg.event.Event(pg.KEYDOWN,key=pg.K_ESCAPE,unicode=""))
    final_game.check_events()
    assert final_game.estado=="menu"


def test_texturas_e_sprite_principais_existem():
    from src import settings
    assert all((settings.CAMINHO_TEXTURAS/f"{i}.png").is_file() for i in range(1,5))
    assert settings.CAMINHO_BOSS.is_file()
    assert settings.CAMINHO_TRILHA.is_file()
    assert settings.CAMINHO_SUSTO.is_file()


def test_textura_de_erro_e_carregada(final_game):
    assert set(final_game.object_renderer.texturas_parede)=={1,2,3,4}
    assert final_game.object_renderer.origem_sprite_boss is not None


class SomFalso:
    def __init__(self):self.play_calls=0
    def set_volume(self,volume):self.volume=volume
    def play(self):self.play_calls+=1


class MusicaFalsa:
    def __init__(self):self.loads=[];self.plays=[];self.busy=False
    def load(self,path):self.loads.append(path)
    def play(self,loops):self.plays.append(loops);self.busy=True
    def set_volume(self,volume):self.volume=volume
    def stop(self):self.busy=False
    def get_busy(self):return self.busy


class MixerFalso:
    def __init__(self):self.music=MusicaFalsa();self.sound=SomFalso()
    def get_init(self):return (22050,-16,2)
    def Sound(self,_path):return self.sound


def test_trilha_em_loop_nao_reinicia_a_cada_chamada():
    from src.audio import AudioManager
    mixer=MixerFalso()
    audio=AudioManager(mixer=mixer)
    audio.iniciar_partida();audio.iniciar_trilha();audio.iniciar_trilha()
    assert mixer.music.plays==[-1]
    assert len(mixer.music.loads)==1


def test_susto_toca_uma_vez_por_derrota():
    from src.audio import AudioManager
    mixer=MixerFalso();audio=AudioManager(mixer=mixer)
    audio.iniciar_partida();audio.tocar_susto();audio.tocar_susto()
    assert mixer.sound.play_calls==1
    audio.iniciar_partida();audio.tocar_susto()
    assert mixer.sound.play_calls==2


def test_volume_e_mudo_respeitam_limites():
    from src.audio import AudioManager
    mixer=MixerFalso();audio=AudioManager(mixer=mixer)
    audio.ajustar_volume(10)
    assert audio.volume==1.0
    audio.alternar_mudo();assert mixer.music.volume==0
    audio.alternar_mudo();assert mixer.music.volume==1.0
    audio.ajustar_volume(-10);assert audio.volume==0.0


def test_falta_de_dispositivo_de_audio_nao_impede_jogo():
    from src.audio import AudioManager
    class SemAudio(MixerFalso):
        def get_init(self):return None
        def init(self,**_kwargs):raise pg.error("sem dispositivo")
    audio=AudioManager(mixer=SemAudio())
    assert audio.disponivel is False
    audio.iniciar_partida();audio.tocar_susto();audio.ajustar_volume(.1)


def test_jumpscare_nao_rearma_em_game_over(final_game,monkeypatch):
    calls=[]
    monkeypatch.setattr(final_game.audio,"tocar_susto",lambda:calls.append(True))
    final_game.encerrar_partida()
    remaining=final_game.jumpscare_restante
    final_game.encerrar_partida()
    assert final_game.estado=="game_over"
    assert remaining>0 and final_game.jumpscare_restante==remaining
    assert calls==[True]
    final_game.draw()
    avancar(final_game,2.0)
    assert final_game.jumpscare_restante==0.0
    assert final_game.estado=="game_over"


def test_update_nao_inicia_trilha_por_quadro(final_game,monkeypatch):
    def nao_reiniciar():pytest.fail("Não deve reiniciar música no quadro")
    monkeypatch.setattr(final_game.audio,"iniciar_trilha",nao_reiniciar)
    avancar(final_game,.016);final_game.draw()
