# project_APS_2

Trabalho APS 2

## O que usei

- Python 3.10+
- FastAPI
- Pydantic (pra validar os dados)
- Uvicorn (pra rodar o servidor)
- Pytest e HTTPX (pros testes)

## Como o projeto está organizado

```
projeto/
├── main.py            # cria o app e trata os erros
├── database.py        # dados guardados em listas (memória)
├── exceptions.py      # os dois erros que criei (404 e 400)
├── controller/        # rotas
├── model/             # modelos e validações
├── service/           # regras de negócio
└── tests/test_api.py  # testes
```

Separei em camadas pra não misturar tudo: o **controller** só recebe a requisição
e chama o **service**, que tem as regras (tipo checar se ainda tem vaga). O **model**
define e valida os dados. Quando o service encontra um problema ele lança um erro,
e o `main.py` transforma esse erro na resposta HTTP certa.

## Como rodar

```bash
cd projeto
python -m venv .venv
source .venv/bin/activate      # no Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Depois é só abrir http://127.0.0.1:8000/docs, que tem a documentação do Swagger
e dá pra testar todas as rotas por lá.

Pra rodar os testes:

```bash
python -m pytest -v
```

## Rotas

**Eventos**

| Método | Rota            | O que faz         |
|--------|-----------------|-------------------|
| POST   | `/eventos`      | cadastra evento   |
| GET    | `/eventos`      | lista eventos     |
| GET    | `/eventos/{id}` | busca um evento   |
| PUT    | `/eventos/{id}` | atualiza evento   |
| DELETE | `/eventos/{id}` | exclui evento     |

**Participantes** (mesmas rotas, em `/participantes`)

**Inscrições**

| Método | Rota                                                | O que faz                       |
|--------|-----------------------------------------------------|---------------------------------|
| POST   | `/eventos/{evento_id}/inscricoes/{participante_id}` | inscreve participante no evento |
| GET    | `/eventos/{evento_id}/inscricoes`                   | lista quem está inscrito        |
| DELETE | `/eventos/{evento_id}/inscricoes/{participante_id}` | cancela a inscrição (extra)     |

## Validações e regras

- `titulo`, `local`, `nome` e `curso` não podem ficar vazios
- `email` precisa ser válido e não pode repetir entre participantes
- `capacidade` tem que ser maior que zero
- `data` no formato `AAAA-MM-DD` e `horario` no formato `HH:MM:SS`
- `categoria`: Palestra, Workshop, Minicurso, Seminário ou Competição

Na hora de inscrever, a API confere: se o evento existe, se o participante existe,
se ele já não está inscrito e se ainda tem vaga. Se excluir um evento ou participante,
as inscrições ligadas a ele também somem. Também não dá pra diminuir a capacidade
de um evento pra menos do que o número de inscritos.

## Códigos de status

| Código | Quando acontece                                             |
|--------|-------------------------------------------------------------|
| 200    | deu certo (consulta, lista, atualização)                    |
| 201    | criou algo / fez a inscrição                                |
| 204    | excluiu                                                     |
| 400    | quebrou uma regra (já inscrito, sem vagas, e-mail repetido) |
| 404    | evento, participante ou inscrição não existe                |
| 422    | dados inválidos                                             |

## Exemplos

Cadastrar evento (`POST /eventos`):

```json
{
  "titulo": "Introdução ao FastAPI",
  "descricao": "Palestra sobre construção de APIs RESTful.",
  "data": "2026-11-15",
  "horario": "19:30:00",
  "local": "Auditório A",
  "capacidade": 2,
  "categoria": "Palestra"
}
```

Cadastrar participante (`POST /participantes`):

```json
{
  "nome": "Ana Souza",
  "email": "ana.souza@example.com",
  "curso": "Engenharia de Software"
}
```

Inscrever (`POST /eventos/1/inscricoes/1`) devolve `201`:

```json
{ "evento_id": 1, "participante_id": 1 }
```

Se tentar inscrever de novo, devolve `400`:

```json
{ "detail": "Participante já está inscrito neste evento." }
```

## Limitações

Os dados ficam só na memória, então perdem quando o servidor reinicia. Também não
fiz autenticação. Uma melhoria futura seria usar um banco de dados de verdade
(SQLite, por exemplo).

## Autor

- Henrique C Silva
