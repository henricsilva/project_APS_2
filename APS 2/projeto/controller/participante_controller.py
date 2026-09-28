from fastapi import APIRouter, status

from model.participante import Participante, ParticipanteCreate
from service import participante_service

router = APIRouter(prefix="/participantes", tags=["Participantes"])


@router.post("", response_model=Participante, status_code=status.HTTP_201_CREATED)
def cadastrar_participante(dados: ParticipanteCreate):
    return participante_service.criar(dados)


@router.get("", response_model=list[Participante])
def listar_participantes():
    return participante_service.listar()


@router.get("/{participante_id}", response_model=Participante)
def consultar_participante(participante_id: int):
    return participante_service.buscar(participante_id)


@router.put("/{participante_id}", response_model=Participante)
def atualizar_participante(participante_id: int, dados: ParticipanteCreate):
    return participante_service.atualizar(participante_id, dados)


@router.delete("/{participante_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_participante(participante_id: int):
    participante_service.excluir(participante_id)
