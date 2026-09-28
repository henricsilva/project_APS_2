import database as db
from exceptions import NaoEncontradoError, RegraNegocioError
from model.evento import Evento


def listar():
    return list(db.eventos)


def buscar(evento_id):
    for evento in db.eventos:
        if evento.id == evento_id:
            return evento
    raise NaoEncontradoError("Evento não encontrado.")


def criar(dados):
    evento = Evento(id=db.proximo_id("evento"), **dados.model_dump())
    db.eventos.append(evento)
    return evento


def atualizar(evento_id, dados):
    evento = buscar(evento_id)
    # não pode diminuir a capacidade pra menos do que já tem de inscritos
    inscritos = sum(1 for i in db.inscricoes if i.evento_id == evento_id)
    if dados.capacidade < inscritos:
        raise RegraNegocioError(
            f"A capacidade não pode ser menor que o número de inscritos ({inscritos})."
        )
    atualizado = Evento(id=evento.id, **dados.model_dump())
    db.eventos[db.eventos.index(evento)] = atualizado
    return atualizado


def excluir(evento_id):
    evento = buscar(evento_id)
    db.eventos.remove(evento)
    # se apaga o evento, apaga as inscrições dele também
    db.inscricoes[:] = [i for i in db.inscricoes if i.evento_id != evento_id]
