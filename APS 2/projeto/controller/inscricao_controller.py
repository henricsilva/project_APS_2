from fastapi import APIRouter, status

from model.inscricao import Inscricao
from model.participante import Participante
from service import inscricao_service

router = APIRouter(prefix="/eventos", tags=["Inscrições"])


@router.post(
    "/{evento_id}/inscricoes/{participante_id}",
    response_model=Inscricao,
    status_code=status.HTTP_201_CREATED,
)
def inscrever_participante(evento_id: int, participante_id: int):
    return inscricao_service.inscrever(evento_id, participante_id)


@router.get("/{evento_id}/inscricoes", response_model=list[Participante])
def listar_inscritos(evento_id: int):
    return inscricao_service.listar_participantes(evento_id)


@router.delete(
    "/{evento_id}/inscricoes/{participante_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def cancelar_inscricao(evento_id: int, participante_id: int):
    inscricao_service.cancelar(evento_id, participante_id)
