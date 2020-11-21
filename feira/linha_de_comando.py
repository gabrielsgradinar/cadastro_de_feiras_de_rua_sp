import click
from feira.db import db
import feira.mvc.model
from feira.mvc.controller import importar_csv
from flask.cli import AppGroup

feira_cli = AppGroup("feira")


@feira_cli.command("create_db")
def create_db():
    """Este comando inicializa o banco de dados"""
    db.create_all()
    click.echo("Banco de dados criado")


@feira_cli.command("import_csv")
def import_csv():
    """Este comando realiza a importação dos dados do arquivo excel para o banco de dados"""
    arquivo = "./DEINFO_AB_FEIRASLIVRES_2014.csv"
    click.echo(importar_csv(arquivo))


def init_app(app):
    app.cli.add_command(feira_cli)
