---
tipo: ticket_execucao
projeto: atividade-pygame
responsavel: Ricardo
atividade: "R04"
prioridade: P1
status: pendente
estimativa_min: 10
ordem: 4
dia_do_plano: "2026-11-25"
atualizado_em: "2026-11-26"
commit_base: "f138590303129f4d869886d1c36c20df139608b1"
tags: [pygame, ricardo, quarta, execucao]
---

# Q04 - Acionar um único spawn após 30 segundos

**Tempo estimado:** 10 min | **Atividade:** R04 | **Prioridade:** P1
**Depende de:** [[Q01_Alinhar_nome_da_funcao|Q01 - Alinhar o nome importado com confirma_tempo]] · [[Q02_Corrigir_reinicio_do_contador|Q02 - Corrigir o reinício do contador na nova partida]] · [[Q03_Criar_estado_e_posicao_do_chefe|Q03 - Dar dados e posição ao spawn_boss]]

[[00_Painel_Quarta|Voltar ao painel]]

> [!todo] Objetivo
> O update já soma tempo_boss, mas ainda não consulta confirma_tempo nem chama spawn_boss.

## Critérios de aceite
- [ ] Antes de 30 segundos de jogo ativo, nenhum chefe é criado. <!-- Q04-CA01 -->
- [ ] Ao atingir ou ultrapassar 30 segundos, uma única criação válida acontece. <!-- Q04-CA02 -->
- [ ] Com boss_ativo verdadeiro, novos quadros não criam outro chefe. <!-- Q04-CA03 -->
- [ ] Se a criação falhar, boss_ativo continua falso. <!-- Q04-CA04 -->
- [ ] O tempo de espera permanece parado com uma pergunta aberta e fora da partida. <!-- Q04-CA05 -->

## Executar
- [x] No bloco existente de contagem, consultar confirma_tempo usando o contador e o estado que você já criou. <!-- Q04-EX01 -->
- [x] Quando houver autorização, chamar spawn_boss e guardar o retorno no Game. <!-- Q04-EX02 -->
- [x] Somente após uma criação válida, atualizar boss_ativo e usar aviso_chefe para informar a aparição na HUD. <!-- Q04-EX03 -->

> [!tip] Para raciocinar
> A função confirma_tempo responde uma pergunta. O update usa essa resposta para decidir quando executar a ação.

## Evidência da revisão
jogo.py, linhas 173 e 174, já contém a proteção do painel e a soma de delta_time / 1000.0. Falta usar o resultado da função de autorização após essa soma.

- [jogo.py - update, linha 164](https://github.com/Knumi5/atividade-pygame/blob/8ef8ba75b2523a2d148c1aa8fc26ba8cc0ca19d5/src/jogo.py#L164)
- [jogo.py - contagem existente, linha 173](https://github.com/Knumi5/atividade-pygame/blob/8ef8ba75b2523a2d148c1aa8fc26ba8cc0ca19d5/src/jogo.py#L173)
- [boss.py - autorização, linha 20](https://github.com/Knumi5/atividade-pygame/blob/8ef8ba75b2523a2d148c1aa8fc26ba8cc0ca19d5/src/boss.py#L20)

## Registro ao terminar
- Resultado observado:
- Evidência do teste ou commit:
- Falha encontrada, se houver:
