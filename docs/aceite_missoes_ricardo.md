# Missões de programação - pendências de 23 e 24/11

## Escopo e requisitos

Implementar R01/R02/R03 do Gantt de Ricardo: contrato das missões, painel e
cinco perguntas, com resposta, pontuação e resolução única dos terminais.
O chefe usará `game.em_tarefa` para consultar a proteção durante perguntas;
seu personagem, aparição e movimento pertencem à etapa seguinte.

As alterações partem de `4a20002`, preservando o nome e a persistência do
ranking feitos por Fernando e a HUD/guia feitos por Igor.

| ID | Critério de aceite | Evidência prevista |
| --- | --- | --- |
| CA01 | E ou Mouse 1 perto de um terminal abre pergunta, sem concluir nem pontuar. O evento de abertura não vira resposta. | Eventos reais do Pygame em `test_missoes.py`. |
| CA02 | Busca usa alcance de 1,8 e não altera o mapa. Terminais distantes ou já resolvidos não abrem. | Casos de distância, busca e terminal resolvido. |
| CA03 | Cinco questões distintas têm ID, enunciado e resposta; comparação remove espaços externos e ignora maiúsculas/minúsculas. | `test_tarefas.py`. |
| CA04 | Campo aceita texto imprimível, Backspace e até 40 caracteres. Resposta vazia mantém a pergunta aberta sem penalidade. | Digitação, limite e envio vazio. |
| CA05 | Movimento, câmera, cronômetro e atalhos do mapa ficam bloqueados durante a pergunta; eventos e relógio de quadros continuam funcionando. | Atualização pausada e eventos durante o painel. |
| CA06 | ESC cancela somente a pergunta; preserva posição, pontos, chances e pendências. Reabrir o terminal mantém a questão. | Cancelamento e reabertura. |
| CA07 | Resposta correta resolve uma vez, soma um ponto e não desconta chance. | Acerto e Enter repetido. |
| CA08 | Resposta errada resolve o terminal sem contar como acerto e tira uma chance, preservando mapa, tempo e demais tarefas enquanto houver chances. | Erro com tarefas restantes. |
| CA09 | HUD diferencia tarefas resolvidas de acertos; erro não fica marcado como tarefa acertada. | Estado do mapa, textos da HUD e revisão visual. |
| CA10 | Ao resolver o último terminal com chances restantes, a rodada avança uma vez, mantém pontos/chances e reinicia tarefas/tempo conforme as regras existentes. | Última resposta correta/errada e rodada completa. |
| CA11 | Se o erro zera as chances, abre Game Over e preserva a gravação do recorde e do ranking. | Arquivos temporários e derrota por erro. |
| CA12 | Nova partida limpa painel/resposta/feedback e restaura rodada, pontos e chances. | Reinício com pergunta aberta. |
| CA13 | Painel desenha enunciado, campo e comandos dentro da janela, sem exibir a resposta esperada ou o dicionário interno. | Captura dos textos renderizados e revisão visual. |
| CA14 | Fechar janela continua encerrando o programa durante a pergunta; fora dela, menu, edição de nome e guia mantêm o funcionamento. | Eventos de encerramento e regressão do menu. |

## Decisões de implementação

- Enter confirma; ESC cancela sem penalidade. Resposta vazia não é enviada.
- Cada terminal guarda sua pergunta até a rodada acabar, inclusive após cancelar.
- A pergunta pede apenas a palavra-chave/nome, sem parênteses.
- Erro remove o terminal das pendências e o distingue de um acerto. A HUD
  mostra resolvidas/total e acertos separadamente.
- Usar o único loop de eventos do jogo; não usar `input()` ou loop bloqueante.
- A pausa tem uma fonte de verdade: `painel_pergunta is not None`.
- Testes não escrevem nos arquivos de dados reais: recorde e ranking usam
  diretórios temporários.

## Execução e resultado

1. Escrever critérios e testes antes das alterações em `src/`.
2. Executar a versão de base para reproduzir as falhas (fase vermelha).
3. Implementar por etapas e executar os mesmos testes (fase verde).
4. Revisar o painel visualmente e registrar o resultado final neste documento.

Comando: `python -m pytest -q`.

Fase vermelha, antes de alterar `src/`: **35 falhas e 2 aprovações** em
`python -m pytest -q`. As falhas incluem conclusão automática ao interagir,
ausência do banco de perguntas e ausência do fluxo de resposta/cancelamento.
Implementação ainda não validada nesta etapa.
