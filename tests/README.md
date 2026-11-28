# Testes

Na raiz, com as dependências instaladas: `python -m pytest -q`.
Resultado em 28/11/2026: **186 aprovados**, sem exclusões.

| Arquivo | Cobertura |
| --- | --- |
| test_logica.py | Pontos, chances, nomes, recorde e ranking existentes |
| test_tarefas.py | Banco de perguntas e comparação das respostas |
| test_missoes.py | Digitação, cancelamento, respostas, rodadas e derrota |
| test_spawn_boss.py | Criação, posição válida e integração nos cinco mapas |
| test_encontros_boss.py | Q04-Q07: espera, F, prazo, penalidade e transições |
| test_entrega_quinta_sexta.py | Caminho, colisão, oclusão, pausa real, recursos, áudio, susto e guia |

Os testes usam eventos/superfícies reais do Pygame, drivers SDL dummy e dados
persistentes em diretórios temporários. Os testes de áudio combinam um mixer
simulado para observar chamadas com carregamento de WAVs no mixer real dummy.
Não verificam audição, teclado/mouse físicos ou desempenho na máquina final.
Critérios, diagnóstico inicial e etapas: `docs/aceite_quinta_sexta.md`.
