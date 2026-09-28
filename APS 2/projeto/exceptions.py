# Erros que eu criei pra usar nos services.
# O main.py pega eles e transforma em resposta HTTP.


class NaoEncontradoError(Exception):
    # vira 404
    def __init__(self, mensagem):
        self.mensagem = mensagem


class RegraNegocioError(Exception):
    # vira 400
    def __init__(self, mensagem):
        self.mensagem = mensagem
