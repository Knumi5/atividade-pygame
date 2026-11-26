---
tipo: ticket_execucao
projeto: atividade-pygame
responsavel: Ricardo
atividade: "R05"
prioridade: P1
status: pendente
estimativa_min: 20
ordem: 5
dia_do_plano: "2026-11-25"
atualizado_em: "2026-11-26"
commit_base: "f138590303129f4d869886d1c36c20df139608b1"
tags: [pygame, ricardo, quarta, execucao]
---

# Q05 - Aceitar o cumprimento e encerrar o encontro

**Tempo estimado:** 20 min | **Atividade:** R05 | **Prioridade:** P1
**Depende de:** [[Q04_Ligar_spawn_ao_loop|Q04 - Acionar um único spawn após 30 segundos]]

[[00_Painel_Quarta|Voltar ao painel]]

> [!todo] Objetivo
> O jogo ainda não possui um fluxo de cumprimento do chefe.

## Critérios de aceite
- [x] Um cumprimento só é aceito quando há chefe ativo e o jogador está dentro do alcance combinado. <!-- Q05-CA01 -->
- [x] Cumprir dentro do prazo encerra o encontro sem penalidade. <!-- Q05-CA02 -->
- [ ] Uma interação fora do alcance não encerra o encontro. <!-- Q05-CA03 -->
- [ ] Uma mesma entrada não conclui simultaneamente um terminal e o cumprimento. <!-- Q05-CA04 -->
- [ ] Depois do encontro, o aviso e a presença do chefe são limpos e o próximo ciclo é rearmado conforme a regra combinada. <!-- Q05-CA05 -->

## Executar
- [x] Aplicar a tecla e o alcance anotados por você na primeira etapa de quarta. <!-- Q05-EX01 -->
- [x] Conectar a detecção do cumprimento ao tratamento de eventos, respeitando a interação já existente com terminais. <!-- Q05-EX02 -->
- [x] Ao cumprir corretamente, encerrar o encontro e preparar a espera pela próxima aparição. <!-- Q05-EX03 -->

> [!tip] Para raciocinar
> Separe três verificações: existe chefe, o jogador está perto e a entrada corresponde ao cumprimento combinado.

## Evidência da revisão
check_events() trata a interação com terminais, mas não há verificação de chefe ativo, alcance ou cumprimento. Use a tecla, o alcance e as regras que você já definiu na primeira parte de quarta.

- [jogo.py - check_events, linha 324](https://github.com/Knumi5/atividade-pygame/blob/8ef8ba75b2523a2d148c1aa8fc26ba8cc0ca19d5/src/jogo.py#L324)
- [jogo.py - interação existente, linha 355](https://github.com/Knumi5/atividade-pygame/blob/8ef8ba75b2523a2d148c1aa8fc26ba8cc0ca19d5/src/jogo.py#L355)

## Registro ao terminar
- Resultado observado:
- Evidência do teste ou commit:
- Falha encontrada, se houver:
