import database as db
from exceptions import NaoEncontradoError, RegraNegocioError
from model.inscricao import Inscricao
from model.participante import Participante
from service import evento_service, participante_service


def _buscar_inscricao(evento_id, participante_id):
    for i in db.inscricoes:
        if i.evento_id == evento_id and i.participante_id == participante_id:
            return i
    return None


def inscrever(evento_id, participante_id):
    # primeiro vejo se o evento e o participante existem
    # (se não existir, o buscar já lança o erro 404)
    evento = evento_service.buscar(evento_id)
    participante_service.buscar(participante_id)

    # não deixa inscrever duas vezes
    if _buscar_inscricao(evento_id, participante_id):
        raise RegraNegocioError("Participante já está inscrito neste evento.")

    # conta quantos já estão inscritos pra ver se ainda tem vaga
    total = sum(1 for i in db.inscricoes if i.evento_id == evento_id)
    if total >= evento.capacidade:
        raise RegraNegocioError("Não existem vagas disponíveis para este evento.")

    inscricao = Inscricao(evento_id=evento_id, participante_id=participante_id)
    db.inscricoes.append(inscricao)
    return inscricao


def listar_participantes(evento_id):
    evento_service.buscar(evento_id)
    return [
        participante_service.buscar(i.participante_id)
        for i in db.inscricoes
        if i.evento_id == evento_id
    ]


def cancelar(evento_id, participante_id):
    evento_service.buscar(evento_id)
    participante_service.buscar(participante_id)
    inscricao = _buscar_inscricao(evento_id, participante_id)
    if not inscricao:
        raise NaoEncontradoError("Inscrição não encontrada.")
    db.inscricoes.remove(inscricao)
