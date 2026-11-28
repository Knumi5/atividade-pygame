# Try // Except

Jogo de labirinto em primeira pessoa feito com Python e Pygame para a disciplina
Introdução a Algoritmos/Programação. Você é um programador que precisa concluir
tarefas sem a ajuda da IA, explorar o escritório e cumprimentar o chefe para
conservar suas chances.

## Equipe

- Ricardo Santana Kill: chefe, missões e recursos audiovisuais.
- Fernando Gomes Reis de Resende: pontuação, fontes e ranking.
- Igor Pereira Apolinário: correções e organização da HUD.
- Gustavo Alberto Araújo de Sá: critérios, testes e ranking.

## Executar

Validado em Python 3.12 e Pygame 2.6.1. Na raiz do projeto:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py
```

No menu, use as setas ou W/S e Enter. Preencha o nome antes de escolher Jogar.
A janela tem 1600 × 900 pixels. Se não houver dispositivo de áudio, o jogo
continua e a HUD informa que o som está indisponível.

## Regras

- A partida começa com 5 chances, 0 pontos e 3 terminais por rodada.
- E ou Mouse 1 perto de um terminal abre uma pergunta de programação. Digite
  a palavra-chave pedida: espaços externos e maiúsculas são normalizados.
- Acertar soma 1 ponto; errar desconta 1 chance. Ambos resolvem o terminal,
  mas somente acertos aumentam o contador de acertos. Não há efeito duplicado.
- Ao resolver os terminais restantes com chances, a próxima rodada começa em
  outro layout. O tempo começa em 45 s e diminui 3 s por rodada, até 15 s.
- Tempo esgotado desconta 1 chance e reinicia a tentativa em outro layout.
- Após 30 s de exploração ativa, o chefe aparece ao lado do jogador e o segue
  por chão livre. Pressione F em até 5 s, a no máximo 1,8 célula e sem parede
  entre vocês. Falhar tira 1 chance, preservando mapa, tarefas e tempo da rodada.
- Durante perguntas, jogador, chefe e cronômetros ficam pausados. Depois de
  resolver o encontro, começa uma nova espera de 30 s para o chefe.
- Zero chances encerra a partida: um susto visual/sonoro de 1,2 s antecede o
  resumo. A melhor pontuação é salva e pode ser consultada no menu de ranking.

O ranking preserva uma regra especial já presente na main: toda partida também
registra o nome Gustavo com quatro vezes a pontuação. Isso foi mantido na
integração e precisa ser considerado pela equipe ao avaliar a classificação.

## Controles

| Contexto | Comando | Ação |
| --- | --- | --- |
| Exploração | W / A / S / D | Mover |
| Exploração | Mouse / setas esquerda e direita | Girar a câmera |
| Exploração | E / Mouse 1 | Abrir terminal próximo |
| Exploração | F | Cumprimentar chefe próximo e visível |
| Pergunta | Texto / Backspace / Enter | Responder, apagar e confirmar |
| Pergunta | ESC | Cancelar sem penalidade |
| Exploração | - / + | Diminuir/aumentar o volume em 5 pontos percentuais |
| Qualquer tela | F10 | Silenciar/restaurar áudio, inclusive o susto |
| Guia | Setas / W / S / roda do mouse | Rolar instruções |
| Guia / ranking | ESC | Voltar ao menu |
| Game Over | Enter / Espaço após o susto | Voltar ao menu |
| Menu, exploração ou Game Over | ESC | Sair (na edição do nome, apenas cancela a edição) |

## Testes

```bash
python -m pytest -q
```

A suíte usa vídeo/áudio SDL dummy e arquivos temporários para não alterar os
recordes reais. Resultado da finalização de 28/11/2026: **186 testes aprovados**.
O carregamento de sons é exercitado, mas a audição e os controles físicos devem
ser conferidos no computador da apresentação.

## Código e documentação

- `main.py`: ponto de entrada; `src/jogo.py`: estados, rodadas e eventos.
- `src/boss.py`: aparição, caminho, colisão e visibilidade do encontro.
- `src/object_renderer.py`: texturas, sprite, oclusão e sobreposição do susto.
- `src/tarefas.py`, `src/map.py`, `src/player.py`: perguntas, terminais e jogador.
- `src/audio.py`: trilha, efeito, mudo e volume.
- `src/dados.py`, `src/ranking.py`: recorde em `data/recorde.txt` e ranking em
  `src/ranking.txt`, conforme os caminhos existentes da equipe.
- [Critérios de quinta/sexta](docs/aceite_quinta_sexta.md) e
  [resultado da entrega](docs/RESULTADO_QUINTA_SEXTA.md).
- [Recursos e geração reproduzível](assets/RECURSOS_ORIGINAIS.md).
- `docs/quarta/` e os documentos de aceite anteriores registram as etapas
  históricas, com contagens de testes válidas naquelas versões.
