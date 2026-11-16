import pytest
from app.database import Base, engine, SessionLocal
from app.crud import seed_initial_data


@pytest.fixture(scope="session", autouse=True)
def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    seed_initial_data(db)
    db.close()
    yield
