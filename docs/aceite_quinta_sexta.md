# Quinta e sexta - critérios e plano de patches

Base de integração: `main` em `bbc37efc478e90a8bb2a199f8d95029c8998f780`.
Escopo de Ricardo: R06/R07 (26/11) e R08/R09 (27/11), finalizado em 28/11.
Critérios e cenários escritos antes das alterações de implementação.

| ID | Entrega | Critério de aceite |
| --- | --- | --- |
| QSF01 | Integração | Missões e encontros anteriores funcionam junto ao ranking da main; imports e menu iniciam. |
| QSF02 | R06 | Chefe aparece em perspectiva, fica oculto por paredes e desaparece quando está atrás da câmera. |
| QSF03 | R06 | Chefe segue um caminho por células livres, sem atravessar paredes ou cortar quinas. |
| QSF04 | R07 | Pergunta aberta pausa movimento do chefe, espera, prazo, jogador e rodada; retorno não acumula punição. |
| QSF05 | R07 | F respeita alcance, prazo e paredes; cumprimento resolve uma vez e erro de missão preserva o encontro. |
| QSF06 | R07 | Troca de mapa, reinício, zero chances e ranking preservam estados consistentes. |
| QSF07 | R08 | Recursos reais de paredes e terminais pendente, correto e incorreto são carregados e reutilizados. |
| QSF08 | R09 | Trilha original toca em loop e não é recarregada ou reiniciada por quadro. |
| QSF09 | R09 | Volume e mudo funcionam; falta de dispositivo de áudio não impede a partida. |
| QSF10 | R09 | Derrota dispara um único jumpscare visual/sonoro; depois mostra Game Over, sem bloquear eventos. |

## Organização dos commits

1. `test(entrega)`: critérios e testes de quinta/sexta.
2. `fix(integracao)`: ciclo do chefe e ranking na versão atual.
3. `feat(missoes)`: perguntas integradas aos encontros.
4. `feat(boss)`: aproximação por caminho livre e projeção com oclusão.
5. `fix(jogo)`: proteção das missões e consistência das transições.
6. `feat(assets)`: texturas, sprite e sons originais reproduzíveis.
7. `feat(audio)`: trilha em loop, volume e jumpscare final.
8. `docs(entrega)`: resultado final, controles e instruções de revisão.

Cada commit explica o comportamento e a validação feita. Recursos existentes
da equipe são integrados; o histórico dos PRs anteriores permanece preservado.

## Diagnóstico inicial

Antes da implementação: 20 cenários novos, com 9 falhas e 11 erros de preparação.
As falhas incluem APIs de navegação/áudio e recursos ausentes; os erros de
preparação apontam o import inexistente de `temporizador` na main.
Esse resultado registra a etapa inicial de TDD, não uma validação de entrega.
