from feira.mvc.model import Feira
from feira.linha_de_comando import import_csv, create_db
import os


def test_comando_importar_csv(app):
    Feira.query.delete()
    runner = app.test_cli_runner()
    result = runner.invoke(import_csv)
    assert "Foram importadas 880" in result.output


def test_comando_criar_banco_de_dados(app):
    os.remove("./feira/test_feira.db")
    runner = app.test_cli_runner()
    result = runner.invoke(create_db)
    assert "Banco de dados criado" in result.output
