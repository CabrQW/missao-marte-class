# language: pt

Funcionalidade: Solicitação de oxigênio no habitat de Marte
  Como astronauta
  Quero solicitar oxigênio
  Para manter os recursos necessários à sobrevivência

  Cenário: Solicitação aprovada com estoque suficiente
    Dado que o habitat possui 1000 unidades de oxigênio
    Quando o astronauta solicita 200 unidades de oxigênio
    Então a solicitação deve ser aprovada
    E o estoque de oxigênio deve ser 800 unidades

  Cenário: Solicitação recusada por falta de oxigênio
    Dado que o habitat possui 100 unidades de oxigênio
    Quando o astronauta solicita 200 unidades de oxigênio
    Então a solicitação deve ser recusada por falta de oxigênio
    E o estoque de oxigênio deve permanecer em 100 unidades
