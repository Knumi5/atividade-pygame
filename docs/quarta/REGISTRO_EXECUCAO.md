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

## Q05-CA02

Cumprir dentro do prazo encerra o encontro sem penalidade.

- Verificação: `python -m pytest -q tests/test_encontros_boss.py::test_cumprimento_no_prazo_nao_pune`.
- Resultado: 1 passed in 0.08s.

## Q05-CA03

Uma interação fora do alcance não encerra o encontro.

- Verificação: `python -m pytest -q tests/test_encontros_boss.py::test_cumprimento_respeita_alcance`.
- Resultado: 4 passed in 0.20s.

## Q05-CA04

Uma mesma entrada não conclui simultaneamente um terminal e o cumprimento.

- Verificação: `python -m pytest -q tests/test_encontros_boss.py::test_evento_f_cumprimenta_sem_interagir_com_terminal tests/test_encontros_boss.py::test_mesma_tecla_nao_cumprimenta_e_resolve_terminal`.
- Resultado: 2 passed in 0.11s.

## Q05-CA05

Depois do encontro, o aviso e a presença do chefe são limpos e o próximo ciclo é rearmado conforme a regra combinada.

- Verificação: `python -m pytest -q tests/test_encontros_boss.py::test_encerrar_rearma_espera_completa tests/test_encontros_boss.py::test_tecla_repetida_nao_resolve_outro_encontro`.
- Resultado: 2 passed in 0.12s.

## Q06-EX01

Representar o prazo do encontro separadamente do intervalo de 30 segundos e do tempo restante da rodada.

- Verificação: `python -m pytest -q tests/test_encontros_boss.py::test_prazo_comeca_na_criacao_e_tem_contador_proprio tests/test_encontros_boss.py::test_prazo_so_comeca_quando_ha_posicao_valida tests/test_encontros_boss.py::test_nova_partida_limpa_todo_estado_do_encontro`.
- Resultado: 3 passed in 0.22s.

## Q06-EX02

Atualizar esse prazo enquanto o encontro estiver ativo e aplicar a penalidade prevista ao esgotar.

- Verificação: `python -m pytest -q tests/test_encontros_boss.py::test_prazo_decrementa_sem_mudar_contador_de_espera tests/test_encontros_boss.py::test_expiracao_aplica_uma_penalidade_e_preserva_rodada`.
- Resultado: 2 passed in 0.18s.

## Q06-EX03

Encerrar ou marcar o encontro como resolvido antes que os quadros seguintes possam aplicar a penalidade novamente; rearmar o ciclo conforme sua regra.

- Verificação: `python -m pytest -q tests/test_encontros_boss.py::test_expiracao_aplica_uma_penalidade_e_preserva_rodada tests/test_encontros_boss.py::test_ciclo_completo_eventos_hud_e_game_over`.
- Resultado: 2 passed in 0.22s.

## Q06-CA01

O prazo de cumprimento usa o valor que você já definiu na primeira etapa de quarta.

- Verificação: `python -m pytest -q tests/test_encontros_boss.py::test_regras_confirmadas_pelo_usuario tests/test_encontros_boss.py::test_prazo_comeca_na_criacao_e_tem_contador_proprio`.
- Resultado: 2 passed in 0.09s.

## Q06-CA02

O prazo começa na aparição válida e deixa de produzir punição após um cumprimento aceito.

- Verificação: `python -m pytest -q tests/test_encontros_boss.py::test_prazo_so_comeca_quando_ha_posicao_valida tests/test_encontros_boss.py::test_cumprimento_no_prazo_nao_pune`.
- Resultado: 2 passed in 0.15s.

## Q06-CA03

Ao vencer o prazo, a penalidade combinada é aplicada uma única vez, mesmo com vários quadros seguintes.

- Verificação: `python -m pytest -q tests/test_encontros_boss.py::test_expiracao_aplica_uma_penalidade_e_preserva_rodada`.
- Resultado: 1 passed in 0.12s.

## Q06-CA04

O encontro vencido é encerrado e não dispara repetidamente a mesma penalidade.

- Verificação: `python -m pytest -q tests/test_encontros_boss.py::test_expiracao_aplica_uma_penalidade_e_preserva_rodada tests/test_encontros_boss.py::test_ciclo_completo_eventos_hud_e_game_over`.
- Resultado: 2 passed in 0.18s.

## Q06-CA05

Se a penalidade zerar as chances, a partida segue para o Game Over existente.

- Verificação: `python -m pytest -q tests/test_encontros_boss.py::test_penalidade_com_ultima_chance_salva_ranking_e_game_over`.
- Resultado: 1 passed in 0.08s.

