from fastapi import APIRouter, status

from model.evento import Evento, EventoCreate
from service import evento_service

router = APIRouter(prefix="/eventos", tags=["Eventos"])


@router.post("", response_model=Evento, status_code=status.HTTP_201_CREATED)
def cadastrar_evento(dados: EventoCreate):
    return evento_service.criar(dados)


@router.get("", response_model=list[Evento])
def listar_eventos():
    return evento_service.listar()


@router.get("/{evento_id}", response_model=Evento)
def consultar_evento(evento_id: int):
    return evento_service.buscar(evento_id)


@router.put("/{evento_id}", response_model=Evento)
def atualizar_evento(evento_id: int, dados: EventoCreate):
    return evento_service.atualizar(evento_id, dados)


@router.delete("/{evento_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_evento(evento_id: int):
    evento_service.excluir(evento_id)
