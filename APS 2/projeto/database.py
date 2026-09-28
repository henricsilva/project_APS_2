# Aqui eu guardo tudo em listas mesmo, sem banco de dados.
# Quando o servidor reinicia os dados somem.

eventos = []
participantes = []
inscricoes = []

# contadores pra gerar o id de cada coisa
_contadores = {"evento": 0, "participante": 0}


def proximo_id(recurso):
    _contadores[recurso] += 1
    return _contadores[recurso]


def resetar():
    # usei isso nos testes pra cada teste começar do zero
    eventos.clear()
    participantes.clear()
    inscricoes.clear()
    for chave in _contadores:
        _contadores[chave] = 0
