from datetime import date, time
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class Categoria(str, Enum):
    palestra = "Palestra"
    workshop = "Workshop"
    minicurso = "Minicurso"
    seminario = "Seminário"
    competicao = "Competição"


class EventoBase(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        json_schema_extra={
            "example": {
                "titulo": "Introdução ao FastAPI",
                "descricao": "Palestra sobre construção de APIs RESTful.",
                "data": "2026-11-15",
                "horario": "19:30:00",
                "local": "Auditório A",
                "capacidade": 50,
                "categoria": "Palestra",
            }
        },
    )

    titulo: str = Field(..., min_length=1, max_length=150)
    descricao: str = Field(default="", max_length=1000)
    data: date
    horario: time
    local: str = Field(..., min_length=1, max_length=150)
    capacidade: int = Field(..., gt=0, description="Deve ser maior que zero")
    categoria: Categoria


class EventoCreate(EventoBase):
    # usado no POST e no PUT (sem o id)
    pass


class Evento(EventoBase):
    # o que a API devolve (com id)
    id: int
