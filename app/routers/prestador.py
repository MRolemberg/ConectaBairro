"""
Endpoints da Tela 2: Auto-Cadastro de Prestador de Serviços (RF03, RNF01, RNF02).
Implementa validações estritas, sanitização de entrada e prevenção a injeções maliciosas.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import PrestadorCreate, PrestadorResponse
from app import crud

router = APIRouter(prefix="/api/prestadores", tags=["Prestadores de Serviço"])


@router.post(
    "",
    response_model=PrestadorResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar novo prestador autônomo"
)
def cadastrar_prestador(prestador_in: PrestadorCreate, db: Session = Depends(get_db)):
    """
    Cadastra um trabalhador autônomo na vitrine comunitária.
    Aplica validações de regex no telefone e sanitização no nome/descrição.
    """
    # Valida se a categoria informada existe no banco de dados
    categoria = crud.get_categoria_by_id(db, prestador_in.categoria_id)
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Categoria de serviço informada não é válida ou não existe."
        )

    try:
        novo_prestador = crud.create_prestador(db, prestador_in)
        return novo_prestador
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Falha ao persistir cadastro do prestador: {str(e)}"
        )


@router.get(
    "/{prestador_id}",
    response_model=PrestadorResponse,
    summary="Obter detalhes de um prestador"
)
def obter_prestador(prestador_id: int, db: Session = Depends(get_db)):
    """Busca o perfil completo de um prestador pelo seu identificador único."""
    prestador = crud.get_prestador_by_id(db, prestador_id)
    if not prestador:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Prestador com identificador {prestador_id} não encontrado."
        )
    return prestador
