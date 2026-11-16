# ConectaBairro PWA — Plataforma Comunitária de Serviços

O **ConectaBairro PWA** é uma aplicação web progressiva (PWA) desenvolvida para conectar moradores e trabalhadores autônomos locais na comunidade (região da AMBE), impulsionando a economia circular e a geração de renda (alinhamento com as ODS 8 e ODS 10 da ONU).

---

## 🛠️ Tecnologias Utilizadas

* **Backend:** Python 3.10+ com **FastAPI** e **Uvicorn**
* **Banco de Dados & ORM:** **SQLAlchemy** (SQLite para desenvolvimento/testes locais e PostgreSQL para produção)
* **Validação & Sanitização:** **Pydantic v2** com expressões regulares (Regex) e escape de HTML contra XSS e SQL Injection
* **Frontend:** PWA com HTML5 semântico, CSS3 mobile-first (WCAG 2.1 AA) e Service Worker para cache offline
* **Testes Automatizados:** **pytest** com cobertura dos fluxos de todas as telas
* **CI/CD:** **GitHub Actions** automatizado

---

## 🏛️ Arquitetura do Sistema

O projeto adota uma arquitetura em camadas limpa e modular:

```text
conectabairro-pwa/
├── .github/workflows/ci.yml       # Pipeline automatizado de integração contínua
├── app/
│   ├── main.py                    # Configuração da aplicação, CORS e injeção de rotas
│   ├── database.py                # Conexão de banco e pool de sessões (get_db)
│   ├── models.py                  # Modelos relacionais ORM (SQLAlchemy)
│   ├── schemas.py                 # Validação estrita de tipos e sanitização (Pydantic)
│   ├── crud.py                    # Operações de banco de dados desacopladas
│   ├── routers/
│   │   ├── vitrine.py             # Tela 1: Listagem e filtros de categorias (RF01)
│   │   ├── prestador.py           # Tela 2: Auto-cadastro e validações (RF03, RNF01, RNF02)
│   │   └── conexao.py             # Tela 3: Confirmação e link WhatsApp (RF02, RA01)
│   └── static/                    # Frontend PWA (Mobile-first, WCAG 2.1 AA)
│       ├── css/style.css
│       ├── js/app.js
│       ├── js/service-worker.js
│       └── manifest.json
└── tests/                         # Suíte de testes automatizados com pytest
```

---

## 🚀 Como Executar o Projeto

### 1. Clonar o repositório
```bash
git clone https://github.com/MRolemberg/TesteConectaBairro.git
cd TesteConectaBairro
```

### 2. Criar e ativar o ambiente virtual
```bash
python -m venv venv
# No Windows:
venv\Scripts\activate
# No Linux/Mac:
source venv/bin/activate
```

### 3. Instalar as dependências
```bash
pip install -r requirements.txt
```

### 4. Executar os testes automatizados
```bash
pytest -v
```

### 5. Iniciar o servidor de desenvolvimento
```bash
uvicorn app.main:app --reload
```
Acesse a aplicação no navegador em `http://127.0.0.1:8000`.
A documentação interativa Swagger está disponível em `http://127.0.0.1:8000/docs`.

---

## ♿ Acessibilidade e Segurança

* **WCAG 2.1 AA:** Redundância informativa rigorosa na tela de confirmação (ícones de estado, texto explícito em caixa alta e contraste cromático elevado para daltônicos). Áreas de clique mínimas de 44x44px.
* **Segurança e Sanitização:** Validação estrita de entradas via Pydantic, regex para telefones no padrão brasileiro e queries parametrizadas via ORM prevenindo SQL Injection.
