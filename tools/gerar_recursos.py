"""Recursos originais de Try // Except, reproduzíveis sem downloads externos.

Execute da raiz: python tools/gerar_recursos.py. Usa apenas pygame e a stdlib.
O seed fixo mantém o ruído dos sons e os pixels idênticos entre execuções.
"""
import math
import os
import random
import struct
import wave
from pathlib import Path

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
import pygame as pg

RAIZ = Path(__file__).resolve().parents[1]
IMAGENS = RAIZ / "assets" / "imagens"
SONS = RAIZ / "assets" / "sons"
TAXA = 11025


def textura(tipo):
    s = pg.Surface((128, 128))
    s.fill((143, 143, 130))
    for y in range(128):
        cor = (155 - y // 12, 154 - y // 14, 139 - y // 16)
        pg.draw.line(s, cor, (0, y), (127, y))
    for x in (0, 63, 126):
        pg.draw.line(s, (89, 100, 96), (x, 0), (x, 127), 2)
        pg.draw.line(s, (177, 179, 158), (x + 2, 0), (x + 2, 127))
    pg.draw.rect(s, (52, 66, 68), (0, 98, 128, 30))
    pg.draw.line(s, (184, 161, 101), (0, 97), (127, 97), 2)
    pg.draw.rect(s, (31, 42, 47), (0, 122, 128, 6))
    if tipo == 1:
        pg.draw.rect(s, (55, 68, 73), (42, 22, 44, 24))
        pg.draw.rect(s, (173, 156, 111), (45, 25, 38, 18), 1)
        # Pequeno símbolo de código, sem depender de fontes do sistema.
        pg.draw.lines(s, (173, 156, 111), False, [(53, 29), (49, 34), (53, 39)], 2)
        pg.draw.lines(s, (173, 156, 111), False, [(75, 29), (79, 34), (75, 39)], 2)
        pg.draw.line(s, (173, 156, 111), (66, 28), (61, 40), 2)
    else:
        cor = {2: (57, 199, 214), 3: (84, 213, 132), 4: (228, 91, 86)}[tipo]
        pg.draw.rect(s, (20, 29, 37), (22, 29, 84, 62))
        pg.draw.rect(s, (68, 82, 87), (25, 32, 78, 55), 2)
        pg.draw.rect(s, (9, 29, 34), (30, 37, 68, 44))
        pg.draw.line(s, (38, 52, 56), (33, 42), (94, 42))
        if tipo == 2:
            pg.draw.lines(s, cor, False, [(39, 50), (46, 56), (39, 62)], 2)
            pg.draw.line(s, cor, (54, 63), (69, 63), 2)
            pg.draw.line(s, cor, (36, 74), (85, 74))
        elif tipo == 3:
            pg.draw.lines(s, cor, False, [(47, 56), (58, 66), (79, 47)], 4)
        else:
            pg.draw.line(s, cor, (52, 48), (76, 70), 4)
            pg.draw.line(s, cor, (76, 48), (52, 70), 4)
        pg.draw.circle(s, cor, (96, 85), 2)
        pg.draw.rect(s, (31, 43, 49), (58, 91, 12, 10))
        pg.draw.rect(s, (27, 38, 43), (41, 101, 46, 4))
    return pg.transform.scale(s, (256, 256))


def chefe():
    s = pg.Surface((96, 160), pg.SRCALPHA)
    # Sombra e sapatos, calça, paletó, braços, camisa e gravata.
    pg.draw.ellipse(s, (8, 14, 22, 100), (10, 151, 78, 8))
    for x in (24, 51):
        pg.draw.rect(s, (23, 30, 42), (x, 104, 20, 45))
        pg.draw.rect(s, (10, 18, 29), (x - 3, 146, 24, 8))
        pg.draw.line(s, (66, 76, 85), (x + 9, 111), (x + 9, 143))
    pg.draw.polygon(s, (25, 40, 54), [(22, 55), (72, 55), (83, 110), (13, 110)])
    pg.draw.polygon(s, (215, 208, 179), [(35, 53), (59, 53), (52, 86), (43, 86)])
    pg.draw.polygon(s, (158, 45, 55), [(46, 60), (51, 60), (54, 91), (48, 98), (43, 91)])
    pg.draw.lines(s, (70, 87, 97), False, [(32, 57), (27, 75), (38, 91)], 2)
    pg.draw.lines(s, (70, 87, 97), False, [(64, 57), (69, 75), (58, 91)], 2)
    pg.draw.rect(s, (38, 53, 63), (13, 62, 13, 42))
    pg.draw.rect(s, (32, 47, 60), (71, 62, 13, 42))
    pg.draw.rect(s, (199, 160, 132), (14, 100, 12, 13))
    pg.draw.rect(s, (199, 160, 132), (72, 100, 12, 13))
    pg.draw.rect(s, (122, 91, 58), (66, 93, 23, 29))
    pg.draw.rect(s, (201, 189, 151), (69, 97, 17, 21))
    for y in (102, 107, 112):
        pg.draw.line(s, (113, 119, 108), (72, y), (82, y))
    pg.draw.rect(s, (187, 149, 119), (41, 44, 14, 16))
    pg.draw.ellipse(s, (212, 181, 142), (29, 9, 38, 43))
    pg.draw.rect(s, (198, 163, 127), (29, 22, 38, 21))
    pg.draw.rect(s, (25, 25, 33), (29, 13, 7, 20))
    pg.draw.rect(s, (25, 25, 33), (60, 13, 7, 20))
    pg.draw.rect(s, (30, 29, 35), (32, 9, 32, 6))
    pg.draw.rect(s, (35, 33, 38), (34, 25, 12, 5))
    pg.draw.rect(s, (35, 33, 38), (52, 25, 11, 5))
    pg.draw.rect(s, (236, 109, 76), (38, 27, 5, 2))
    pg.draw.rect(s, (236, 109, 76), (54, 27, 5, 2))
    pg.draw.line(s, (143, 105, 88), (47, 30), (45, 38), 2)
    pg.draw.line(s, (75, 49, 48), (39, 43), (57, 43), 2)
    return s


def salvar_som(nome, duracao, amostra):
    total = int(TAXA * duracao)
    dados = bytearray()
    for i in range(total):
        t = i / TAXA
        # As duas pontas chegam a zero para não haver clique na emenda do loop.
        envelope = min(1.0, t / 0.12, (duracao - t) / 0.12)
        valor = max(-1.0, min(1.0, amostra(t) * envelope))
        dados.extend(struct.pack("<h", round(valor * 32767)))
    with wave.open(str(SONS / nome), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(TAXA)
        wav.writeframes(dados)


def main():
    pg.display.init()
    (IMAGENS / "texturas").mkdir(parents=True, exist_ok=True)
    SONS.mkdir(parents=True, exist_ok=True)
    for tipo in range(1, 5):
        pg.image.save(textura(tipo), str(IMAGENS / "texturas" / f"{tipo}.png"))
    pg.image.save(chefe(), str(IMAGENS / "chefe.png"))
    rng = random.Random(20261127)

    def ambiente(t):
        base = sum(math.sin(2 * math.pi * hz * t) * peso
                   for hz, peso in ((55, .12), (82.5, .07), (110, .04)))
        pulso = .7 + .3 * math.sin(2 * math.pi * .25 * t)
        nota = (220, 261.625, 246.942, 164.814)[int(t // 2) % 4]
        tecla = math.sin(2 * math.pi * nota * t) * .035 * math.exp(-5 * (t % 2))
        return base * pulso + tecla + rng.uniform(-.004, .004)

    def susto(t):
        ruido = rng.uniform(-.28, .28)
        tom = math.sin(2 * math.pi * (180 * t + 280 * t * t)) * .22
        return (ruido + tom) * math.exp(-3 * t)

    salvar_som("escritorio_loop.wav", 8.0, ambiente)
    salvar_som("chefe_susto.wav", .65, susto)
    pg.quit()
    print("Gerados: quatro texturas, um sprite e dois sons originais.")


if __name__ == "__main__":
    main()
