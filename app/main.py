"""
ConectaBairro PWA - Aplicação Principal FastAPI
Ponto de entrada do sistema, configuração de CORS, middlewares e injeção de rotas.
"""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.database import engine, Base, SessionLocal
from app.crud import seed_initial_data
from app.routers import vitrine, prestador, conexao


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicialização do banco de dados relacional e dados iniciais
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_initial_data(db)
    finally:
        db.close()
    yield


app = FastAPI(
    title="ConectaBairro API",
    description="API RESTful para conexão entre moradores e prestadores de serviços locais (AMBE)",
    version="1.0.0",
    lifespan=lifespan
)

# Configuração de CORS para permitir acesso local e PWA
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusão dos roteadores modulares
app.include_router(vitrine.router)
app.include_router(prestador.router)
app.include_router(conexao.router)

# Montagem de arquivos estáticos do PWA
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/", summary="Interface Web PWA")
def read_root():
    """Entrega a aplicação PWA (Single Page Application) diretamente."""
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"mensagem": "Bem-vindo ao ConectaBairro API", "status": "online"}


@app.get("/health", summary="Healthcheck do serviço")
def healthcheck():
    """Endpoint para monitoramento da integridade do sistema em nuvem."""
    return {"status": "healthy", "service": "conectabairro-pwa"}
