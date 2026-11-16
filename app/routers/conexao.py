"""
Endpoints da Tela 3: Confirmação e Conexão via WhatsApp (RF02, RA01).
Gera o link padronizado para abertura de chat direto sem intermediários,
registrando a métrica de geração de oportunidade comunitária.
"""

import urllib.parse
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import ConexaoCreate, ConexaoResponse
from app import crud

router = APIRouter(prefix="/api/conexao", tags=["Conexão WhatsApp"])


@router.post(
    "/iniciar",
    response_model=ConexaoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar e iniciar conexão com o prestador via WhatsApp"
)
def iniciar_conexao(dados: ConexaoCreate, db: Session = Depends(get_db)):
    """
    Registra a solicitação de contato e gera o link direto da API do WhatsApp.
    O formato do link gerado é https://wa.me/55{telefone}?text={mensagem_codificada}.
    """
    prestador = crud.get_prestador_by_id(db, dados.prestador_id)
    if not prestador:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prestador selecionado não foi localizado para conexão."
        )

    try:
        registro = crud.create_conexao(db, prestador.id)

        # Montagem do link dinâmico padronizado do WhatsApp
        mensagem = (
            f"Olá {prestador.nome}! Vi seu anúncio no ConectaBairro PWA "
            f"e gostaria de solicitar um orçamento para serviços de {prestador.categoria.nome if prestador.categoria else 'serviços gerais'}."
        )
        mensagem_encoded = urllib.parse.quote(mensagem)
        whatsapp_url = f"https://wa.me/55{prestador.telefone}?text={mensagem_encoded}"

        return ConexaoResponse(
            id=registro.id,
            prestador_id=prestador.id,
            nome_prestador=prestador.nome,
            whatsapp_url=whatsapp_url,
            mensagem_status="Conexão gerada com sucesso",
            status="ativa"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Falha ao gerar link de conexão: {str(e)}"
        )
