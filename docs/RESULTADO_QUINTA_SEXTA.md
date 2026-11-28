# Finalização de quinta e sexta - Ricardo

Execução real: **28/11/2026**. Quinta (26/11) e sexta (27/11) identificam os
blocos do planejamento original; os commits não foram retrodatados.
Base integrada: `main` em `bbc37efc478e90a8bb2a199f8d95029c8998f780`.

## Resultado por requisito

| Bloco | Implementação | Evidência |
| --- | --- | --- |
| R06 - chefe visível | Sprite em perspectiva e oclusão por coluna; imagens carregadas uma vez | Câmera à frente/atrás, parede integral/parcial e captura real do renderizador |
| R06 - aproximação | BFS cardinal, centros de células, raio 0,18 e subpassos de até 0,05 célula | Desvio de obstáculo, caminho inexistente, quinas e passo de 2 s |
| R07 - proteção | Pergunta pausa jogador, espera do chefe, prazo e rodada; F bloqueado na pergunta e através de parede | Pergunta real aberta por 20 s simulados sem alterar entidade ou cronômetros |
| R07 - transições | Erro preserva mapa/encontro; troca de rodada invalida rota; reinício limpa estados | Eventos reais do Pygame e regressões de Q03-Q07/missões |
| R08 - texturas | Parede e terminais pendente/correto/incorreto com PNGs reais | Existência, carregamento dos quatro tipos e inspeção visual |
| R09 - áudio | Loop original de 8 s, efeito de 0,65 s, volume inicial de 25%, F10 e -/+ | Mixer simulado para chamadas; WAVs reais carregados pelo mixer SDL dummy |
| R09 - derrota | Susto visual de 1,2 s, uma vez por derrota, sem bloquear eventos | Repetição de encerramento, espera de Enter, novo jogo e captura do resumo |

## Validação executada

- Antes da implementação: **20 cenários novos**, com **9 falhas e 11 erros**
  por funcionalidades/import ausentes, registrados no primeiro patch.
- Após integração do chefe/ranking: **117 aprovados**.
- Após integração das missões: **157 aprovados**.
- Navegação e projeção: **9 cenários dirigidos aprovados**.
- Proteção/transições: **173 aprovados**, com 8 cenários de recursos/áudio
  ainda pendentes naquela etapa.
- Resultado final: **186 aprovados**, sem falhas ou exclusões na suíte completa;
  são **157 casos existentes e 29 casos novos** de quinta/sexta e regressões.
- Verificação adicional nos **cinco layouts reais**: início, chefe e pausa de
  pergunta funcionaram. Capturas incluíram menu, guia, chefe visível/oculto,
  pergunta, susto, resumo e ranking. Dados foram isolados em pasta temporária.
- Na cena controlada, 131 colunas do chefe ficaram visíveis; atrás de uma
  parede real do mapa, nenhuma coluna foi desenhada.
- Amostra local de 120 quadros (raycasting, cenário e HUD, SDL dummy): mediana
  **14,95 ms**, percentil 95 **18,03 ms**. Não inclui apresentação de janela
  ou controles físicos e não garante desempenho na máquina da apresentação.

Comando principal: `python -m pytest -q`.
Ambiente: Python 3.12, Pygame 2.6.1, pytest 9.2.0, Linux, SDL dummy.

## Revisão dos patches

1. Testes e critérios antes de alterar implementação.
2. Integração do ciclo Q03-Q07 com ranking e correções de desenho/ESC.
3. Integração do painel de missões com o renderizador texturizado atual.
4. Navegação e sprite do chefe com oclusão.
5. Proteção, linhas de visão, limpeza de rotas e remoção dos atalhos de debug.
6. Recursos originais e gerador reproduzível.
7. Trilha, volume, susto e guia acessível.
8. Documentação real da entrega, comandos e evidências.

Os PRs anteriores permanecem no histórico. A branch de finalização integra
seus conteúdos em patches coesos sobre a main; não altera a main diretamente.

## Conferência presencial antes da entrega

- [ ] Testar W/A/S/D, mouse, E e F na máquina da apresentação.
- [ ] Ouvir a trilha por mais de 8 s e verificar a emenda do loop.
- [ ] Conferir volume de 25%, -/+, F10 e efeito do susto com o áudio real.
- [ ] Jogar uma rodada completa, errar uma tarefa, esperar o chefe e chegar à derrota.
- [ ] Revisar o PR integrado antes de fazer merge; evitar integrar os PRs antigos de novo.
- [ ] Confirmar a decisão da equipe sobre a regra especial de pontuação do Gustavo,
  preservada da main e descrita no README.
- [ ] Preparar e enviar a versão validada até **domingo, 29/11, às 23:59**;
  meta interna do planejamento: **21:00**.

Essas conferências e a entrega ao professor não são marcadas como realizadas
pelos testes automatizados. Não há áudio físico audível nem teclado/mouse
físicos neste ambiente.
