import pytest
from feira.app import create_app
from feira.db import db
from feira.mvc.controller import importar_csv
import pytest
import os


@pytest.fixture
def app():
    app = create_app()
    return app


@pytest.fixture
def mock_feira_criar():
    mock_criar_feira = {
        "registro": "1705-1",
        "nome": "Feira do Gabriel",
        "distrito": "Teste",
        "regiao": "Teste",
        "logradouro": "Teste",
        "numero": "1234",
        "bairro": "Teste",
        "referencia": "Teste",
    }

    return mock_criar_feira


@pytest.fixture(autouse=True)
def conexao_banco(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test_feira.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.create_all()

    importar_csv("./DEINFO_AB_FEIRASLIVRES_2014.csv")

    yield db.init_app(app)

    os.remove("./feira/test_feira.db")
