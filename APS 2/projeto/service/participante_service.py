import database as db
from exceptions import NaoEncontradoError, RegraNegocioError
from model.participante import Participante


def listar():
    return list(db.participantes)


def buscar(participante_id):
    for participante in db.participantes:
        if participante.id == participante_id:
            return participante
    raise NaoEncontradoError("Participante não encontrado.")


# ignorar_id serve pro PUT: o participante pode manter o próprio e-mail
def _validar_email_unico(email, ignorar_id=None):
    for p in db.participantes:
        if p.email.lower() == email.lower() and p.id != ignorar_id:
            raise RegraNegocioError("Já existe um participante com este e-mail.")


def criar(dados):
    _validar_email_unico(dados.email)
    participante = Participante(id=db.proximo_id("participante"), **dados.model_dump())
    db.participantes.append(participante)
    return participante


def atualizar(participante_id, dados):
    participante = buscar(participante_id)
    _validar_email_unico(dados.email, ignorar_id=participante_id)
    atualizado = Participante(id=participante.id, **dados.model_dump())
    db.participantes[db.participantes.index(participante)] = atualizado
    return atualizado


def excluir(participante_id):
    participante = buscar(participante_id)
    db.participantes.remove(participante)
    db.inscricoes[:] = [i for i in db.inscricoes if i.participante_id != participante_id]
