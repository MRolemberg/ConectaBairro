"""
Endpoints da Tela 1: Vitrine de Serviços e Filtros por Categoria (RF01).
Permite explorar os prestadores locais cadastrados na comunidade.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import CategoriaResponse, PrestadorResponse
from app import crud

router = APIRouter(prefix="/api/vitrine", tags=["Vitrine Comunitária"])


@router.get("/categorias", response_model=List[CategoriaResponse], summary="Listar todas as categorias")
def listar_categorias(db: Session = Depends(get_db)):
    """Retorna a lista de categorias disponíveis para filtro rápido na vitrine."""
    try:
        return crud.get_categorias(db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao carregar categorias comunitárias: {str(e)}"
        )


@router.get("/prestadores", response_model=List[PrestadorResponse], summary="Listar prestadores ativos com filtro")
def listar_prestadores(
    categoria_id: Optional[int] = Query(None, description="Filtrar por ID da categoria de serviço"),
    db: Session = Depends(get_db)
):
    """
    Retorna a lista de profissionais autônomos ativos.
    Permite filtrar por categoria selecionada na barra horizontal.
    """
    try:
        if categoria_id and not crud.get_categoria_by_id(db, categoria_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Categoria selecionada não encontrada."
            )
        return crud.get_prestadores(db, categoria_id=categoria_id, apenas_ativos=True)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar prestadores da vitrine: {str(e)}"
        )
