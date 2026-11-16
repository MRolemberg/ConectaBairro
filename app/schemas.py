"""
Schemas Pydantic para validação estrita de entrada/saída de dados,
sanitização de inputs e prevenção de XSS/injeções maliciosas.
"""

import re
import html
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator, ConfigDict


class CategoriaBase(BaseModel):
    nome: str = Field(..., min_length=2, max_length=50, description="Nome da categoria")
    slug: str = Field(..., min_length=2, max_length=50, description="Identificador amigável")
    icone: Optional[str] = Field("tools", max_length=30)


class CategoriaResponse(CategoriaBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class PrestadorBase(BaseModel):
    nome: str = Field(..., min_length=3, max_length=100, description="Nome do prestador")
    telefone: str = Field(..., min_length=10, max_length=20, description="Telefone com DDD (somente números ou formato padrão)")
    descricao: str = Field(..., min_length=10, max_length=500, description="Descrição detalhada do serviço")
    categoria_id: int = Field(..., gt=0, description="ID da categoria associada")

    @field_validator("nome")
    @classmethod
    def sanitize_nome(cls, v: str) -> str:
        clean = html.escape(v.strip())
        if not re.match(r"^[\w\sÀ-ÿ\.\-']+$", clean, re.UNICODE):
            raise ValueError("O nome contém caracteres inválidos.")
        return clean

    @field_validator("telefone")
    @classmethod
    def validate_and_clean_telefone(cls, v: str) -> str:
        # Remove caracteres de formatação
        digits_only = re.sub(r"\D", "", v)
        # Validação estrita de número brasileiro (DDD + 8 ou 9 dígitos)
        if not re.match(r"^[1-9]{2}9?[0-9]{8}$", digits_only):
            raise ValueError("Número de telefone inválido. Informe DDD + número completo (ex: 11987654321).")
        return digits_only

    @field_validator("descricao")
    @classmethod
    def sanitize_descricao(cls, v: str) -> str:
        clean = html.escape(v.strip())
        if len(clean) < 10:
            raise ValueError("A descrição deve conter no mínimo 10 caracteres.")
        return clean


class PrestadorCreate(PrestadorBase):
    pass


class PrestadorResponse(BaseModel):
    id: int
    nome: str
    telefone: str
    descricao: str
    ativo: bool
    categoria_id: int
    categoria: Optional[CategoriaResponse] = None
    data_cadastro: datetime

    model_config = ConfigDict(from_attributes=True)


class ConexaoCreate(BaseModel):
    prestador_id: int = Field(..., gt=0)


class ConexaoResponse(BaseModel):
    id: int
    prestador_id: int
    nome_prestador: str
    whatsapp_url: str
    mensagem_status: str
    status: str

    model_config = ConfigDict(from_attributes=True)
