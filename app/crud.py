"""
Operações de acesso a dados (CRUD) seguras utilizando o ORM do SQLAlchemy.
Garante queries parametrizadas contra SQL Injection.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from app.models import Categoria, Prestador, ConexaoRegistro
from app.schemas import PrestadorCreate


def get_categorias(db: Session) -> List[Categoria]:
    return db.query(Categoria).all()


def get_categoria_by_id(db: Session, categoria_id: int) -> Optional[Categoria]:
    return db.query(Categoria).filter(Categoria.id == categoria_id).first()


def get_categoria_by_slug(db: Session, slug: str) -> Optional[Categoria]:
    return db.query(Categoria).filter(Categoria.slug == slug).first()


def get_prestadores(db: Session, categoria_id: Optional[int] = None, apenas_ativos: bool = True) -> List[Prestador]:
    query = db.query(Prestador)
    if apenas_ativos:
        query = query.filter(Prestador.ativo == True)
    if categoria_id:
        query = query.filter(Prestador.categoria_id == categoria_id)
    return query.order_by(Prestador.id.desc()).all()


def get_prestador_by_id(db: Session, prestador_id: int) -> Optional[Prestador]:
    return db.query(Prestador).filter(Prestador.id == prestador_id).first()


def create_prestador(db: Session, prestador_data: PrestadorCreate) -> Prestador:
    db_prestador = Prestador(
        nome=prestador_data.nome,
        telefone=prestador_data.telefone,
        descricao=prestador_data.descricao,
        categoria_id=prestador_data.categoria_id,
        ativo=True
    )
    db.add(db_prestador)
    db.commit()
    db.refresh(db_prestador)
    return db_prestador


def create_conexao(db: Session, prestador_id: int) -> ConexaoRegistro:
    conexao = ConexaoRegistro(prestador_id=prestador_id, status="iniciada")
    db.add(conexao)
    db.commit()
    db.refresh(conexao)
    return conexao


def seed_initial_data(db: Session):
    """Popula categorias essenciais e prestadores iniciais de demonstração."""
    if db.query(Categoria).count() == 0:
        categorias = [
            Categoria(nome="Pintura", slug="pintura", icone="paint-roller"),
            Categoria(nome="Limpeza", slug="limpeza", icone="broom"),
            Categoria(nome="Elétrica", slug="eletrica", icone="bolt"),
            Categoria(nome="Hidráulica", slug="hidraulica", icone="wrench"),
            Categoria(nome="Marcenaria", slug="marcenaria", icone="hammer"),
        ]
        db.add_all(categorias)
        db.commit()

        # Prestadores iniciais de exemplo na comunidade AMBE
        cat_eletrica = db.query(Categoria).filter_by(slug="eletrica").first()
        cat_pintura = db.query(Categoria).filter_by(slug="pintura").first()
        cat_limpeza = db.query(Categoria).filter_by(slug="limpeza").first()

        prestadores = [
            Prestador(
                nome="Carlos Eduardo de Oliveira",
                telefone="11987654321",
                descricao="Eletricista residencial com mais de 20 anos de experiência na região da AMBE.",
                categoria_id=cat_eletrica.id if cat_eletrica else 1,
                ativo=True
            ),
            Prestador(
                nome="Maria Conceição Santos",
                telefone="11976543210",
                descricao="Diarista e especialista em limpeza pós-obra. Atendimento ágil e de confiança.",
                categoria_id=cat_limpeza.id if cat_limpeza else 2,
                ativo=True
            ),
            Prestador(
                nome="José Roberto Pereira",
                telefone="11965432109",
                descricao="Pintor profissional, acabamento fino residencial e textura externa.",
                categoria_id=cat_pintura.id if cat_pintura else 3,
                ativo=True
            )
        ]
        db.add_all(prestadores)
        db.commit()
