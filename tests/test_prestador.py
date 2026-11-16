"""
Testes automatizados para a Tela 2: Auto-Cadastro de Prestador (RF03, RNF01, RNF02).
Validação de inputs, sanitização de caracteres e tratamento de erros.
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_cadastrar_prestador_sucesso():
    payload = {
        "nome": "Marcos Silva Eletricista",
        "telefone": "(11) 98888-7777",
        "categoria_id": 1,
        "descricao": "Instalações elétricas residenciais e comerciais com garantia."
    }
    response = client.post("/api/prestadores", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == "Marcos Silva Eletricista"
    assert data["telefone"] == "11988887777"
    assert data["ativo"] is True
    assert "id" in data


def test_cadastrar_prestador_nome_invalido():
    payload = {
        "nome": "João <script>alert(1)</script>",
        "telefone": "11988887777",
        "categoria_id": 1,
        "descricao": "Instalações elétricas com segurança e garantia."
    }
    response = client.post("/api/prestadores", json=payload)
    assert response.status_code == 422


def test_cadastrar_prestador_telefone_invalido():
    payload = {
        "nome": "João Sem Telefone",
        "telefone": "12345",
        "categoria_id": 1,
        "descricao": "Trabalhos de pintura de paredes e tetos residenciais."
    }
    response = client.post("/api/prestadores", json=payload)
    assert response.status_code == 422


def test_cadastrar_prestador_descricao_curta():
    payload = {
        "nome": "Pedro Pedreiro",
        "telefone": "11999998888",
        "categoria_id": 1,
        "descricao": "Curto"
    }
    response = client.post("/api/prestadores", json=payload)
    assert response.status_code == 422


def test_cadastrar_prestador_categoria_inexistente():
    payload = {
        "nome": "Antônio Marceneiro",
        "telefone": "11999998888",
        "categoria_id": 99999,
        "descricao": "Móveis planejados sob medida e reformas de estofados."
    }
    response = client.post("/api/prestadores", json=payload)
    assert response.status_code == 400
    assert "Categoria" in response.json()["detail"]


def test_obter_prestador_por_id():
    response = client.get("/api/prestadores/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert "nome" in data


def test_obter_prestador_inexistente():
    response = client.get("/api/prestadores/99999")
    assert response.status_code == 404
    assert "não encontrado" in response.json()["detail"]