## Q07-EX02

Depois dos testes de regra, percorrer a partida para validar a ligação com eventos, HUD e Game Over.

- Verificação: `python -m pytest -q tests/test_encontros_boss.py::test_ciclo_completo_eventos_hud_e_game_over tests/test_encontros_boss.py::test_evento_f_cumprimenta_sem_interagir_com_terminal`.
- Resultado: 2 passed in 0.19s.

## Q07-EX03

Registrar o observado e corrigir qualquer falha antes de marcar R04/R05 como concluídos.

- Verificação: `python -m pytest -q tests`.
- Resultado: 70 passed in 2.91s.

## Q07-CT01

29,9 s, chefe ausente: nenhuma criação.

- Verificação: `python -m pytest -q tests/test_encontros_boss.py::test_antes_30_segundos_nao_cria`.
- Resultado: 3 passed in 0.19s.
- Observado: Em 29,9 s, boss=None e boss_ativo=False.

## Q07-CT02

30,0 s e 30,1 s, chefe ausente: autorização e uma criação válida.

- Verificação: `python -m pytest -q tests/test_encontros_boss.py::test_atingir_ou_ultrapassar_30_cria`.
- Resultado: 4 passed in 0.25s.
- Observado: Em 30,0 s e 30,1 s houve uma entidade ativa em célula livre.

## Q07-CT03

Vários quadros com chefe ativo: nenhuma criação adicional.

- Verificação: `python -m pytest -q tests/test_encontros_boss.py::test_varios_quadros_nao_duplicam_chefe`.
- Resultado: 1 passed in 0.14s.
- Observado: Após 20 quadros adicionais, uma chamada à criação e a mesma entidade.

## Q07-CT04

Cumprimento válido antes do prazo: encontro encerrado, sem penalidade.

- Verificação: `python -m pytest -q tests/test_encontros_boss.py::test_cumprimento_no_prazo_nao_pune`.
- Resultado: 1 passed in 0.08s.
- Observado: F após 4 s encerrou o encontro, limpou o aviso e preservou as chances.

## Q07-CT05

Interação fora do alcance ou sem chefe: nenhum cumprimento aceito.

- Verificação: `python -m pytest -q tests/test_encontros_boss.py::test_cumprimento_respeita_alcance tests/test_encontros_boss.py::test_sem_chefe_cumprimento_nao_tem_efeito`.
- Resultado: 5 passed in 0.23s.
- Observado: Distâncias 1,801 e 4 células foram rejeitadas; sem chefe o retorno foi False.

## Q07-CT06

Prazo esgotado seguido de vários quadros: uma penalidade apenas.

- Verificação: `python -m pytest -q tests/test_encontros_boss.py::test_expiracao_aplica_uma_penalidade_e_preserva_rodada`.
- Resultado: 1 passed in 0.12s.
- Observado: Prazo de 5 s reduziu chances de 5 para 4, preservou mapa e tarefas; dez quadros depois não houve novo desconto.

## Q07-CT07

Nova partida: contador zerado, chefe inativo e dados/aviso antigos limpos.

- Verificação: `python -m pytest -q tests/test_encontros_boss.py::test_nova_partida_limpa_todo_estado_do_encontro`.
- Resultado: 1 passed in 0.07s.
- Observado: Nova partida iniciou com contador 0, chefe None/inativo, prazo 0 e aviso vazio.

## Q07-CT08

Penalidade com a última chance: Game Over.

- Verificação: `python -m pytest -q tests/test_encontros_boss.py::test_penalidade_com_ultima_chance_salva_ranking_e_game_over`.
- Resultado: 1 passed in 0.07s.
- Observado: Última chance foi de 1 a 0, estado game_over e pontuação 7 salva em recorde e ranking temporários.

## Q07-CA01

Todos os cenários abaixo têm resultado observado registrado.

- Verificação: `python -m pytest -q tests/test_encontros_boss.py::test_antes_30_segundos_nao_cria tests/test_encontros_boss.py::test_atingir_ou_ultrapassar_30_cria`.
- Resultado: 7 passed in 0.41s.

## Q07-CA02

Não há criação duplicada, punição repetida ou estado antigo reaproveitado em uma nova partida.

- Verificação: `python -m pytest -q tests/test_encontros_boss.py::test_varios_quadros_nao_duplicam_chefe tests/test_encontros_boss.py::test_expiracao_aplica_uma_penalidade_e_preserva_rodada tests/test_encontros_boss.py::test_nova_partida_limpa_todo_estado_do_encontro`.
- Resultado: 3 passed in 0.27s.
