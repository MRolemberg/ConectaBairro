"""
Testes automatizados para a Tela 1: Vitrine Comunitária e Filtros (RF01).
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine, SessionLocal
from app.crud import seed_initial_data


@pytest.fixture(scope="module", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    seed_initial_data(db)
    db.close()
    yield
    # Limpeza se necessário


client = TestClient(app)


def test_healthcheck():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_listar_categorias_vitrine():
    response = client.get("/api/vitrine/categorias")
    assert response.status_code == 200
    categorias = response.json()
    assert isinstance(categorias, list)
    assert len(categorias) >= 3
    slugs = [c["slug"] for c in categorias]
    assert "eletrica" in slugs
    assert "pintura" in slugs


def test_listar_prestadores_sem_filtro():
    response = client.get("/api/vitrine/prestadores")
    assert response.status_code == 200
    prestadores = response.json()
    assert isinstance(prestadores, list)
    assert len(prestadores) > 0


def test_listar_prestadores_com_filtro_valido():
    # Buscar ID da categoria eletrica
    res_cat = client.get("/api/vitrine/categorias")
    categorias = res_cat.json()
    cat_eletrica = next(c for c in categorias if c["slug"] == "eletrica")

    response = client.get(f"/api/vitrine/prestadores?categoria_id={cat_eletrica['id']}")
    assert response.status_code == 200
    prestadores = response.json()
    assert all(p["categoria_id"] == cat_eletrica["id"] for p in prestadores)


def test_listar_prestadores_categoria_inexistente():
    response = client.get("/api/vitrine/prestadores?categoria_id=99999")
    assert response.status_code == 404
