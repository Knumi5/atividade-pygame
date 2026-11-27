# Quarta - Q04 a Q07 concluídos

Regras confirmadas por Ricardo: **F**, alcance de **1,8 célula**, prazo de
**5 segundos** e perda de **1 chance sem reiniciar a rodada**. A espera de
**30 segundos** é contada em jogo ativo e recomeça após cada encontro resolvido.

| Ticket | Estado | Checkboxes |
| --- | --- | --- |
| [Q04 - Aparição](Q04_Ligar_spawn_ao_loop.md) | Concluído | 8/8 |
| [Q05 - Cumprimento](Q05_Implementar_cumprimento.md) | Concluído | 8/8 |
| [Q06 - Prazo e penalidade](Q06_Implementar_prazo_e_penalidade.md) | Concluído | 8/8 |
| [Q07 - Validação](Q07_Validar_fluxo_de_quarta.md) | Concluído | 14/14 |

São **38 commits novos**, um para cada checkbox, além dos três commits
anteriores do Q03. As notas são arquivos Markdown compatíveis com Obsidian.

- [Registro de execução e evidências por checkbox](REGISTRO_EXECUCAO.md).
- [Resultados e ambiente da validação](RESULTADOS_Q07.md).

## Conferir o código

- `Game.atualizar_boss()` controla a espera, a aparição e o prazo.
- `Game.cumprimentar_boss()` valida presença, alcance e prazo antes de encerrar.
- `Game.encerrar_encontro_boss()` limpa os dados e rearma o próximo ciclo.
- `dano_boss()` usa o fluxo de chances existente, preservando a rodada.

Executar os testes, na raiz do projeto: `python -m pytest -q`.

A imagem e a locomoção do personagem 3D pertencem à etapa R06 do planejamento
de quinta. O ciclo de quarta usa a entidade, suas coordenadas e os avisos da HUD.
