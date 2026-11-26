# Q03 - Posição e dados do chefe

Base: `main`, commit `77ad2df9335ba7ada70b8b21643eaee5d263f0c2`.

Critérios definidos antes das alterações em `src/`. O Q03 fornece a escolha
da posição e a criação dos dados. `Game.criar_boss()` será o ponto de chamada
para o acionamento por tempo do Q04 e para a renderização da etapa seguinte.

| ID | Critério de aceite | Verificação |
| --- | --- | --- |
| CA01 | `spawn_boss(posicao)` recebe uma tupla e devolve um novo dicionário com `x`, `y` em float e `ativo=True`. | Casos com inteiros, decimais e resultados independentes. |
| CA02 | A posição é escolhida entre as quatro células ortogonais à célula atual do jogador, no centro da célula escolhida. | Quatro direções e diagonais bloqueadas. |
| CA03 | Nenhuma posição fora da grade é aceita. | Casos de borda e cantos. |
| CA04 | Uma célula presente em `world_map` não serve de chão livre. | Paredes e terminais bloqueando vizinhos. |
| CA05 | Sem vizinha livre, não cria dados nem ativa o chefe. | Retorno `None` da busca e `False` da criação. |
| CA06 | A busca funciona nos cinco mapas sem alterar mapa, tarefas ou jogador. | Casos parametrizados com os layouts reais. |
| CA07 | O `Game` guarda o retorno e ativa um único chefe; nova tentativa com chefe ativo preserva os dados existentes. | Criação, repetição e ausência de espaço. |
| CA08 | Uma nova partida limpa o chefe, seu estado, o contador e o aviso anterior. | Reinício com estado preenchido. |
| CA09 | O jogo importa como pacote e como módulo direto; uma partida e seu desenho continuam funcionando. | Imports e quadro real do Pygame com SDL dummy. |

## Método de verificação

1. Executar os testes antes de implementar e registrar a falha de base.
2. Corrigir os bloqueios de importação e de reinício encontrados na `main`.
3. Implementar o Q03 e repetir os mesmos testes.
4. Verificar a compilação e o diff antes da publicação.

Comando: `python -m pytest -q` na raiz do projeto.

## Fase vermelha

Antes de alterar `src/`, a coleta dos testes falhou com `ImportError`:
`jogo.py` importava `temporizador`, mas `boss.py` declara `confirma_tempo`.
Essa falha foi reproduzida em `python -m pytest -q`.
