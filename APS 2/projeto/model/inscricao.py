from pydantic import BaseModel


class Inscricao(BaseModel):
    evento_id: int
    participante_id: int
