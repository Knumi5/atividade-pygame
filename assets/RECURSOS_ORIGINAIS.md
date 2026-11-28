# Recursos de quinta e sexta

Os arquivos abaixo foram criados para este projeto por geração procedural
determinística. Não foram baixados de bancos externos. A temática é o
escritório de **Try // Except**, conforme a proposta da equipe.

| Arquivo | Uso | Formato |
| --- | --- | --- |
| imagens/texturas/1.png | Divisória com placa de código | PNG 256 × 256 |
| imagens/texturas/2.png | Terminal pendente, prompt ciano | PNG 256 × 256 |
| imagens/texturas/3.png | Resposta correta, marca verde | PNG 256 × 256 |
| imagens/texturas/4.png | Resposta incorreta, X vermelho | PNG 256 × 256 |
| imagens/chefe.png | Chefe de paletó, gravata e prancheta | PNG 96 × 160, transparente |
| sons/escritorio_loop.wav | Ambiente grave com quatro notas, loop de 8 s | WAV PCM mono, 11025 Hz, 16 bits |
| sons/chefe_susto.wav | Impacto de ruído e tom ascendente, 0,65 s | WAV PCM mono, 11025 Hz, 16 bits |

Para reproduzir exatamente os arquivos, na raiz do projeto execute:

```bash
python tools/gerar_recursos.py
```

O script usa `pygame`, biblioteca já exigida pelo jogo, e a biblioteca padrão
do Python. Nenhuma geração acontece durante os quadros do jogo. O sprite BMP
preexistente da equipe foi preservado; sua autoria não é atribuída a este script.
A autoria e as alterações do gerador ficam registradas no histórico de commits.
