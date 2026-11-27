# Resultados do fluxo de quarta

Regras confirmadas: F, alcance de 1,8 célula, prazo de 5 segundos e penalidade
de uma chance sem reiniciar a rodada. Cada encontro resolvido rearma uma
espera completa de 30 segundos de jogo ativo.

## Execução de ponta a ponta

O teste `test_ciclo_completo_eventos_hud_e_game_over` executa a criação,
renderiza a HUD, envia um evento F pela fila real do Pygame, confirma a
limpeza, aguarda outra aparição e percorre as penalidades até o Game Over.
Os arquivos de ranking e recorde ficam em diretórios temporários.

## Cenários individuais

Os resultados observados e os comandos de cada cenário ficam nas entradas
Q07-CT01 a Q07-CT08 de `REGISTRO_EXECUCAO.md`. Cada entrada é registrada
somente após o teste correspondente passar.

## Ambiente

Python 3.12, Pygame 2.6.1 e vídeo/áudio SDL dummy. As superfícies, eventos e
rotinas de desenho são reais; o avanço de tempo é controlado para testar
limites sem esperar 30 segundos em cada caso. Teclado, mouse e desempenho
na máquina de apresentação continuam sujeitos à validação presencial.
