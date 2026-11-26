---
tipo: ticket_execucao
projeto: atividade-pygame
responsavel: Ricardo
atividade: "R05"
prioridade: P1
status: pendente
estimativa_min: 20
ordem: 6
dia_do_plano: "2026-11-25"
atualizado_em: "2026-11-26"
commit_base: "f138590303129f4d869886d1c36c20df139608b1"
tags: [pygame, ricardo, quarta, execucao]
---

# Q06 - Controlar o prazo e aplicar a penalidade uma vez

**Tempo estimado:** 20 min | **Atividade:** R05 | **Prioridade:** P1
**Depende de:** [[Q05_Implementar_cumprimento|Q05 - Aceitar o cumprimento e encerrar o encontro]]

[[00_Painel_Quarta|Voltar ao painel]]

> [!todo] Objetivo
> Ainda não existe prazo ativo para cumprimentar nem tratamento do vencimento desse prazo.

## Critérios de aceite
- [x] O prazo de cumprimento usa o valor que você já definiu na primeira etapa de quarta. <!-- Q06-CA01 -->
- [ ] O prazo começa na aparição válida e deixa de produzir punição após um cumprimento aceito. <!-- Q06-CA02 -->
- [ ] Ao vencer o prazo, a penalidade combinada é aplicada uma única vez, mesmo com vários quadros seguintes. <!-- Q06-CA03 -->
- [ ] O encontro vencido é encerrado e não dispara repetidamente a mesma penalidade. <!-- Q06-CA04 -->
- [ ] Se a penalidade zerar as chances, a partida segue para o Game Over existente. <!-- Q06-CA05 -->

## Executar
- [x] Representar o prazo do encontro separadamente do intervalo de 30 segundos e do tempo restante da rodada. <!-- Q06-EX01 -->
- [x] Atualizar esse prazo enquanto o encontro estiver ativo e aplicar a penalidade prevista ao esgotar. <!-- Q06-EX02 -->
- [x] Encerrar ou marcar o encontro como resolvido antes que os quadros seguintes possam aplicar a penalidade novamente; rearmar o ciclo conforme sua regra. <!-- Q06-EX03 -->

> [!tip] Para raciocinar
> O teste mais importante é continuar atualizando o jogo depois do prazo e verificar que a penalidade não se repete.

## Evidência da revisão
boss.py mantém dano_boss com pass. jogo.py tem o fluxo existente de perder_chance e encerrar_partida, mas nenhuma chamada ligada ao prazo do chefe.

- [boss.py - dano_boss, linha 29](https://github.com/Knumi5/atividade-pygame/blob/8ef8ba75b2523a2d148c1aa8fc26ba8cc0ca19d5/src/boss.py#L29)
- [jogo.py - perder_chance, linha 125](https://github.com/Knumi5/atividade-pygame/blob/8ef8ba75b2523a2d148c1aa8fc26ba8cc0ca19d5/src/jogo.py#L125)

## Registro ao terminar
- Resultado observado:
- Evidência do teste ou commit:
- Falha encontrada, se houver:
