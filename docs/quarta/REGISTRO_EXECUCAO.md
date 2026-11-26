# Execução de Q04 a Q07

Base: Q03 no commit `f138590303129f4d869886d1c36c20df139608b1`.

Regras confirmadas pelo usuário: F, alcance 1,8 célula, prazo 5 s e penalidade de 1 chance sem reiniciar a rodada.

Cada checkbox será marcada em seu próprio commit, com o teste ou a evidência correspondente. Os cenários são preparados antes das alterações de implementação.

## Q07-EX01

Preparar os cenários da lista antes da execução e testar os limites de tempo de forma controlada.

- Verificação: `python -m pytest -q --tb=no (fase vermelha antes da implementação)`.
- Resultado: Fase vermelha reproduzida: 36 falhas e 33 aprovações, antes de alterar src/.

## Q04-EX01

No bloco existente de contagem, consultar confirma_tempo usando o contador e o estado que você já criou.

- Verificação: `python -m pytest -q tests/test_encontros_boss.py::test_update_consulta_regra_de_autorizacao tests/test_encontros_boss.py::test_antes_30_segundos_nao_cria tests/test_encontros_boss.py::test_fora_da_partida_nao_conta_nem_cria`.
- Resultado: 7 passed in 0.35s.

## Q04-EX02

Quando houver autorização, chamar spawn_boss e guardar o retorno no Game.

- Verificação: `python -m pytest -q tests/test_encontros_boss.py::test_atingir_ou_ultrapassar_30_cria tests/test_spawn_boss.py::test_criacao_guarda_os_dados_e_ativa_chefe`.
- Resultado: 5 passed in 0.23s.

## Q04-EX03

Somente após uma criação válida, atualizar boss_ativo e usar aviso_chefe para informar a aparição na HUD.

- Verificação: `python -m pytest -q tests/test_encontros_boss.py::test_aparicao_valida_exibe_aviso tests/test_encontros_boss.py::test_sem_espaco_tenta_novamente_sem_ativar`.
- Resultado: 2 passed in 0.15s.

## Q04-CA01

Antes de 30 segundos de jogo ativo, nenhum chefe é criado.

- Verificação: `python -m pytest -q tests/test_encontros_boss.py::test_antes_30_segundos_nao_cria`.
- Resultado: 3 passed in 0.15s.

## Q04-CA02

Ao atingir ou ultrapassar 30 segundos, uma única criação válida acontece.

- Verificação: `python -m pytest -q tests/test_encontros_boss.py::test_atingir_ou_ultrapassar_30_cria`.
- Resultado: 4 passed in 0.23s.

## Q04-CA03

Com boss_ativo verdadeiro, novos quadros não criam outro chefe.

- Verificação: `python -m pytest -q tests/test_encontros_boss.py::test_varios_quadros_nao_duplicam_chefe`.
- Resultado: 1 passed in 0.12s.

## Q04-CA04

Se a criação falhar, boss_ativo continua falso.

- Verificação: `python -m pytest -q tests/test_encontros_boss.py::test_sem_espaco_tenta_novamente_sem_ativar`.
- Resultado: 1 passed in 0.08s.

## Q04-CA05

O tempo de espera permanece parado com uma pergunta aberta e fora da partida.

- Verificação: `python -m pytest -q tests/test_encontros_boss.py::test_fora_da_partida_nao_conta_nem_cria tests/test_encontros_boss.py::test_pergunta_pausa_espera_e_retorno_nao_acumula_punicao`.
- Resultado: 4 passed in 0.18s.

## Q05-EX01

Aplicar a tecla e o alcance anotados por você na primeira etapa de quarta.

- Verificação: `python -m pytest -q tests/test_encontros_boss.py::test_regras_confirmadas_pelo_usuario tests/test_encontros_boss.py::test_cumprimento_respeita_alcance tests/test_encontros_boss.py::test_sem_chefe_cumprimento_nao_tem_efeito`.
- Resultado: 6 passed in 0.29s.

## Q05-EX02

Conectar a detecção do cumprimento ao tratamento de eventos, respeitando a interação já existente com terminais.

- Verificação: `python -m pytest -q tests/test_encontros_boss.py::test_evento_f_cumprimenta_sem_interagir_com_terminal tests/test_encontros_boss.py::test_mesma_tecla_nao_cumprimenta_e_resolve_terminal tests/test_encontros_boss.py::test_outra_tecla_nao_cumprimenta`.
- Resultado: 3 passed in 0.19s.

## Q05-EX03

Ao cumprir corretamente, encerrar o encontro e preparar a espera pela próxima aparição.

- Verificação: `python -m pytest -q tests/test_encontros_boss.py::test_encerrar_rearma_espera_completa tests/test_encontros_boss.py::test_tecla_repetida_nao_resolve_outro_encontro`.
- Resultado: 2 passed in 0.15s.

## Q05-CA01

Um cumprimento só é aceito quando há chefe ativo e o jogador está dentro do alcance combinado.

- Verificação: `python -m pytest -q tests/test_encontros_boss.py::test_cumprimento_respeita_alcance tests/test_encontros_boss.py::test_sem_chefe_cumprimento_nao_tem_efeito`.
- Resultado: 5 passed in 0.26s.
