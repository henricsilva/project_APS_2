import os
import sys

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import database  # noqa: E402
from main import app  # noqa: E402

client = TestClient(app)

EVENTO = {
    "titulo": "Introdução ao FastAPI",
    "descricao": "Palestra sobre APIs.",
    "data": "2026-11-15",
    "horario": "19:30:00",
    "local": "Auditório A",
    "capacidade": 2,
    "categoria": "Palestra",
}


def participante(n: int) -> dict:
    return {"nome": f"Aluno {n}", "email": f"aluno{n}@example.com", "curso": "ADS"}


@pytest.fixture(autouse=True)
def limpar():
    database.resetar()


def test_crud_evento():
    r = client.post("/eventos", json=EVENTO)
    assert r.status_code == 201
    evento_id = r.json()["id"]

    assert client.get("/eventos").json()[0]["id"] == evento_id
    assert client.get(f"/eventos/{evento_id}").status_code == 200

    r = client.put(f"/eventos/{evento_id}", json={**EVENTO, "titulo": "Novo título"})
    assert r.status_code == 200 and r.json()["titulo"] == "Novo título"

    assert client.delete(f"/eventos/{evento_id}").status_code == 204
    r = client.get(f"/eventos/{evento_id}")
    assert r.status_code == 404
    assert r.json() == {"detail": "Evento não encontrado."}


def test_crud_participante():
    r = client.post("/participantes", json=participante(1))
    assert r.status_code == 201
    pid = r.json()["id"]
    assert client.get(f"/participantes/{pid}").status_code == 200
    r = client.put(f"/participantes/{pid}", json={**participante(1), "curso": "Direito"})
    assert r.json()["curso"] == "Direito"
    assert client.delete(f"/participantes/{pid}").status_code == 204
    assert client.get(f"/participantes/{pid}").status_code == 404


def test_email_duplicado():
    client.post("/participantes", json=participante(1))
    r = client.post("/participantes", json=participante(1))
    assert r.status_code == 400


@pytest.mark.parametrize(
    "alteracao",
    [
        {"titulo": ""},
        {"titulo": "   "},
        {"capacidade": 0},
        {"capacidade": -5},
        {"data": "31/02/2026"},
        {"categoria": "Inexistente"},
    ],
)
def test_evento_invalido(alteracao):
    assert client.post("/eventos", json={**EVENTO, **alteracao}).status_code == 422


def test_evento_campo_obrigatorio_ausente():
    dados = {k: v for k, v in EVENTO.items() if k != "local"}
    assert client.post("/eventos", json=dados).status_code == 422


@pytest.mark.parametrize(
    "alteracao", [{"nome": ""}, {"email": "invalido"}, {"curso": ""}]
)
def test_participante_invalido(alteracao):
    assert client.post("/participantes", json={**participante(1), **alteracao}).status_code == 422


def test_inscricao_fluxo_completo():
    ev = client.post("/eventos", json=EVENTO).json()["id"]
    p = [client.post("/participantes", json=participante(i)).json()["id"] for i in (1, 2, 3)]

    assert client.post(f"/eventos/{ev}/inscricoes/{p[0]}").status_code == 201

    r = client.post(f"/eventos/{ev}/inscricoes/{p[0]}")
    assert r.status_code == 400
    assert r.json() == {"detail": "Participante já está inscrito neste evento."}

    assert client.post(f"/eventos/{ev}/inscricoes/{p[1]}").status_code == 201

    r = client.post(f"/eventos/{ev}/inscricoes/{p[2]}")
    assert r.status_code == 400
    assert r.json() == {"detail": "Não existem vagas disponíveis para este evento."}

    inscritos = client.get(f"/eventos/{ev}/inscricoes").json()
    assert [i["id"] for i in inscritos] == [p[0], p[1]]

    assert client.delete(f"/eventos/{ev}/inscricoes/{p[0]}").status_code == 204
    assert client.post(f"/eventos/{ev}/inscricoes/{p[2]}").status_code == 201


def test_inscricao_inexistentes():
    ev = client.post("/eventos", json=EVENTO).json()["id"]
    r = client.post("/eventos/999/inscricoes/1")
    assert r.status_code == 404 and r.json() == {"detail": "Evento não encontrado."}
    r = client.post(f"/eventos/{ev}/inscricoes/999")
    assert r.status_code == 404 and r.json() == {"detail": "Participante não encontrado."}
    assert client.get("/eventos/999/inscricoes").status_code == 404


def test_reduzir_capacidade_abaixo_dos_inscritos():
    ev = client.post("/eventos", json=EVENTO).json()["id"]
    for i in (1, 2):
        pid = client.post("/participantes", json=participante(i)).json()["id"]
        client.post(f"/eventos/{ev}/inscricoes/{pid}")
    r = client.put(f"/eventos/{ev}", json={**EVENTO, "capacidade": 1})
    assert r.status_code == 400
