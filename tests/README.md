# Testes

Esta pasta contem testes automatizados do projeto.

## Arquivos

- `test_logica.py`: valida funcoes puras de logica em `src/funcoes.py`.
- `test_spawn_boss.py`: valida os dados do chefe, a escolha da posição nos cinco mapas, criação única, reinício e inicialização do jogo.

## Como executar

```bash
python -m pytest
```

## Boas praticas

- Crie testes para toda regra de pontuacao, vidas e condicoes de fim de jogo.
- Prefira funcoes pequenas e testaveis no modulo `src/funcoes.py`.
