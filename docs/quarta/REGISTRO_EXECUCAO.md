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
