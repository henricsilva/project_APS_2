from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from controller import evento_controller, inscricao_controller, participante_controller
from exceptions import NaoEncontradoError, RegraNegocioError

app = FastAPI(
    title="API de Eventos Acadêmicos",
    description="API para cadastrar eventos, participantes e inscrições.",
    version="1.0.0",
)

app.include_router(evento_controller.router)
app.include_router(participante_controller.router)
app.include_router(inscricao_controller.router)


# transforma o erro "não encontrado" em 404
@app.exception_handler(NaoEncontradoError)
async def nao_encontrado_handler(request: Request, exc: NaoEncontradoError):
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": exc.mensagem})


# transforma erro de regra de negócio em 400
@app.exception_handler(RegraNegocioError)
async def regra_negocio_handler(request: Request, exc: RegraNegocioError):
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": exc.mensagem})


@app.get("/", tags=["Raiz"])
def raiz():
    return {"mensagem": "API de Eventos Acadêmicos no ar. Documentação em /docs"}
