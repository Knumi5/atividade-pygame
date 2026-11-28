"""Áudio da partida: carregamento único, volume e degradação sem dispositivo."""
import pygame as pg

if __package__:
    from .settings import CAMINHO_TRILHA, CAMINHO_SUSTO, VOLUME_INICIAL
else:
    from settings import CAMINHO_TRILHA, CAMINHO_SUSTO, VOLUME_INICIAL


class AudioManager:
    def __init__(self, mixer=None):
        self.mixer = pg.mixer if mixer is None else mixer
        self.volume = VOLUME_INICIAL
        self.mudo = False
        self.disponivel = False
        self.susto_tocado = False
        self.susto = None
        self.erro = ""
        try:
            if not self.mixer.get_init():
                self.mixer.init()
            self.mixer.music.load(str(CAMINHO_TRILHA))
            self.susto = self.mixer.Sound(str(CAMINHO_SUSTO))
            self.disponivel = True
            self._aplicar_volume()
        except (pg.error, OSError) as exc:
            self.erro = str(exc)

    def _aplicar_volume(self):
        if self.disponivel:
            volume = 0.0 if self.mudo else self.volume
            self.mixer.music.set_volume(volume)
            self.susto.set_volume(volume)

    def ajustar_volume(self, variacao):
        self.volume = max(0.0, min(1.0, self.volume + variacao))
        self._aplicar_volume()

    def alternar_mudo(self):
        self.mudo = not self.mudo
        self._aplicar_volume()

    def iniciar_partida(self):
        self.susto_tocado = False
        self.iniciar_trilha()

    def iniciar_trilha(self):
        if self.disponivel and not self.mixer.music.get_busy():
            self.mixer.music.play(-1)

    def tocar_susto(self):
        if self.susto_tocado:
            return
        self.susto_tocado = True
        if self.disponivel:
            self.mixer.music.stop()
            self.susto.play()

    def encerrar(self):
        if self.disponivel:
            self.mixer.music.stop()
