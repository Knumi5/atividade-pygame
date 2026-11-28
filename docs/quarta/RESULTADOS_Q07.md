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

## Regressão encontrada e corrigida

A revisão completa reproduziu **5 falhas e 65 aprovações**: ao trocar de
layout, a entidade conservava coordenadas do mapa anterior. Os cinco casos
foram tornados determinísticos, iniciando o encontro longe da posição inicial
do novo layout. A correção reposiciona a mesma entidade em uma vizinha livre,
sem reiniciar o prazo. Se não houver ponto válido, o encontro é limpo.

A renderização foi conferida nas etapas de aparição, cumprimento, penalidade
e Game Over, usando capturas das superfícies reais do jogo.

## Ambiente

Python 3.12, Pygame 2.6.1 e vídeo/áudio SDL dummy. As superfícies, eventos e
rotinas de desenho são reais; o avanço de tempo é controlado para testar
limites sem esperar 30 segundos em cada caso. Teclado, mouse e desempenho
na máquina de apresentação continuam sujeitos à validação presencial.

## Encerramento

- Suíte completa: **70 testes aprovados**, nenhuma falha.
- Compilação de `src/` e `tests/`: aprovada.
- `git diff --check`: aprovado.
- Auditoria do histórico: **38 commits novos para 38 checkboxes**, exatamente
  uma checkbox marcada em cada commit, com seu identificador na mensagem.
- Q04, Q05, Q06 e Q07 estão concluídos nas notas desta pasta.
