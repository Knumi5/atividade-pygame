---
tipo: ticket_execucao
projeto: atividade-pygame
responsavel: Ricardo
atividade: "R04-R05"
prioridade: P1
status: pendente
estimativa_min: 15
ordem: 7
dia_do_plano: "2026-11-25"
atualizado_em: "2026-11-26"
commit_base: "f138590303129f4d869886d1c36c20df139608b1"
tags: [pygame, ricardo, quarta, execucao]
---

# Q07 - Registrar os testes da aparição e do cumprimento

**Tempo estimado:** 15 min | **Atividade:** R04-R05 | **Prioridade:** P1
**Depende de:** [[Q04_Ligar_spawn_ao_loop|Q04 - Acionar um único spawn após 30 segundos]] · [[Q05_Implementar_cumprimento|Q05 - Aceitar o cumprimento e encerrar o encontro]] · [[Q06_Implementar_prazo_e_penalidade|Q06 - Controlar o prazo e aplicar a penalidade uma vez]]

[[00_Painel_Quarta|Voltar ao painel]]

> [!todo] Objetivo
> A regra de autorização foi testada isoladamente, mas o fluxo integrado de quarta ainda precisa ser validado após a implementação.

## Critérios de aceite
- [ ] Todos os cenários abaixo têm resultado observado registrado. <!-- Q07-CA01 -->
- [ ] Não há criação duplicada, punição repetida ou estado antigo reaproveitado em uma nova partida. <!-- Q07-CA02 -->
- [ ] O fluxo de R04 e R05 pode ser demonstrado do início ao fim. <!-- Q07-CA03 -->

## Executar
- [x] Preparar os cenários da lista antes da execução e testar os limites de tempo de forma controlada. <!-- Q07-EX01 -->
- [x] Depois dos testes de regra, percorrer a partida para validar a ligação com eventos, HUD e Game Over. <!-- Q07-EX02 -->
- [x] Registrar o observado e corrigir qualquer falha antes de marcar R04/R05 como concluídos. <!-- Q07-EX03 -->

## Cenários a validar
- [x] 29,9 s, chefe ausente: nenhuma criação. <!-- Q07-CT01 -->
- [x] 30,0 s e 30,1 s, chefe ausente: autorização e uma criação válida. <!-- Q07-CT02 -->
- [ ] Vários quadros com chefe ativo: nenhuma criação adicional. <!-- Q07-CT03 -->
- [ ] Cumprimento válido antes do prazo: encontro encerrado, sem penalidade. <!-- Q07-CT04 -->
- [ ] Interação fora do alcance ou sem chefe: nenhum cumprimento aceito. <!-- Q07-CT05 -->
- [ ] Prazo esgotado seguido de vários quadros: uma penalidade apenas. <!-- Q07-CT06 -->
- [ ] Nova partida: contador zerado, chefe inativo e dados/aviso antigos limpos. <!-- Q07-CT07 -->
- [ ] Penalidade com a última chance: Game Over. <!-- Q07-CT08 -->

> [!tip] Para raciocinar
> Use os mesmos casos antes e depois de cada ajuste. A função isolada e a partida integrada verificam partes diferentes.

## Evidência da revisão
A revisão confirmou seis casos da função confirma_tempo e identificou os bloqueios de importação e reinício. Isso não constitui um teste aprovado do fluxo completo da partida.

- [jogo.py - update](https://github.com/Knumi5/atividade-pygame/blob/8ef8ba75b2523a2d148c1aa8fc26ba8cc0ca19d5/src/jogo.py#L164)
- [jogo.py - check_events](https://github.com/Knumi5/atividade-pygame/blob/8ef8ba75b2523a2d148c1aa8fc26ba8cc0ca19d5/src/jogo.py#L324)
- [boss.py - funções do chefe](https://github.com/Knumi5/atividade-pygame/blob/8ef8ba75b2523a2d148c1aa8fc26ba8cc0ca19d5/src/boss.py#L20)

## Registro ao terminar
- Resultado observado:
- Evidência do teste ou commit:
- Falha encontrada, se houver:
