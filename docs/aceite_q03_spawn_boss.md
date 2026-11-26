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

Após corrigir o import e a atribuição do contador, a mesma suíte apresentou
**25 falhas e 1 aprovação**: faltavam o retorno de `spawn_boss`, a busca da
posição e a criação integrada. Foi acrescentada também uma regressão para
impedir uma tentativa de criação no menu, sem mapa carregado.

## Validação final

- **27 testes aprovados**, nenhuma falha, em `python -m pytest -q`.
- CA01 a CA09 aprovados pelos casos de dados, seleção, limites, cinco mapas,
  criação única, reinício, importação e desenho de um quadro texturizado.
- `git diff --check` e compilação de `src/` e `tests/` aprovados.
- Ambiente: Python 3.12, Pygame 2.6.1 e SDL de vídeo/áudio `dummy`.

## Checklist do Q03

- [x] Parâmetro `posicao` recebe a tupla `(x, y)`.
- [x] `Game.escolher_posicao_boss()` usa a célula atual do jogador.
- [x] São examinadas apenas as células de cima, baixo, esquerda e direita.
- [x] Candidatas ficam dentro da grade e fora de `world_map`.
- [x] A posição retornada fica no centro da célula escolhida.
- [x] Sem vizinha livre, a busca retorna `None` e não há criação.
- [x] `spawn_boss()` devolve um novo dicionário com `x`, `y` e `ativo`.
- [x] `Game.criar_boss()` guarda os dados e informa se houve criação.

## Como usar

Durante uma partida carregada, `game.criar_boss()` tenta criar a entidade:

- Retorna `True` ao guardar os dados em `game.boss` e ativar `boss_ativo`.
- Retorna `False` sem vizinha livre, fora da partida ou com chefe já ativo.
- `game.boss` contém `x` e `y` em coordenadas do mapa e `ativo=True`.
- Nova partida limpa os dados, o estado, o contador e o aviso anterior.

O acionamento dessa chamada aos 30 segundos será feito no Q04. A imagem do
chefe em 3D será conectada na etapa de renderização; o Q03 entrega seus dados
e a posição válida, sem alterar o desenho atual das paredes e texturas.
