"""
Modelos ORM relacionais do SQLAlchemy para o ConectaBairro.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.database import Base


class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(50), unique=True, nullable=False, index=True)
    slug = Column(String(50), unique=True, nullable=False, index=True)
    icone = Column(String(30), default="tools")

    prestadores = relationship("Prestador", back_populates="categoria")


class Prestador(Base):
    __tablename__ = "prestadores"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    telefone = Column(String(20), nullable=False)
    descricao = Column(Text, nullable=False)
    ativo = Column(Boolean, default=True)
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=False)
    data_cadastro = Column(DateTime, default=datetime.utcnow)

    categoria = relationship("Categoria", back_populates="prestadores")
    conexoes = relationship("ConexaoRegistro", back_populates="prestador")


class ConexaoRegistro(Base):
    __tablename__ = "conexoes_registros"

    id = Column(Integer, primary_key=True, index=True)
    prestador_id = Column(Integer, ForeignKey("prestadores.id"), nullable=False)
    status = Column(String(30), default="iniciada")
    data_criacao = Column(DateTime, default=datetime.utcnow)

    prestador = relationship("Prestador", back_populates="conexoes")
