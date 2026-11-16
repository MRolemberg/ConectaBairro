"""
Testes automatizados para a Tela 3: Confirmação e Contato WhatsApp (RF02, RA01).
Verifica a geração do link padronizado e tratamento de exceções.
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_iniciar_conexao_sucesso():
    payload = {"prestador_id": 1}
    response = client.post("/api/conexao/iniciar", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["prestador_id"] == 1
    assert "https://wa.me/55" in data["whatsapp_url"]
    assert "mensagem_status" in data
    assert data["status"] == "ativa"


def test_iniciar_conexao_prestador_inexistente():
    payload = {"prestador_id": 99999}
    response = client.post("/api/conexao/iniciar", json=payload)
    assert response.status_code == 404
    assert "não foi localizado" in response.json()["detail"]
