"""
Configuração do banco de dados relacional e pool de conexões com SQLAlchemy.
Suporta SQLite para ambiente local/desenvolvimento e PostgreSQL para produção.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./conectabairro.db")

# Configuração com pool otimizado e tratamento para multithreading no SQLite
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        pool_pre_ping=True
    )
else:
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    Gerador de dependência de sessão de banco de dados.
    Garante fechamento correto da sessão após o ciclo da requisição,
    prevenindo vazamento de conexões e memória.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
