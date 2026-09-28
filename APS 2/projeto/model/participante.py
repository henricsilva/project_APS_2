from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ParticipanteBase(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        json_schema_extra={
            "example": {
                "nome": "Ana Souza",
                "email": "ana.souza@example.com",
                "curso": "Engenharia de Software",
            }
        },
    )

    nome: str = Field(..., min_length=1, max_length=120)
    email: EmailStr
    curso: str = Field(..., min_length=1, max_length=120)


class ParticipanteCreate(ParticipanteBase):
    # usado no POST e no PUT (sem o id)
    pass


class Participante(ParticipanteBase):
    # o que a API devolve (com id)
    id: int
